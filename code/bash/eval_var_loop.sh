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

datetime1="2021-12-20/16-24-42"
valid_data_path="/home/tkolb/bsc/data/testset/c2h8"
lmfile="c2lmfile.bin"
lexicon="c2lexicon.txt"
gen_subset="test"
outputsfolder="fairseq-outputs-xlsr"
evalsfolder="fairseq-evals-xlsr/varloop/two"

source ~/.cache/pypoetry/virtualenvs/new-env-xry5bPeK-py3.8/bin/activate
for lmw in $(seq 0.0 .1 4.0)
do
    python3.8 ~/bsc/fairseq/examples/speech_recognition/infer.py \
        $valid_data_path \
        --task audio_finetuning \
        --nbest 1 \
        --path ~/bsc/data/$outputsfolder/$datetime1/checkpoints/checkpoint_best.pt \
        --gen-subset $gen_subset \
        --results-path ~/bsc/data/$evalsfolder/$datetime1/$gen_subset \
        --w2l-decoder kenlm \
        --lm-model ~/bsc/data/models/$lmfile \
        --lm-weight $lmw \
        --lexicon ~/bsc/data/models/$lexicon \
        --word-score -1 \
        --sil-weight 0 \
        --criterion ctc \
        --labels ltr \
        --max-tokens 1000000 \
        --post-process letter
    OUTPUTLM=$(python3.8 ../extractWER.py "/home/tkolb/bsc/data/$evalsfolder/$datetime1/$gen_subset" $valid_data_path "lm$lmw")
    echo -n "${OUTPUTLM}, " >> "/home/tkolb/bsc/data/$evalsfolder/$datetime1/$gen_subset/output-lm.txt"
done
for wsw in $(seq -2.0 .1 2.0)
do
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
        --word-score $wsw \
        --sil-weight 0 \
        --criterion ctc \
        --labels ltr \
        --max-tokens 1000000 \
        --post-process letter
    OUTPUTWS=$(python3.8 ../extractWER.py "/home/tkolb/bsc/data/$evalsfolder/$datetime1/$gen_subset" $valid_data_path "ws$wsw")
    echo -n "${OUTPUTWS}, " >> "/home/tkolb/bsc/data/$evalsfolder/$datetime1/$gen_subset/output-ws.txt"
done
deactivate