#!/bin/bash -e
#SBATCH --partition=csedu
#SBATCH --gres=gpu:1
#SBATCH --mem=10G
#SBATCH --cpus-per-task=1
#SBATCH --time=16:00:00
#SBATCH --output=generator-%J.out
#SBATCH --error=generator-%J.err
#SBATCH --mail-user=thomaskolb@live.nl
#SBATCH --mail-type=BEGIN,END,FAIL

source ~/.cache/pypoetry/virtualenvs/new-env-xry5bPeK-py3.8/bin/activate
python3 ../samplegenerator.py "/home/tkolb/bsc/bsc-thesis/filtered" "/home/tkolb/bsc/data/datanew" "/home/tkolb/bsc/data/testset/ctc2h8" 
python3 ../extractalphabet.py "/home/tkolb/bsc/data/testset/ctc2h8/test.ltr" "/home/tkolb/bsc/data/testset/ctc2h8/dict.ltr.txt"
deactivate