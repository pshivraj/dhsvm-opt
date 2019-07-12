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

class fast_run_setup(object):
    def __init__(self, parallel='seq'):
        self.params = [spotpy.parameter.Uniform('exponential_decrease_62',low=0.5, high=3,  optguess=1.5),
                       spotpy.parameter.Uniform('lateral_conductivity_62',low=0.0002, high=0.0015,  optguess=0.0008),
                       spotpy.parameter.Uniform('Snow Threshold',low=-6, high=6,  optguess=2),
                       ]
        self.evals = pd.read_csv(VALIDATION_CSV)['value'].values
        self.parallel = parallel

    def parameters(self):
        return spotpy.parameter.generate(self.params)
    
    #setting up simulation for location:12189500 with predefined params and writing to config file 
    def simulation(self, x):
        pid = str(os.getpid())
        logging.info("Initiating Copy for Process %d", format(pid))
        child_dir = "./" + DIR_PREFIX + pid
        shutil.copytree(".", child_dir, ignore=shutil.ignore_patterns(DIR_PREFIX + "*", DB_NAME + "*"))
        logging.info("Copy for Process completed %d", format(pid))
        logging.info("Forking into %s",  child_dir)
        os.chdir(child_dir)

        #write DREAM parameter input to config file.

        change_setting(CONFIG_FILE, "Snow Threshold       ", str(round(x[2],5)))
        change_setting(CONFIG_FILE, "Rain Threshold       ", str(round(x[2]-2,5)))       
        change_setting(CONFIG_FILE, "Exponential Decrease 62", str(round(x[0],5)))
        change_setting(CONFIG_FILE, "Lateral Conductivity 62", str(round(x[1],5)))
        change_setting(CONFIG_FILE, "Maximum Infiltration 62", str(round(x[1]*2,5))) #assume equalt to 2*saturated hydraulic conductivity
        change_setting(CONFIG_FILE, "Vertical Conductivity 62"," ".join([str(round(x[1],5)),str(round(x[1],5)),str(round(x[1],5))]))

        #run DHSVM with modified parameters in config file
        subprocess.call(DHSVM_CMD, shell=True, stdout=False, stderr=False)
        simulations=[]
        #read streamflow data from DHSVM output file
        with open(STREAMFLOW_ONLY, 'r') as file_output:
            header_name = file_output.readlines()[0].split(' ')

        with open(STREAMFLOW_ONLY) as inf:
            next(inf)
            date_q = []
            q_12189500 = []
            for line in inf:
                parts = line.split()
                if len(parts) > 1:
                    date_q.append(parts[0])
                    q_12189500.append(float(parts[2])/(3600*1))
                    
        os.chdir("..")
        logging.info("Removing copied directory %s", str(child_dir))
        remove_tree(child_dir)
        logging.info("Removed directory %s",  str(child_dir))

        simulation_streamflow = pd.DataFrame({'x[0]':date_q, 'x[2]':q_12189500})
        simulation_streamflow.columns = [header_name[0], header_name[2]]
        simulations = simulation_streamflow['12189500'].values
        return simulations
    
    def evaluation(self):
        return self.evals.tolist()
    
    def objectivefunction(self, simulation, evaluation, params=None):
        assert len(evaluation) == len(simulation), "Evaluation and simulation file are of different length, quitting now"
        try:
            model_fit = spotpy.objectivefunctions.nashsutcliffe(evaluation,simulation)
            logging.info('Nashsutcliffe: %s', str(model_fit))
        except Exception as e:
            logging.info('Exception occured: %s', str(e))
        return model_fit

#Function to write to DHSVM config file simulated inputs from DREAM.
def change_setting(config_file, setting_name, new_value, occurrence_loc='g'):
    sed_cmd = "sed -i 's:{setting_name} = .*:{setting_name} = {new_value}:{occurrence_loc}' {config_file}"
    sed_cmd = sed_cmd.format(setting_name = setting_name, new_value = new_value
                             , config_file = config_file
                             , occurrence_loc = occurrence_loc)
    return subprocess.call(sed_cmd, shell=True)

def plot_results(results, threshold=0.2):
    names = []
    values = []
    no_names = []
    no_values = []
    index = []
    no_index = []

    parnames = spotpy.analyser.get_parameternames(results)
    sensitivity_data = spotpy.analyser.get_sensitivity_of_fast(results,M=4)
    sensitivity_data = list(sensitivity_data.values())[1]
    
    with open('sensitivity_data_run_pnnlOct2005toSep2007.txt', 'w') as f:
        f.writelines([str(pname) + ", " + str(s) + "\n" for (pname, s) in zip(parnames, sensitivity_data)])

    for j in range(len(sensitivity_data)):
        if sensitivity_data[j] > threshold:
            names.append(parnames[j])
            values.append(sensitivity_data[j])
            index.append(j)
        else:
            no_names.append(parnames[j])
            no_values.append(sensitivity_data[j])
            no_index.append(j)

    fig = plt.figure(figsize=(16,6))
    ax = plt.subplot(1,1,1)
    ax.bar(index, values, align='center')
    ax.bar(no_index, no_values, color='orange', label = 'Insensitive parameter')

    ax.plot(np.arange(-1,len(parnames)+1,1),[threshold]*(len(parnames)+2),'r--')
    plt.xticks(list(range(len(sensitivity_data))), parnames,rotation = 15)
    plt.setp(ax.get_xticklabels(), fontsize=10)
    fig.savefig('FAST_sensitivity_run_pnnlOct2005toSep2007.png',dpi=300)

if __name__ == '__main__':
    # Initialize the Dream Class
    fast_run = fast_run_setup()
    #Files and their input paths
    NUM_OF_ITERATIONS = 1284
    DB_NAME = 'fast_dhsvm_pnnlOct2005toSep2007'
    CONFIG_FILE = 'Input.sauk.dynG.pnnl.Oct2005toSep2007'
    STREAMFLOW_ONLY = 'output/PNNLWRF/Streamflow.Only'
    VALIDATION_CSV = 'validation_1hr_Oct2005toSep2007.csv'
    DHSVM_CMD = '/home/ubuntu/DHSVM-PNNL/DHSVM/sourcecode/DHSVM3.1.3 ' + CONFIG_FILE 
    DIR_PREFIX = "dhsvm_run_pnnl_data_pid_"

    sampler=spotpy.algorithms.fast(fast_run, dbname= DB_NAME, dbformat='sql', parallel='mpc')
    sampler.sample(NUM_OF_ITERATIONS)
    results = sampler.getdata()
    plot_results(results)