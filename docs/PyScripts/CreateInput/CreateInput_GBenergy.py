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
import math

# Define parameters for the loop

latticeConst = 3.52
pEnergy = -4.45
cutOff =  [1.5]
moveAtoms = [[0.7,0,0]]

#Grain1 orientation
x1 = [1,-2,1]
y1 = [11,8,5]
z1 = [-3,1,5]

# Grain2 orientation
x2 = [2,-1,-1]
y2 = [8,11,5]
z2 = [1,-3,5]

# Size
nx = 4
ny = 2
nz = 4

sim_type = 'GB_energy'
boundary_type =  'Ni_1185_FoilesNi' #'MishinNiCr'
Ni_fraction = "1"
potential_tyep = 'eam'
potential_name = 'Ni_Foiles_1986.eam '

#####################################
#---------- Directory---------------#
#####################################
base_dir = '/home/yixishen/DMREF/NiCr/MD/'  # cluster
templates_dir = base_dir + "templates/"  # direction for lammps input templates
simulation_dir = base_dir + f"/simulations/{sim_type}/{boundary_type}/{Ni_fraction}/" 
potential_file = base_dir + f"potentials/{potential_name}"  # Path to your interatomic potential file
#oriFile_path = base_dir + "OriRef/"



#####################################
#---calculate lattice parameters----#
#####################################

xd1 = math.sqrt(sum(x**2 for x in x1))
yd1 = math.sqrt(sum(x**2 for x in y1))
zd1 = math.sqrt(sum(x**2 for x in z1))

xd2 = math.sqrt(sum(x**2 for x in x1))
yd2 = math.sqrt(sum(x**2 for x in y1))
zd2 = math.sqrt(sum(x**2 for x in z1))

xp0 = 0.0
xp1 = nx * xd1

yp0 = -ny * yd1
yp0 = ny * yd2

zp0 = 0.0
zp1 = nz * zd1

# Read the LAMMPS template
with open(templates_dir + "in.latticeConst_Ni_temp", "r") as template_file:
    lammps_template = template_file.read()
lammps_template = string.Template(lammps_template)

# Read the SLURM template
with open(templates_dir + "run.LAMMPS_latConst", "r") as slurm_file:
    slurm_template = slurm_file.read()
slurm_template = string.Template(slurm_template)

# Loop over parameters
for i in range(0,len(cutOff)):
    # three random model for each alloy
    for j in range(0, len(moveAtoms)): 
        
        # Create a unique directory for the simulation
        _cutOff = cutOff[i]
        _disX, _disY, _disZ = moveAtoms[j][:3]

        _xx1,_xy1,_xz1 = x1[:3]
        _yx1,_yy1,_yz1 = y1[:3]
        _zx1,_zy1,_zz1 = z1[:3]

        _xx2,_xy2,_xz2 = x2[:3]
        _yx2,_yy2,_yz2 = y2[:3]
        _zx2,_zy2,_zz2 = z2[:3]

        _dis_inf = f'{_disX}_{_disY}_{_disZ}'
        sim_dir = os.path.join(simulation_dir, f"{_cutOff}/{_dis_inf}")
        os.makedirs(sim_dir, exist_ok=True)

        # Generate LAMMPS input file
        lammps_input = lammps_template.safe_substitute({
            "latticeConst" : latticeConst,
            #lattice orientation
            "xp0": xp0, "xp1": xp1, "yp0": yp0, "yp1": yp1, "zp0": zp0, "zp1": zp1,
            "xx1": _xx1, "xy1": _xy1, "xz1": _xz1,  "yx1": _yx1, "yy1": _yy1, "yz1": _yz1, 
            "zx1": _zx1, "zy1": _zy1, "zz1": _zz1,
            "xx2": _xx2, "xy2": _xy2, "xz2": _xz2,  "yx2": _yx2, "yy2": _yy2, "yz2": _yz2, 
            "zx2": _zx2, "zy2": _zy2, "zz2": _zz2,
            "potential_tyep" : potential_tyep,
            "potential_file" : potential_file,
            
            "disX" : _disX,
            "disY" : _disY,
            "disZ" : _disZ,
            "cutOff" : _cutOff,
            
            "boundary_type" : boundary_type,
            "pEnergy" : pEnergy

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

    # Copy the interatomic potential file to the simulation directory
    #shutil.copy(potential_file, sim_dir)

    # Submit the job
    #subprocess.run(["sbatch", os.path.join(sim_dir, "job.slurm")])
##
