# Thomas Kolb s1027332
# This program generates pairs of captions and wav files that can be used for training

# TODO enkele captions eruit filteren
#      X-telefoonnummers
#      X-alles hoofdletters
# TODO subtitles aanpassen
#      X-getallen naar nummers
# TODO 3e argument van outputlist
# TODO filter nutteloze data

import captionparser
import worderrorrate
import webvttparser
import asrparser
import datetime
import wave
import sys
import os

# Minimum error rate allowed
min_wer = 0.2

# Amount of seconds that are subtracted from start time to compensate for subtitles being displayed too late
subtract_start_time = 0.1

# Max number of hours data needed
max_hours = 8

# Domain in which we search for best subtract time for each caption separately, stepsize, start
# So from subtract_start -> subtract_start + subtract_range * subtract_stepsize
subtract_start = -1.0
subtract_stepsize = 0.1
subtract_range = 30

# Now the same for adding at the beginning of a caption
add_start = 1.0
add_stepsize = 0.1
add_range = 30

# Allow strict caption time subtraction
subtract_caption_time = False

# Function that creates the same folders as found in the datapath directory
def create_directories(datapath, outputpath):
    for folder in os.listdir(datapath):
        try:
            os.makedirs(f'{outputpath}/{folder}')
        except FileExistsError:
            pass

# Function that traverses list of datafiles and creates sample subtitle pairs
def generate_pairlist(listpath, datapath, outputpath, type, lines):
    caption_count = 0
    total_caption_count = 0
    total_seconds = 0
    wer_sum = 0
    # max_seconds = max_hours * 3600 * part
    max_lines = lines
    with open(f'{listpath}/{type}.txt', 'r') as data, \
            open(f'{outputpath}/{type}.wrd', 'w') as wrd, \
            open(f'{outputpath}/{type}.ltr', 'w') as ltr, \
            open(f'{outputpath}/asr-{type}.txt', 'w') as asr, \
            open(f'{outputpath}/{type}.tsv', 'w') as filelist:
        filelist.write(outputpath + '\n')
        datalist = data.read().split('\n')
        filepaths = datalist[:len(datalist)-1]
        for filepath in filepaths:
            if caption_count < max_lines:
                file_id = 0
                tcc, cc, wer, sc = generate_pairs(f'{datapath}/{filepath}', outputpath, filepath, file_id, filelist, wrd, ltr, asr)
                total_caption_count += tcc
                caption_count += cc
                wer_sum += wer
                total_seconds += sc
    # percentage = "{:.1f}".format((caption_count/total_caption_count)*100)
    # print(f'{percentage}% of data salvaged\ttotal WER sum: {wer_sum}\tdata length = {str(datetime.timedelta(seconds=total_seconds))}')
    print(f'{caption_count} of {total_caption_count} of data salvaged\ttotal WER sum: {wer_sum}\tdata length = {str(datetime.timedelta(seconds=total_seconds))}')

# Function that generates pairs for a single file
def generate_pairs(filepath, outputpath, folder, file_id, filelist, wrd, ltr, asr):
    captions = webvttparser.read(f'{filepath}.webm.vtt')
    wordsequence = asrparser.read(f'{filepath}.hyp')
    caption_count = 0
    seconds_count = 0
    wer_total = 0
    try:
        os.makedirs(f'{outputpath}/{folder}')
    except:
        pass
    with wave.open(f'{filepath}.wav', 'r') as wavfile:
        for caption in captions:
            new_caption_text = captionparser.acceptable_caption_text(caption.text, ' ')
            # If caption was accepted the length is > 0
            if len(new_caption_text) > 0:
                # Check for the WER with the caption and the asr data to be lower than our threshold
                wer, asr_words, subtract_time, add_time = similar_caption_text(new_caption_text, caption.start, caption.end, wordsequence)
                if wer <= min_wer:
                    if subtract_caption_time:
                        wer, asr_words, subtract_time, add_time = similar_caption_text_subtract(new_caption_text, caption.start, caption.end, wordsequence)
                    start_seconds = webvttparser.get_time_in_seconds(caption.start) + add_time
                    end_seconds = webvttparser.get_time_in_seconds(caption.end) - subtract_time
                    start_frame = int(start_seconds * wavfile.getframerate())
                    end_frame = int(end_seconds * wavfile.getframerate())
                    wavfile.setpos(start_frame)
                    sampleframes = wavfile.readframes(end_frame-start_frame)
                    samplepath = generate_sample(sampleframes, wavfile.getnchannels(), wavfile.getsampwidth(), 
                        wavfile.getframerate(), outputpath, folder, file_id)
                    file_id += 1
                    caption_count += 1
                    seconds_count += end_seconds - start_seconds
                    write_output_files(filelist, samplepath, end_frame-start_frame, new_caption_text, ' '.join(asr_words), wrd, ltr, asr)
                wer_total += wer
    return len(captions), caption_count, wer_total, seconds_count

