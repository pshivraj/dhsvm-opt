#!/bin/bash
  
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -u &&
echo 'export PATH=~/miniconda/bin:$PATH' >> ~/.bashrc &&
conda create -n dhsvm-opt python=3.6 -y &&
source ~/miniconda3/etc/profile.d/conda.sh
conda activate dhsvm-opt
cd scripts/sql-setup
bash test.sh && cd ../..
