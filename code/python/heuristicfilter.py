# Thomas Kolb s1027332
# This program filters data that is not useful for training the wav2vec2 model

import webvttparser
import wave
import sys
import os
import re

# Extension of subtitle files
subtitle_ext = '.vtt'

# Weblinks that are allowed to be used for data
weblink_exceptions = ['nos.nl', 'service.npo.nl', 'npo.nl', 'eenvandaag.nl', 'bbc.nl', 'coronavaccinatie.nl']

# Words that indicate uselessness of data
unfit_data_indicators = ['LIVEPROGRAMMA,', 'LIVEPROGRAMMA', 'LIVE', 'ONDERTITELD', 'ACHTERLOPEN', 'MUZIEK']

# Minimal number of captions required in subtitle file for data to be used
min_caption_count = 10

# Numbers of captions to check to see if data is unique
unique_data_check = 5

# Data files starting with this string will be used as test data
test_data_date = '2022-01'

# Number of files for validation (of train data)
validation_files = 0

# Configurations to enable/disable weblinks and broadcasts, look for double data
weblinks_allowed = False
broadcasts_allowed = False
doubledata_allowed = False

# Function that traverses all 'webm.vtt' files within a given directory
# and filters them based on requirements
def filter_vtt_data(path):
    filtered_paths = []
    unique_data = []
    path_count = 0
    for folder in os.listdir(path):
        vttfiles = [f for f in os.listdir(f"{path}/{folder}") if os.path.splitext(f)[1] == subtitle_ext]
        path_count += len(vttfiles)
        for vttfile in vttfiles:
            captions = webvttparser.read(f"{path}/{folder}/{vttfile}")
            wavfile = vttfile.split('.')[0] + '.wav'
            is_unique_data, unique_data =  check_unique_data(captions, unique_data)
            if (len(captions) >= min_caption_count 
                    and (doubledata_allowed or is_unique_data)
                    and synchronized(captions, f'{path}/{folder}/{wavfile}') 
                    and meets_data_requirements(captions)):
                filtered_paths.append(f"{folder}/{vttfile.split('.')[0]}")
    percentage = "{:.1f}".format((len(filtered_paths)/path_count)*100)
    return filtered_paths, percentage

# Function that decides whether data can be used
def meets_data_requirements(captions):
    for caption in [c.text.split() for c in captions]:
        for word in caption:
            if (not weblinks_allowed and is_weblink(word)) or (not broadcasts_allowed and is_livebroadcast(word)):
                return False
    return True

# Function that checks if the data is unique by looking at the first n captions
def check_unique_data(captions, unique_data):
    for data in reversed(unique_data):
        check_length = min(len(captions), len(data))
        for i in range(check_length):
            if data[i].text != captions[i].text:
                break
            elif i >= check_length-1:
                return False, unique_data
    if len(captions) > 0:
        unique_data.append(captions[:min(len(captions), unique_data_check)])
    return True, unique_data

# Function that checks whether caption times are within wavfile length
def synchronized(captions, wavpath):
    if os.path.isfile(wavpath):
        with wave.open(wavpath, 'r') as wavfile:
            # I also tried this for end_frame, but hardly any data was salvaged (< 3%)
            start_frame = int(webvttparser.get_time_in_seconds(captions[len(captions)-1].start) * wavfile.getframerate())
            return start_frame <= wavfile.getnframes()
    return False

# Checks whether a string contains a weblink
def is_weblink(word):
    if re.match("([a-zA-Z]{1,})\.([a-zA-Z]{1,})", word) and not any([word.lower().startswith(exc) for exc in weblink_exceptions]):
        return True
    return False

# Checks whether a string is an indicator of a live broadcast
def is_livebroadcast(word):
    return word in unfit_data_indicators

# Write data to txt file, first two files in test data will be used for validation
def write_data(paths, outdir):
    try:
        os.makedirs(outdir)
    except FileExistsError:
        pass
    validation_paths = validation_files
    with open(f'{outdir}/train.txt', 'w') as train_data, \
            open(f'{outdir}/valid.txt', 'w') as validation_data, \
            open(f'{outdir}/test.txt', 'w') as test_data:
        for path in paths:
            if path.startswith(test_data_date):
                test_data.write(path + '\n')
            else:
                if validation_paths > 0:
                    validation_data.write(path + '\n')
                    validation_paths -= 1
                else:
                    train_data.write(path + '\n')

if len(sys.argv) < 3:
    print("Please enter the data path and the output directory")
else:
    # List of file paths that will be used for training
    filepaths, percentage = filter_vtt_data(sys.argv[1])
    write_data(filepaths, sys.argv[2])
    print(f"{percentage}% of data salvaged")