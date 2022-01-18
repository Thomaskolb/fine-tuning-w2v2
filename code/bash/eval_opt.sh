#!/bin/bash -e
#SBATCH --partition=csedu
#SBATCH --gres=gpu:1
#SBATCH --mem=50G
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00
#SBATCH --output=eval-%J.out
#SBATCH --error=eval-%J.err
#SBATCH --mail-user=thomaskolb@live.nl
#SBATCH --mail-type=BEGIN,END,FAIL

datetime="2021-12-12/11-41-57"
valid_data_path="/home/tkolb/bsc/data/ctc2tempdata"
lmfile="c2lmfile.bin"
lexicon="c2lexicon.txt"
gen_subset="test"
outputsfolder="fairseq-outputs-xlsr"
evalsfolder="fairseq-evals-xlsr/opt"

source ~/.cache/pypoetry/virtualenvs/new-env-xry5bPeK-py3.8/bin/activate
python3.8 ~/bsc/fairseq/examples/speech_recognition/infer.py \
    $valid_data_path \
    --task audio_finetuning \
    --nbest 1 \
    --path ~/bsc/data/$outputsfolder/$datetime/checkpoints/checkpoint_best.pt \
    --gen-subset $gen_subset \
    --results-path ~/bsc/data/$evalsfolder/$datetime/$gen_subset \
    --w2l-decoder kenlm \
    --lm-model ~/bsc/data/models/$lmfile \
    --lm-weight 3 \
    --lexicon ~/bsc/data/models/$lexicon \
    --word-score 0 \
    --sil-weight 0 \
    --criterion ctc \
    --labels ltr \
    --max-tokens 1000000 \
    --post-process letter
python3.8 ../extractWER.py "/home/tkolb/bsc/data/$evalsfolder/$datetime/$gen_subset" $valid_data_path "base"
deactivate