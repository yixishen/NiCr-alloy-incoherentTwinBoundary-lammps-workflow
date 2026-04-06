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
#0.7 Mishin NiCr 800-1400
lattice_constant = [ 3.611518, 3.6222298] 

# 0.8
#lattice_constant = [ 3.605387333, 3.616631667, 3.629128333] 

# 0.9
#lattice_constant = [ 3.5765582, 3.5866016, 3.5978786] 


#
#lattice_constant = [3.5213, 3.523, 3.5254, 3.531, 3.5376, 3.5446, 3.5524, 3.5708] # mishin potential

# 0.9
#lattice_constant = [3.5592, 3.5675, 3.5766, 3.5816, 3.5866,  3.5923, 3.5979 ] # mishin potential
#temperatures = [600, 800, 1000, 1100, 1200, 1300, 1400]  # sigma3 {112} has lower mobility

#1
#lattice_constant = [3.5213, 3.523, 3.5254, 3.531, 3.5376, 3.5446, 3.5524, 3.5708]
temperatures =     [600, 800]  # sigma3 {112} has lower mobility
steps = [300000, 300000]

##Bonny NiCr

#lattice_constant = [3.5577, 3.5679, 3.5737, 3.5794, 3.5859, 3.5923 ] #0.9
#lattice_constant = [3.5669, 3.5768, 3.5824, 3.5881, 3.5943, 3.6006 ] #0.8
#lattice_constant = [3.5756, 3.5851, 3.5905, 3.5957, 3.6018, 3.6078 ] #0.7
#temperatures = [800, 1000, 1100, 1200, 1300, 1400]  # sigma3 {112} has lower mobility
#steps = [150000, 100000, 100000,100000,100000,100000]
run_time = 60


seeds =  [0,1,2]
comp_index = [0,1,2]
size = ['nz8']
potential_type = 'MishinNiCr' # 'NiFoiles1986'
sim_type = 'Step4_ECOS3_112'
sim_type_create_GB = 'Step3_EqSigma3'  # for read restart
Comp = "NiCr"
Ni_fraction = 0.7
eco_df = 0.01
pair_style = 'adp'
component = 'Cr Ni' # empty for eam
# Paths

#base_dir = "/Users/yixishen/Desktop/Ni_BasedAlloy/NiCr/MD/" #local
base_dir = '/home/yixishen/DMREF/NiCr/MD/'  # cluster
templates_dir = base_dir + "templates/"  # direction for lammps input templates
simulation_dir = base_dir + f"/simulations/Step4_ECO_112/{potential_type}/{Ni_fraction}/{eco_df}/" 
restart_dir = base_dir + f"/simulations/Step3_EqSigma3_112/{potential_type}/{Ni_fraction}/" 
#potential_file = base_dir + "potentials/Ni_Foiles_1986.eam"  # Path to your interatomic potential file
potential_file = base_dir + "potentials/CrNi.adp.Howells_Mishin.txt"
oriFile_path = base_dir + f"OriRef/{potential_type}/"

# Read the LAMMPS template
with open(templates_dir + "in.Step4_ECO_Mishin_templates", "r") as template_file:
    lammps_template = template_file.read()
lammps_template = string.Template(lammps_template)

# Read the SLURM template
with open(templates_dir + "run.LAMMPS_ucsb", "r") as slurm_file:
    slurm_template = slurm_file.read()
slurm_template = string.Template(slurm_template)

# Loop over parameters
for _size in size:
    for i in range(0,len(lattice_constant)):
        # three random model for each alloy
        for j in range(0, len(seeds)): 
            for k in comp_index:
                # Create a unique directory for the simulation
                lc = lattice_constant[i]
                cut_off = round(1.1 * lc,4) # cutoff distance is 1.1 of lattice constant
                temp = temperatures[i]
                s = seeds[j]
                total_steps = steps[i]
                sim_dir = os.path.join(simulation_dir, f"{_size}/comp{k}/{sim_type}_{eco_df}_{temp}/{j}")
                os.makedirs(sim_dir, exist_ok=True)
                restart_path = os.path.join(restart_dir, f"{_size}/comp{k}/{sim_type_create_GB}_{temp}/{j}")
                restart_file = restart_path + f"/restart.{Comp}_{Ni_fraction}_sig3_112_{_size}_comp{k}_{temp}K"
                oriFile = oriFile_path + f"{Ni_fraction}/sigma3_112{Comp}{Ni_fraction}_{temp}K.ori"
                # Generate LAMMPS input file
                lammps_input = lammps_template.safe_substitute({
                    "a" : lc,
                    "cut_off":cut_off,
                    "potential_file" : potential_file,
                    "pair_style" : pair_style,
                    "component" : component,
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
                    "eco_df":eco_df,
                    "run_time" : run_time
                    })
   
  
                with open(os.path.join(sim_dir, "run.LAMMPS_ucsb"), "w") as f:
                    f.write(slurm_script)



                