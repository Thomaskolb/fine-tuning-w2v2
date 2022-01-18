# Thomas Kolb s1027332
# This program reads all the collected results from training and finds the captions that performed better than the ASR

import sys

# Active configuration
active_config = 2

# File name to analyse
wer_data_file = 'WERdata_test_base.txt'

# Line of equal chars
bar = '=' * 30

# type of test currently being analyzed
value_test = False
interpunction_test = False
eh_test = False

# List of interpunction symbols - no '.' because it is not interesting
# interpunction = [',', '!', '?', '-', ':']
interpunction = ['...']

# list of 'eh' words
eh_words = ['eh', 'euh', 'uh']

# Function that finds the well performed captions with list of paths and writes them to output file
def write_data(outpath, paths):
    for path in paths:
        with open(outpath, 'w') as outfile, open(f'{path}/{wer_data_file}', 'r') as infile:
            lines = infile.read().split('\n')
            refs = lines[0:-3:10]
            hyps = lines[1:-3:10]
            asrs = lines[5:-3:10]
            asr_values = lines[7:-3:10]
            values = lines[3:-3:10]
            cases = 0
            correct_cases = 0
            line_count = 0
            total_line_count = 0
            word_counts = (0, 0, 0)
            for i in range(len(values)):
                total_line_count += 1
                value = values[i].split(' ')[-1]
                asr_value = asr_values[i].split(' ')[-1]
                int_hyp_count = sum([word in interpunction for word in hyps[i][5:].split(' ')])
                eh_asr_count = sum([any([word.startswith(eh) for eh in eh_words]) for word in asrs[i][5:].split(' ')])
                word_counts = (
                    word_counts[0] + len([x for x in refs[i][5:] if x is not ' ' and x is not '*']), 
                    word_counts[1] + len([x for x in hyps[i][5:] if x is not ' ' and x is not '*']), 
                    word_counts[2] + len([x for x in asrs[i][5:] if x is not ' ' and x is not '*']))
                if ((not value_test or value < asr_value)
                        and (not interpunction_test or int_hyp_count > 0)
                        and (not eh_test or eh_asr_count > 0)):
                    line_count += 1
                    outfile.write(f'val {value} - asr {asr_value}\nREF={refs[i][5:]}\nHYP={hyps[i][5:]}\nASR={asrs[i][5:]}\n{bar}\n\n')
                    outfile.write(f'{word_counts}\n')
                    int_ref_count = sum([word in interpunction for word in refs[i][5:].split(' ')])
                    eh_hyp_count = sum([any([word.startswith(eh) for eh in eh_words]) for word in hyps[i][5:].split(' ')])
                    # Add 1 for each occurence
                    cases += interpunction_test*int_ref_count + eh_test*eh_asr_count
                    correct_cases += interpunction_test*sum([sum([refs[i][5:][ind] == c == w for ind,w in enumerate(hyps[i][5:])]) for c in interpunction])
                    correct_cases += eh_test*(eh_hyp_count == 0)
            if interpunction_test or eh_test:
                outfile.write(f'Total cases: {cases}, conditioned cases: {correct_cases}\n')
            outfile.write(f'Line count: {line_count}, total line count: {total_line_count}\n')
            outfile.write(f'Ref word count: {word_counts[0]}, hyp word count: {word_counts[1]}, asr word count: {word_counts[2]}\n')

if len(sys.argv) < 2:
    print("Please enter the output file and the configuration data paths")
else:
    write_data(sys.argv[1], sys.argv[2:])