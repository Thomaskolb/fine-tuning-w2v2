#!/bin/bash -e
#SBATCH --partition=csedu
#SBATCH --gres=gpu:1
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1
#SBATCH --time=0:15:00
#SBATCH --output=alphabet-%J.out
#SBATCH --error=alphabet-%J.err
#SBATCH --mail-user=thomaskolb@live.nl
#SBATCH --mail-type=BEGIN,END,FAIL

source ~/.cache/pypoetry/virtualenvs/tkolbpoetry-0grRN4_Q-py3.6/bin/activate
python3 ../extractalphabet.py "/home/tkolb/bsc/data/testset/c3h8/test.ltr" "/home/tkolb/bsc/data/testset/c3h8/dict.ltr.txt"
deactivate
