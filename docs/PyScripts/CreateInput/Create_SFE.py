#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 12:46:59 2025

write lammps input and slurm job script by python 
corresponding directory also created

@author: yixishen
"""

import os
import string
import shutil
import subprocess
import math
import numpy as np

# Define parameters for the loop
Cr_fraction = 0.1
## lattice constant
# Mishin #0.7  3.582  ## 0.8 3.559 ## 0.9 3.538  #1 3.52
# Bonny #0.7  3.54855  ## 0.8 3.5391 ## 0.9 3.5296  #1 3.52
latticeConst = 3.538 

## potential energy
# Mishin #0.7  -4.358 ## 0.8 -4.4075 ## 0.9  -4.439  #1 -4.45
# bonny #0.7  -3.938566667 ## 0.8 -4.074283333 ## 0.9  -4.244136667  #1 -4.45

  


sim_type = 'SFE'
component =  "NiCr"
seed = [722302, 512342, 412352]
Ni_fraction = str(1-Cr_fraction)
potential_index = "MishinNiCr" #'NiCrMishin'


#####################################
#---------- Directory---------------#
#####################################
base_dir = '/home/yixishen/DMREF/NiCr/MD/'  # cluster
templates_dir = base_dir + "templates/"  # direction for lammps input templates
simulation_dir = base_dir + f"/simulations/{sim_type}/{component}/{potential_index}/{Ni_fraction}//" 


# Read the LAMMPS template
with open(templates_dir + "in.SEF_Mishin_template", "r") as template_file:
    lammps_template = template_file.read()
lammps_template = string.Template(lammps_template)

# Read the SLURM template
with open(templates_dir + "run.LAMMPA_SFE", "r") as slurm_file:
    slurm_template = slurm_file.read()
slurm_template = string.Template(slurm_template)


for k in range(0, len(seed)): 
        
    sim_dir = os.path.join(simulation_dir, f"{k}")
    _seed = seed[k]
    os.makedirs(sim_dir, exist_ok=True)

    # Generate LAMMPS input file
    lammps_input = lammps_template.safe_substitute({
    "latticeConst" : latticeConst,
    "component" : component,
     "potential" : potential_index,
     "NiFrac" : Ni_fraction,
    "seed" : _seed,
                })

    #lammps_input = lammps_input.replace("{", "${")
    with open(os.path.join(sim_dir, f"in.SFE_{Ni_fraction}"), "w") as f:
        f.write(lammps_input)

    # Write SLURM script
    slurm_script = slurm_template.safe_substitute({
        "Ni_fraction" : Ni_fraction,
        "inFile" : f"in.SFE_{Ni_fraction}",
        "component" : component,
        "potential" : potential_index,
        })

    with open(os.path.join(sim_dir, "run.LAMMPS_ucsb"), "w") as f:
                f.write(slurm_script)

##
