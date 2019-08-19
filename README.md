<h1 align="center">dhsvm-opt - Optimization library for DHSVM</h1>

<div align="center">
  
![Python version](https://img.shields.io/badge/python-3.4+-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## Table of Contents

1. [Introduction](#introduction)
1. [Directory Structure](#directory-structure)
1. [References](#references)
1. [Setup](#setup)


## Introduction

dhsvm-opt is an end to end solution to tune and optimize DHSVM physical parameters using Markov Chain Monte Carlo simulation
algorithm [DFREAM](http://faculty.sites.uci.edu/jasper/files/2016/04/70.pdf) implemented in [spotpy](https://github.com/thouska/spotpy) and using Machine learning methods like Boosted Trees.


## Directory Structure

```
.
├── data
├── scripts
    ├── fast
    ├── dream
    ├── decision_tree
    ├── sql-setup

```

## Setup

Run setup file to get the custom sql version installed to handle ```30,000 columns```. 
Running below sets of command would setup a conda environment ```dhsvm-opt``` with custom sqlite version.

```
bash -i setup.sh
source ~/.bashrc
conda activate dhsvm-opt
```



## References

### Literature

1. [DREAM -an adaptive Markov Chain Monte Carlo simulation algorithm to solve discrete, noncontinuous, and combinatorial
posterior parameter estimation problems ](http://faculty.sites.uci.edu/jasper/files/2016/04/70.pdf)

### Implementations

1. [spotpy- A Statistical Parameter Optimization Tool](https://github.com/thouska/spotpy)
