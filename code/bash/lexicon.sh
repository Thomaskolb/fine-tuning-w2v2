#!/bin/bash -e
#SBATCH --partition=csedu
#SBATCH --gres=gpu:1
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1
#SBATCH --time=0:15:00
#SBATCH --output=lexicon-%J.out
#SBATCH --error=lexicon-%J.err
#SBATCH --mail-user=thomaskolb@live.nl
#SBATCH --mail-type=BEGIN,END,FAIL

source ~/.cache/pypoetry/virtualenvs/tkolbpoetry-0grRN4_Q-py3.6/bin/activate
python3 ../extractlexicon.py "/home/tkolb/bsc/data/models/c3lmfile.txt" "/home/tkolb/bsc/data/models/c3lexicon.txt"
deactivate
