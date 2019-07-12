"""
Script to run FAST(Fourier amplitude sensitivity testing).
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import subprocess
from distutils.dir_util import remove_tree
import shutil
import time
import spotpy
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import logging
logging.basicConfig(filename='fast.log', level=logging.INFO, filemode="w")
plt.switch_backend('agg')