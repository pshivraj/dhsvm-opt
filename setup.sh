#!/bin/bash
  
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -u &&
echo 'export PATH=~/miniconda3/bin:$PATH' >> ~/.bashrc &&
source ~/.bashrc
conda init bash
conda create -n dhsvm-opt python=3.6 -y &&
conda activate dhsvm-opt
cd scripts/sql-setup && bash sql-setup.sh && cd ../..
