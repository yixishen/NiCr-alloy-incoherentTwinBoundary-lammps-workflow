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

#temperatures = [300, 600, 800, 1000, 1100, 1200, 1300, 1400]
#Tstep = [30, 60, 80, 100, 110, 120, 130, 140]

temperatures = [600, 800, 1000, 1100, 1200, 1300, 1400]
Tstep = [60, 80, 100, 110, 120, 130, 140]

seeds =  [513243, 142391, 824534]
potential_type = 'MishinNiCr'

Comp = "NiCr"
Ni_fraction = 0.8

run_time = "20"    # simnulation request time hrs
sim_type = 'Step3_EqSigma3'
lammps_ele = 'Cr Ni'
lammps_potential_com = 'adp'
size = ['nz12']
comp_index = [0, 1, 2] # want to know how component configuration influence mobility

# /home/yixishen/DMREF/NiCr/MD/simulations/GB_energy/Ni_112_Fischer_CuNi2018/1
# Paths
#base_dir = "/Users/yixishen/Desktop/Ni_BasedAlloy/NiCr/MD/" #local
base_dir = '/home/yixishen/DMREF/NiCr/MD/'  # cluster
templates_dir = base_dir + "templates/"  # direction for lammps input templates
simulation_dir = base_dir + f"/simulations/Step3_EqSigma3_112/{potential_type}/{Ni_fraction}/" 
potential_file = base_dir + "potentials/CrNi.adp.Howells_Mishin.txt"  # Path to your interatomic potential file
oriFile_path = base_dir + f"OriRef/{potential_type}/{Ni_fraction}/"

# Read the LAMMPS template
with open(templates_dir + "in.Step3_EqSigma3_112TB_Mishin_templates", "r") as template_file:
    lammps_template = template_file.read()
lammps_template = string.Template(lammps_template)

# Read the SLURM template
with open(templates_dir + "run.LAMMPS_Step3_Eq112", "r") as slurm_file:
    slurm_template = slurm_file.read()
slurm_template = string.Template(slurm_template)

# Loop over parameters
for _size in size:
    for k in comp_index:
        for i in range(0,len(temperatures)):
            # three random model for each alloy
            for j in range(0, len(seeds)): 
        
                temp = temperatures[i]
                s = seeds[j]
                tstep = Tstep[i]
                sim_dir = os.path.join(simulation_dir, f"{_size}/comp{k}/{sim_type}_{temp}/{j}")
                os.makedirs(sim_dir, exist_ok=True)
                oriFile = oriFile_path + f"sigma3_112Ni{Ni_fraction}_{temp}K.ori"
                restart_file = base_dir + f"/simulations/Step2_GridSearch/{Comp}/S3_112/{potential_type}/{Ni_fraction}/restart.al_S3_112_{Comp}_{_size}_comp{k}"
                lammps_input = lammps_template.safe_substitute({
                    "Comp":Comp,
                    "comp_index" : k,
                    "size":_size,
                    "potential" : potential_file,
                    "Tend" : temp,
                    "Tstep": tstep,
                    "seed" : s,
                    "NiFrac": Ni_fraction,
                    "modelNum":j,
                    "restart_file":restart_file,
                    "oriFile":oriFile,
                    "lammps_ele" : lammps_ele,
                    "lammps_potential_com" : lammps_potential_com
                    })

                #lammps_input = lammps_input.replace("{", "${")
                with open(os.path.join(sim_dir, f"in.{sim_type}_{Ni_fraction}_{temp}K_{j}"), "w") as f:
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
                    "run_time" : run_time,
                    "Comp" : Comp
                    })


                with open(os.path.join(sim_dir, "run.LAMMPS_ucsb"), "w") as f:
                    f.write(slurm_script)

