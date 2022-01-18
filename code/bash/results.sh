#!/bin/bash -e
#SBATCH --partition=csedu
#SBATCH --gres=gpu:1
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00
#SBATCH --output=results-%J.out
#SBATCH --error=results-%J.err
#SBATCH --mail-user=thomaskolb@live.nl
#SBATCH --mail-type=BEGIN,END,FAIL

basepath="/home/tkolb/bsc/data/fairseq-evals"
filename="WERdata_test.txt"

nfiles=$(ls ~/bsc/data/results | wc -l)
if [[ $nfiles > 0 ]]; then
    rm -r ~/bsc/data/results/*
fi
source ~/.cache/pypoetry/virtualenvs/tkolbpoetry-0grRN4_Q-py3.6/bin/activate
python3 ../interpretresults.py "/home/tkolb/bsc/data/results" \
    "$basepath/2021-11-11/18-12-54/$filename" \
    "$basepath/2021-11-12/10-12-27/$filename" \
    "$basepath/2021-11-12/10-34-58/$filename" \
    "$basepath/2021-11-14/15-14-42/$filename" \
    "$basepath/2021-11-14/15-23-43/$filename" \
    "$basepath/2021-11-14/15-30-40/$filename" \
    "$basepath/2021-11-15/11-44-06/$filename" \
    "$basepath/2021-11-15/11-45-07/$filename" \
    "$basepath/2021-11-15/13-23-43/$filename"
deactivate