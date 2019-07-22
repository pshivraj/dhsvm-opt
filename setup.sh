#!/bin/bash
  
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -u &&
echo 'export PATH=~/miniconda3/bin:$PATH' >> ~/.bashrc &&
source ~/.bashrc
cd scripts/sql-setup && bash sql-setup.sh && cd ../..
conda create -n dhsvm-opt &&
conda activate dhsvm-opt
