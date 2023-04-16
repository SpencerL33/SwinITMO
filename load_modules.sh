#!/bin/sh

module load python/3.10
module load StdEnv/2020 cuda cudnn
module load gcc opencv
virtualenv --no-download ENV
source ENV/bin/activate
pip install --no-index --upgrade pip
pip install numpy --no-index
pip install -r requirement.txt
