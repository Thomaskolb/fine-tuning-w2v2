# Thomas Kolb s1027332
# This program uses the collection of lines from 'infile_name.wrd' with a given pattern (using grep)
# The output of this program is a 'collect.wrd', 'collect.ltr', 'asr-collect.txt' and 'collect.tsv' file
# With 'line - file' pairs that contain the pattern

import sys

# File name from where we collect the file - line pairs
infile_name = 'train'

# Function that collects line numbers with pattern
def collect_line_numbers(path):
    with open(f'{path}/collected.txt', 'r') as collect_file:
        return [int(line.split(':')[0]) for line in collect_file.read().split('\n') if line]

# Read 'infile_name' files and output ltr, wrd, tsv and asr data
def write_partition(path, line_numbers):
    # Write data for all 4 files
    write_file(path, f'{infile_name}.ltr', 'collect.ltr', line_numbers)
    write_file(path, f'{infile_name}.wrd', 'collect.wrd', line_numbers)
    write_file(path, f'{infile_name}.tsv', 'collect.tsv', line_numbers)
    write_file(path, f'asr-{infile_name}.txt', 'asr-collect.txt', line_numbers)

# Write data to collect file using line_numbers
def write_file(path, infile_name, outfile_name, line_numbers):
    with open(f'{path}/{infile_name}', 'r') as infile, open(f'{path}/{outfile_name}', 'w') as outfile:
        lines = infile.read().split('\n')
        # If tsv extension then write first line also
        offset = 1
        if outfile_name[-3:] == "tsv":
            outfile.write(f'{lines[0]}\n')
            offset = 0
        [outfile.write(f'{lines[number-offset]}\n') for number in line_numbers]

if len(sys.argv) < 2:
    print("Please enter the data folder")
else:
    write_partition(sys.argv[1], collect_line_numbers(sys.argv[1]))