# Thomas Kolb s1027332
# This program interprets all the collected results from training and creates tensorboard log

import tensorflow as tf
import sys

# Number of datapoints per configuration
dps_per_config = 3

# Translate steps to hours
to_hours = [8, 16, 32]

# Write data dictionary to tensorflow log file
def write_data(data, outpath):
    for config in data:
        file_writer = tf.summary.create_file_writer(f'{outpath}/{config}')
        with file_writer.as_default():
            for i in range(len(data[config])):
                tf.summary.scalar('results', data[config][i], step=to_hours[i])

# Interpret data given from differen configuration outputs
def interpret_data(config_path_list):
    data_dict = {}
    config_id = 1
    dataset_id = 0
    for config_path in config_path_list:
        with open(config_path, 'r') as file:
            lines = file.read().split('\n')
            number = (lines[-3]).split(' ')[-1]
            value = float(number)
            asr_number = (lines[-2]).split(' ')[-1]
            asr_value = float(asr_number)
            if f'configuration {config_id}' not in data_dict:
                data_dict[f'configuration {config_id}'] = [value]
                data_dict[f'asr {config_id}'] = [asr_value]
            else:
                data_dict[f'configuration {config_id}'].append(value)
                data_dict[f'asr {config_id}'].append(asr_value)
        dataset_id = (dataset_id + 1) % dps_per_config
        if dataset_id == 0:
            config_id += 1
    return data_dict

if len(sys.argv) < 3:
    print("Please enter the output path and the configuration data paths")
else:
    write_data(interpret_data(sys.argv[2:]), sys.argv[1])