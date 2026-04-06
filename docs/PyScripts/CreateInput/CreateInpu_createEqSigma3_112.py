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
# Define parameters for the loop
#0.7
lattice_constant = [3.57, 3.587, 3.592, 3.596, 3.612,  3.622, 3.628, 3.63961, 3.6457, 3.6524, 3.659] # mishin potential


# Ni
#lattice_constant = [3.5213, 3.523, 3.5254, 3.531, 3.5376, 3.5446, 3.5524, 3.5708] # mishin potential

temperatures = [50, 100, 200, 300, 600, 800, 1000, 1100, 1200, 1300, 1400]

#steps = [ 300000,300000, 300000, 300000, 400000, 400000,400000,400000]

seeds =  [513243, 1042391, 4234534]
potential_type =  'MishinNiCr'  #"NiFoiles1986"
sim_type = 'ECOS3_112'
sim_type_create_GB = 'createS3_112'
Ni_fraction = 0.7
eco_df = 0.05
Tstep = [ 5, 10, 20, 30, 60, 80, 100, 110, 120, 130, 140]
seeds = [23453, 74536, 45645]
TB_type = 'S3_112'
sim_type = 'createS3_112'
lammps_ele = 'Cr Ni'
lammps_potential_com = 'eam/alloy'


# /home/yixishen/DMREF/NiCr/MD/simulations/GB_energy/Ni_112_Fischer_CuNi2018/1
# Paths
#base_dir = "/Users/yixishen/Desktop/Ni_BasedAlloy/NiCr/MD/" #local
base_dir = '/home/yixishen/DMREF/NiCr/MD/'  # cluster
templates_dir = base_dir + "templates/"  # direction for lammps input templates
simulation_dir = base_dir + f"/simulations/step1_Create{TB_type}/{potential_type}/{Ni_fraction}/" 

potential_file = base_dir + "potentials/CuNi_Fischer_2018.eam.alloy"  # Path to your interatomic potential file
oriFile_path = base_dir + f"OriRef/{potential_type}/{Ni_fraction}/"

# Read the LAMMPS template
with open(templates_dir + "in.EqSigma3_112TB_templates", "r") as template_file:
    lammps_template = template_file.read()
lammps_template = string.Template(lammps_template)

# Read the SLURM template
with open(templates_dir + "run.LAMMPS_ucsb", "r") as slurm_file:
    slurm_template = slurm_file.read()
slurm_template = string.Template(slurm_template)

# Loop over parameters
for i in range(0,len(lattice_constant)):
    # three random model for each alloy
    for j in range(0, len(seeds)): 
        
        # Create a unique directory for the simulation
        lc = lattice_constant[i]
        cut_off = round(1.1 * lc,4) # cutoff distance is 1.1 of lattice constant
        temp = temperatures[i]
        s = seeds[j]
        tstep = Tstep[i]
        #total_steps = steps[i]
        sim_dir = os.path.join(simulation_dir, f"{sim_type}_{temp}/{j}")
        os.makedirs(sim_dir, exist_ok=True)
        oriFile = oriFile_path + f"sigma3_1185Ni{Ni_fraction}_{temp}K.ori"
        # Generate LAMMPS input file
        lammps_input = lammps_template.safe_substitute({
            "a" : lc,
            "cut_off":cut_off,
            "potential" : potential_file,
            "Tend" : temp,
            "Tstep": tstep,
            "seed" : s,
            "NiFrac": Ni_fraction,
            "modelNum":j,
            "eco_df":eco_df,
            #"restart_file":restart_file,
            "oriFile":oriFile,
            #"total_steps":total_steps,
            "lammps_ele" : lammps_ele,
            "lammps_potential_com" : lammps_potential_com

            })

        #lammps_input = lammps_input.replace("{", "${")
        with open(os.path.join(sim_dir, f"in.{sim_type}_{eco_df}_{Ni_fraction}_{temp}K_{j}"), "w") as f:
            f.write(lammps_input)

        # Write SLURM script
        slurm_script = slurm_template.safe_substitute({
            "Ni_fraction" : Ni_fraction,
            "sim_type": sim_type,
            "temp" : temp,
            "j" : j,
            "Tend" : temp,
            "seed" : s,
            "NiFrac": Ni_fraction,
            "eco_df":eco_df
            })


        with open(os.path.join(sim_dir, "run.LAMMPS_ucsb"), "w") as f:
            f.write(slurm_script)

    # Copy the interatomic potential file to the simulation directory
    #shutil.copy(potential_file, sim_dir)

    # Submit the job
    #subprocess.run(["sbatch", os.path.join(sim_dir, "job.slurm")])
