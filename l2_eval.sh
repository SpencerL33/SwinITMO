#!/bin/bash
#SBATCH --job-name=l2_eval
#SBATCH -o ./out/%x_%j.out
#SBATCH --nodes 1
#SBATCH --tasks-per-node=1
#SBATCH --account=def-panos
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=16G
#SBATCH --time=0:15:00


module load python/3.10

module load  StdEnv/2020  cuda cudnn
module load gcc opencv

nvidia-smi

source  ~/ENV/bin/activate

cd ~

echo "Testing..."


python ~/KAIR/main_test_psnr.py --opt ~/KAIR/options/swinir/test_swinir_hdr_l2.json



