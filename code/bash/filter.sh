#!/bin/bash -e
#SBATCH --partition=csedu
#SBATCH --gres=gpu:1
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1
#SBATCH --time=0:15:00
#SBATCH --output=filter-%J.out
#SBATCH --error=filter-%J.err
#SBATCH --mail-user=thomaskolb@live.nl
#SBATCH --mail-type=BEGIN,END,FAIL

source ~/.cache/pypoetry/virtualenvs/tkolbpoetry-0grRN4_Q-py3.6/bin/activate
python3 ../heuristicfilter.py "/home/tkolb/bsc/data/datanew" "/home/tkolb/bsc/bsc-thesis/filtered"
deactivate
