#!/bin/bash
#SBATCH --job-name=create_ITMO_dirs
#SBATCH --nodes 1
#SBATCH --tasks-per-node=1
#SBATCH --account=def-panos
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=16G
#SBATCH --time=0:30:00


module load python/3.10

module load  StdEnv/2020  cuda cudnn
module load gcc opencv

source ./ENV/bin/activate

echo "Creating directories..."

python ./create_datasets.py



