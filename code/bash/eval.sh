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
# config 1
# datetime1="2021-11-11/18-12-54"
# datetime2="2021-11-12/10-12-27"
# datetime3="2021-11-12/10-34-58"
# config 2
# datetime1="2021-11-14/15-14-42"
# datetime2="2021-11-14/15-23-43"
# datetime3="2021-11-14/15-30-40"
# config 3
# datetime1="2021-11-15/11-44-06"
# datetime2="2021-11-15/11-45-07"
# datetime3="2021-11-15/13-23-43"
# base10
# ctc
datetime1="2021-12-04/16-32-37"
datetime2="2021-12-08/15-10-32"
datetime3="2021-12-04/16-34-35"
# c
# datetime1="2021-11-14/15-14-42"
# datetime2="2021-11-14/15-23-43"
# datetime3="2021-11-14/15-30-40"
# xlsr
# ctc
# datetime1="2021-12-16/12-12-56"
# datetime2="2021-12-16/12-15-36"
# datetime3="2021-12-12/11-41-57"
# c
# datetime1="2021-12-20/16-11-51"
# datetime2="2021-12-20/16-23-34"
# datetime3="2021-12-20/16-24-42"

# configs = 11-12|11-11|11-14|11-15 ctc = 12-04|12-08
# xlsr = 12-20 ctc = 2021-12-16/12-12-56|2021-12-16/12-15-36|2021-12-12/11-41-57

valid_data_path="/home/tkolb/bsc/data/testset/ctc2h8"
lmfile="c2lmfile.bin"
lexicon="c2lexicon.txt"
gen_subset="test"
outputsfolder="fairseq-outputs"
evalsfolder="fairseq-evals-base/opt"

source ~/.cache/pypoetry/virtualenvs/new-env-xry5bPeK-py3.8/bin/activate
python3.8 ~/bsc/fairseq/examples/speech_recognition/infer.py \
    $valid_data_path \
    --task audio_finetuning \
    --nbest 1 \
    --path ~/bsc/data/$outputsfolder/$datetime1/checkpoints/checkpoint_best.pt \
    --gen-subset $gen_subset \
    --results-path ~/bsc/data/$evalsfolder/$datetime1/$gen_subset \
    --w2l-decoder kenlm \
    --lm-model ~/bsc/data/models/$lmfile \
    --lm-weight 2 \
    --lexicon ~/bsc/data/models/$lexicon \
    --word-score 0 \
    --sil-weight 0 \
    --criterion ctc \
    --labels ltr \
    --max-tokens 1000000 \
    --post-process letter
python3.8 ../extractWER.py "/home/tkolb/bsc/data/$evalsfolder/$datetime1/$gen_subset" $valid_data_path "base"
python3.8 ~/bsc/fairseq/examples/speech_recognition/infer.py \
    $valid_data_path \
    --task audio_finetuning \
    --nbest 1 \
    --path ~/bsc/data/$outputsfolder/$datetime2/checkpoints/checkpoint_best.pt \
    --gen-subset $gen_subset \
    --results-path ~/bsc/data/$evalsfolder/$datetime2/$gen_subset \
    --w2l-decoder kenlm \
    --lm-model ~/bsc/data/models/$lmfile \
    --lm-weight 1.2 \
    --lexicon ~/bsc/data/models/$lexicon \
    --word-score 0 \
    --sil-weight 0 \
    --criterion ctc \
    --labels ltr \
    --max-tokens 1000000 \
    --post-process letter
python3.8 ../extractWER.py "/home/tkolb/bsc/data/$evalsfolder/$datetime2/$gen_subset" $valid_data_path "base"
python3.8 ~/bsc/fairseq/examples/speech_recognition/infer.py \
    $valid_data_path \
    --task audio_finetuning \
    --nbest 1 \
    --path ~/bsc/data/$outputsfolder/$datetime3/checkpoints/checkpoint_best.pt \
    --gen-subset $gen_subset \
    --results-path ~/bsc/data/$evalsfolder/$datetime3/$gen_subset \
    --w2l-decoder kenlm \
    --lm-model ~/bsc/data/models/$lmfile \
    --lm-weight 1.2 \
    --lexicon ~/bsc/data/models/$lexicon \
    --word-score 0 \
    --sil-weight 0 \
    --criterion ctc \
    --labels ltr \
    --max-tokens 1000000 \
    --post-process letter
python3.8 ../extractWER.py "/home/tkolb/bsc/data/$evalsfolder/$datetime3/$gen_subset" $valid_data_path "base"
deactivate