#!/bin/bash -e
#SBATCH --partition=csedu
#SBATCH --gres=gpu:1
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00
#SBATCH --output=rename-%J.out
#SBATCH --error=rename-%J.err
#SBATCH --mail-user=thomaskolb@live.nl
#SBATCH --mail-type=BEGIN,END,FAIL

addtoname="_ws2_"

mv /home/tkolb/bsc/data/fairseq-evals/2021-11-14/15-14-42/test/WERdata_test.txt /home/tkolb/bsc/data/fairseq-evals/2021-11-14/15-14-42/test/WERdata_test${addtoname}8.txt
mv /home/tkolb/bsc/data/fairseq-evals/2021-11-14/15-23-43/test/WERdata_test.txt /home/tkolb/bsc/data/fairseq-evals/2021-11-14/15-23-43/test/WERdata_test${addtoname}16.txt
mv /home/tkolb/bsc/data/fairseq-evals/2021-11-14/15-30-40/test/WERdata_test.txt /home/tkolb/bsc/data/fairseq-evals/2021-11-14/15-30-40/test/WERdata_test${addtoname}32.txt