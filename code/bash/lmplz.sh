#!/bin/bash -e
#SBATCH --partition=csedu
#SBATCH --gres=gpu:1
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00
#SBATCH --output=lmplz-%J.out
#SBATCH --error=lmplz-%J.err
#SBATCH --mail-user=thomaskolb@live.nl
#SBATCH --mail-type=BEGIN,END,FAIL

lmfile="c3lmfile"

source ~/.cache/pypoetry/virtualenvs/tkolbpoetry-0grRN4_Q-py3.6/bin/activate
python3 ../LMgenerator.py "/home/tkolb/bsc/thomas/data" "/home/tkolb/bsc/data/models/$lmfile.txt"
~/bsc/data/kenlm/build/bin/lmplz --discount_fallback -o 5 < ~/bsc/data/models/$lmfile.txt > ~/bsc/data/models/$lmfile.arpa
~/bsc/data/kenlm/build/bin/build_binary ~/bsc/data/models/$lmfile.arpa ~/bsc/data/models/$lmfile.bin
deactivate