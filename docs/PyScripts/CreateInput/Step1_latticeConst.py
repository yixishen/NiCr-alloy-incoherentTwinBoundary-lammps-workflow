#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:46:59 2025

write lammps input and slurm job script by python 
corresponding directory also created


@author: yixishen
"""

import os
import string
import shutil
import subprocess

# Define parameters for the loop
#temperatures = [1200, 1300, 1400]
temperatures = [800, 900, 1000, 1100, 1200, 1300, 1400]
seeds =  [412443, 723343, 643453]
sim_type = 'Step1_latticeConst'
potential_type = 'BelandFeNiCr' #'MishinNiCr'  #'BonnyFeNiCr' #
# sim_type_create_GB = 'createS3_112TB'
Ni_fraction = "0.9"
comp = "NiCr"
# eco_df = 0.025
# Paths

#base_dir = "/Users/yixishen/Desktop/Ni_BasedAlloy/NiCr/MD/" #local
base_dir = '/home/yixishen/DMREF/NiCr/MD/'  # cluster
templates_dir = base_dir + "templates/"  # direction for lammps input templates
simulation_dir = base_dir + f"/simulations/{sim_type}/{potential_type}//{comp}/{Ni_fraction}/" 
potential_file = base_dir + "potentials/FeNiCr_ArturV3.eam"  # Path to your interatomic potential file
#oriFile_path = base_dir + "OriRef/"

# Read the LAMMPS template
with open(templates_dir + "in.Step1_latticeConst_Beland_NiCr_temp", "r") as template_file:
    lammps_template = template_file.read()
lammps_template = string.Template(lammps_template)

# Read the SLURM template
with open(templates_dir + "run.LAMMPS_latConst", "r") as slurm_file:
    slurm_template = slurm_file.read()
slurm_template = string.Template(slurm_template)

# Loop over parameters
for i in range(0,len(temperatures)):
    # three random model for each alloy
    for j in range(0, len(seeds)): 
        
        # Create a unique directory for the simulation
        temp = temperatures[i]
        s = seeds[j]
        sim_dir = os.path.join(simulation_dir, f"{sim_type}_{temp}/{j}")
        os.makedirs(sim_dir, exist_ok=True)

        # Generate LAMMPS input file
        lammps_input = lammps_template.safe_substitute({
            "potential" : potential_file,
            "Tend" : temp,
            "seed" : s,
            "NiFrac": Ni_fraction,
            "modelNum":j
            })

        #lammps_input = lammps_input.replace("{", "${")
        with open(os.path.join(sim_dir, f"in.{sim_type}_{Ni_fraction}_{temp}K_{j}"), "w") as f:
            f.write(lammps_input)

        # Write SLURM script
        slurm_script = slurm_template.safe_substitute({
            "Ni_fraction" : Ni_fraction,
            "temp" : temp,
            "inFile" : f"in.{sim_type}_{Ni_fraction}_{temp}K_{j}",
            "modelNum":j
            })


        with open(os.path.join(sim_dir, "run.LAMMPS_ucsb"), "w") as f:
            f.write(slurm_script)


