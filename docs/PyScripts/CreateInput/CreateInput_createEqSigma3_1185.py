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

# 0.7 
#lattice_constant = [3.587, 3.592, 3.596, 3.601, 3.606, 3.612, 3.617,
                     #3.622, 3.628, 3.634, 3.646, 3.659] # mishin potential

# Ni
#lattice_constant = [3.5213, 3.523, 3.5254, 3.531, 3.5376, 3.5446, 3.5524, 3.5708] # mishin potential

lattice_constant = [3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52]
temperatures = [50, 100, 200, 300, 600, 800, 1000, 1400]
steps = [ 600000,600000, 600000, 600000, 400000, 400000,400000,400000]


Tstep = [ 5, 10, 20, 30, 60, 80, 100, 140]


seeds = [23453, 74536, 45645]
TB_type = 'S3_1185'
sim_type = 'createS3_1185_narrow'
Ni_fraction = 1
potential_type = 'FoilesNi'

# Paths

#base_dir = "/Users/yixishen/Desktop/Ni_BasedAlloy/NiCr/MD/" #local
base_dir = '/home/yixishen/DMREF/NiCr/MD/'  # cluster
base_dir_cluster = '/home/yixishen/DMREF/NiCr/MD/'  # cluster
templates_dir = base_dir + "templates/"  # direction for lammps input templates
simulation_dir = base_dir + f"/simulations/step1_Create{TB_type}/{potential_type}/{Ni_fraction}/" 
potential_file = base_dir + "potentials/CrNi.adp.Howells_Mishin.txt"  # Path to your interatomic potential file
potential_file_cluster = base_dir_cluster + "potentials/Ni_Foiles_1986.eam"
lammps_potential_com = 'eam'
lammps_ele = ''

# Read the LAMMPS template
with open(templates_dir + "in.createSigma3_1185TB_templates", "r") as template_file:
    lammps_template = template_file.read()
lammps_template = string.Template(lammps_template)

# Read the SLURM template
with open(templates_dir + "run.LAMMPS_createSigma3", "r") as slurm_file:
    slurm_template = slurm_file.read()
slurm_template = string.Template(slurm_template)

# Loop over parameters
for i in range(0,len(temperatures)):
    # three random model for each alloy
    for j in range(0, len(seeds)): 
        
        # Create a unique directory for the simulation
        total_steps = steps[i]
        temp = temperatures[i]
        lc = lattice_constant[i]
        tstep = Tstep[i]
        s = seeds[j]
        sim_dir = os.path.join(simulation_dir, f"{sim_type}_{temp}/{j}")
        os.makedirs(sim_dir, exist_ok=True)

        # Generate LAMMPS input file
        lammps_input = lammps_template.safe_substitute({
            "a" : lc,
            "run_steps" : 10000,
            "potential" : potential_file_cluster,
            'lammps_potential_com' : lammps_potential_com,
            'lammps_ele' : lammps_ele,
            "Tend" : temp,
            "Tstep": tstep,
            "seed" : s,
            "NiFrac": Ni_fraction,
            "modelNum":j,
            "total_steps":total_steps
            })

        #lammps_input = lammps_input.replace("{", "${")
        with open(os.path.join(sim_dir, f"in.lammps_{Ni_fraction}_{temp}K_{j}"), "w") as f:
            f.write(lammps_input)

        # Write SLURM script
        slurm_script = slurm_template.safe_substitute({
            "Ni_fraction" : Ni_fraction,
            "temp" : temp,
            "j" : j,
            "Tend" : temp,
            "seed" : s,
            "NiFrac": Ni_fraction
            })


        with open(os.path.join(sim_dir, "run.LAMMPS_ucsb"), "w") as f:
            f.write(slurm_script)

    # Copy the interatomic potential file to the simulation directory
    #shutil.copy(potential_file, sim_dir)

    # Submit the job
    #subprocess.run(["sbatch", os.path.join(sim_dir, "job.slurm")])
