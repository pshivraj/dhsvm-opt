#!/bin/bash

set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

chmod a+x ~/.bashrc
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -u &&
echo 'export PATH=~/miniconda3/bin:$PATH' >> ~/.bashrc &&
source ~/.bashrc
source ~/miniconda3/etc/profile.d/conda.sh
conda create -n dhsvm-opt -y &&
conda activate dhsvm-opt &&
cd scripts/sql-setup && bash sql-setup.sh && cd ../..
rm -rf spotpy &&
git clone https://github.com/pshivraj/spotpy.git && cd spotpy && python setup.py install