# Function that writes the output files
def write_output_files(filelist, samplepath, nrframes, new_caption_text, asr_line, wrd, ltr, asr):
    filelist.write(f'{samplepath}\t{nrframes}\n')
    wrd.write(f'{new_caption_text}\n')
    ltr.write(f'{" ".join(list(str(new_caption_text).replace(" ", "|")))} |\n')
    asr.write(f'{asr_line}\n')

# Function that takes sampleframes and generates a new wav file
def generate_sample(sampleframes, channels, samplewidth, framerate, outputpath, folder, file_id):
    samplepath = f'{folder}/{file_id}.wav'
    with wave.open(f'{outputpath}/{samplepath}', 'w') as outfile:
        outfile.setnchannels(channels)
        outfile.setsampwidth(samplewidth)
        outfile.setframerate(framerate)
        outfile.setnframes(int(len(sampleframes) / samplewidth))
        outfile.writeframes(sampleframes)
        return samplepath

# Returns WER between the caption text and the text given by the output of the ASR within the same time frame
def similar_caption_text(new_caption_text, caption_start, caption_end, wordsequence):
    if len(new_caption_text) > 0:
        sequence = asrparser.search_sequence(wordsequence, 
            (webvttparser.get_time_in_seconds(caption_start) - subtract_start_time), webvttparser.get_time_in_seconds(caption_end))
        return worderrorrate.WER(new_caption_text.split(' '), sequence).wer(), sequence, 0, -subtract_start_time

# Slightly different method from 'similar_caption_text', here we try to find the best subtract time for each subtitle
def similar_caption_text_subtract(new_caption_text, caption_start, caption_end, wordsequence):
    if len(new_caption_text) > 0:
        subtract_time = subtract_start
        add_time = add_start
        best_tuple = 1, [], 0, 0
        # First we figure out what we should subtract
        for i in range(subtract_range):
            start_time = webvttparser.get_time_in_seconds(caption_start)
            end_time = webvttparser.get_time_in_seconds(caption_end) - subtract_time
            sequence = asrparser.search_sequence(wordsequence, start_time, end_time)
            current_tuple = worderrorrate.WER(new_caption_text.split(' '), sequence).wer(), sequence, subtract_time, add_time
            subtract_time += subtract_stepsize
            if (end_time - start_time) > 0 and current_tuple[0] < best_tuple[0]:
                best_tuple = current_tuple
        subtract_time = best_tuple[2]
        # And now we figure out what we should add
        for j in range(add_range):
            start_time = webvttparser.get_time_in_seconds(caption_start) + add_time
            end_time = webvttparser.get_time_in_seconds(caption_end) - subtract_time
            sequence = asrparser.search_sequence(wordsequence, start_time, end_time)
            current_tuple = worderrorrate.WER(new_caption_text.split(' '), sequence).wer(), sequence, subtract_time, add_time
            add_time -= add_stepsize
            if (end_time - start_time) > 0 and current_tuple[0] < best_tuple[0]:
                best_tuple = current_tuple
        return best_tuple

if len(sys.argv) < 4:
    print("Please enter the path of the listed data, the data location, and the output directory.")
else:
    # Training data
    # generate_pairlist(sys.argv[1].replace('\\', '/'), sys.argv[2].replace('\\', '/'), sys.argv[3].replace('\\', '/'), 'train', 1)
    # Test data
    generate_pairlist(sys.argv[1].replace('\\', '/'), sys.argv[2].replace('\\', '/'), sys.argv[3].replace('\\', '/'), 'test', 1500)
    # Validation data
    # generate_pairlist(sys.argv[1].replace('\\', '/'), sys.argv[2].replace('\\', '/'), sys.argv[3].replace('\\', '/'), 'valid', 0.1)