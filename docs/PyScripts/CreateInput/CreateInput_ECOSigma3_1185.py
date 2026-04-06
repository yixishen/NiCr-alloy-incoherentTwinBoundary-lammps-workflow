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
#lattice_constant = [3.587, 3.592, 3.596, 3.601, 3.606, 3.612, 3.617,
#                     3.622, 3.628, 3.634, 3.646, 3.659] # mishin potential


# Ni
lattice_constant = [3.5213, 3.523, 3.5254, 3.531, 3.5376, 3.5446, 3.5524, 3.5708] # mishin potential

temperatures = [50, 100, 200, 300, 600, 800, 1000, 1400]

steps = [ 600000,600000, 600000, 600000, 400000, 400000,400000,400000]

seeds =  [0, 1, 2]
potential_type = 'FischerNiCu'
sim_type = 'ECOS3_1185TB'
sim_type_create_GB = 'createS3_1185'
Ni_fraction = 1
eco_df = 0.025
# Paths

#base_dir = "/Users/yixishen/Desktop/Ni_BasedAlloy/NiCr/MD/" #local
base_dir = '/home/yixishen/DMREF/NiCr/MD/'  # cluster
templates_dir = base_dir + "templates/"  # direction for lammps input templates
simulation_dir = base_dir + f"/simulations/ECO_1185/{potential_type}/{Ni_fraction}/{eco_df}/" 
restart_dir = base_dir + f"/simulations/step1_CreateS3_1185/{potential_type}/{Ni_fraction}/" 
potential_file = base_dir + "potentials/CuNi_Fischer_2018.eam.alloy"  # Path to your interatomic potential file
#potential_file_cluster = base_dir_cluster + "potentials/CrNi.adp.Howells_Mishin.txt"
oriFile_path = base_dir + f"OriRef/{potential_type}/{Ni_fraction}/"

# Read the LAMMPS template
with open(templates_dir + "in.ECO_1185_templates", "r") as template_file:
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
        total_steps = steps[i]
        sim_dir = os.path.join(simulation_dir, f"{sim_type}_{eco_df}_{temp}/{j}")
        os.makedirs(sim_dir, exist_ok=True)
        restart_path = os.path.join(restart_dir, f"{sim_type_create_GB}_{temp}/{j}")
        restart_file = restart_path + f"/restart.Ni_{Ni_fraction}_sig3_1185_{temp}K"
        oriFile = oriFile_path + f"sigma3_1185Ni{Ni_fraction}_{temp}K.ori"
        # Generate LAMMPS input file
        lammps_input = lammps_template.safe_substitute({
            "a" : lc,
            "cut_off":cut_off,
            "potential" : potential_file,
            "Tend" : temp,
            "seed" : s,
            "NiFrac": Ni_fraction,
            "modelNum":j,
            "eco_df":eco_df,
            "restart_file":restart_file,
            "oriFile":oriFile,
            "total_steps":total_steps
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
