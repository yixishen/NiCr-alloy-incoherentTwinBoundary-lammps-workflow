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
Cr_fraction = 0.3
## lattice constant
# Mishin NiCr #0.7  3.582   ## 0.8 3.559 ## 0.9 3.538  #1 3.52
# Bonny NiCr  #0.7  3.54855 ## 0.8 3.5391 ## 0.9 3.5296  #1 3.52

# Bonny NiFe #0.7 3.55578065   ## 0.8 3.545119517   ##0.9 3.533385033
# Beland NiFe #0.7 3.4946   ## 0.8 3.5   ##0.9 3.50793
latticeConst = 3.582

## potential energy
# Mishin NiCr #0.7  -4.358 ## 0.8 -4.4075 ## 0.9  -4.439  #1 -4.45
# bonny NiCr #0.7  -3.938566667 ## 0.8 -4.074283333 ## 0.9  -4.244136667  #1 -4.45

# Bonny NiFe #0.7 -4.343366042   ## 0.8 -4.381251667   ## -4.416488333
# Beland NiFe #0.7 -4.49956   ## 0.8 -4.49664   ## -4.47995

pEnergy =-4.358#    

component =  "NiCr"
potential_index = "MishinNiCr" #'NiCrMishin'
temp_name = "in.Step2_GridSearch_Mishin_template_NiCr"


cutOff =  [0.3, 1]   #A
# def motion   #lattice unit
disX = np.round(np.arange(0, 1.1, 0.1), 1).tolist()
disY = [0]
disZ = np.round(np.arange(0, 1.1, 0.1), 1).tolist()

'''
# 11 8 5
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
'''
# 1 1 2
#Grain1 orientation
x1 = [1,-1,0]
y1 = [1,1,2]
z1 = [-1,-1,1]

# Grain2 orientation
x2 =  [1, 0, 1] #[-1,1,0]  
y2 =  [-1, 2, 1] #[1,1,2]  
z2 =  [-1, -1, 1] #[1,1,-1]  


# 1 1 1
#Grain1 orientation
#x1 = [1,-1,0]
#y1 = [-1, -1, 1]
#z1 = [-1,-1,-2]

# Grain2 orientation
#x2 =  [1, 0, 1] #[-1,1,0]  
#y2 =  [-1, -1, 1] #[1,1,2]  
#z2 =  [1, -2, -1] #[1,1,-1]  

# Size
nx = 15
ny1 = 30   # 30 for grain 1 in center
ny2 = 20    # 20 for grain 1 in center
nz =  8    #  4 for mid; 8 for large

sim_type = 'Step2_GridSearch'
boundary_type =  'S3_112' #'MishinNiC8

Ni_fraction = str(1-Cr_fraction)
seed = [722302, 512342, 412352] # , 123542, 832145, 326645] #[722302, 512342, 412352]
pair_style = 'adp'
potential_name = 'CrNi.adp.Howells_Bonny.txt' #'CrNi.adp.Howells_Mishin.txt' 
potential_element = 'Cr Ni' # empty for eam potential

size = f"nz{nz}nx{nx}"
#size = f"nx{nx}"

#####################################
#---------- Directory---------------#
#####################################
base_dir = '/home/yixishen/DMREF/NiCr/MD/'  # cluster
templates_dir = base_dir + "templates/"  # direction for lammps input templates
simulation_dir = base_dir + f"/simulations/{sim_type}/{component}/{boundary_type}/{potential_index}/{Ni_fraction}/{size}/" 
potential_file = base_dir + f"potentials/{potential_name}"  # Path to your interatomic potential file
#oriFile_path = base_dir + "OriRef/"



#####################################
#---calculate lattice parameters----#
#####################################

xd1 = math.sqrt(sum(x**2 for x in x1))*latticeConst
yd1 = math.sqrt(sum(x**2 for x in y1))*latticeConst
zd1 = math.sqrt(sum(x**2 for x in z1))*latticeConst

xd2 = math.sqrt(sum(x**2 for x in x1))*latticeConst
yd2 = math.sqrt(sum(x**2 for x in y1))*latticeConst
zd2 = math.sqrt(sum(x**2 for x in z1))*latticeConst

xp0 = -nx * xd1
xp1 = nx * xd1

yp0 = -ny1 * yd1+0.005
yp1 = -ny2 * yd1+0.005

yp2 = -ny2 * yd1-0.005
yp3 = ny2 * yd1 + 0.005

yp4  = ny2 * yd1 - 0.005
yp5 = ny1 * yd2+0.01

zp0 = -nz * zd1
zp1 = nz * zd1

# simulation box size
yp00 = yp0 - 0.01
yp55 = yp5 + 0.01



moveAtoms = []
for i in disX:
    for j in disY:
        for k in disZ:
            moveAtoms.append([i,j,k])
 #lattice unit



# Read the LAMMPS template
with open(templates_dir + temp_name, "r") as template_file:
    lammps_template = template_file.read()
lammps_template = string.Template(lammps_template)

# Read the SLURM template
with open(templates_dir + "run.LAMMPS_GridSearch", "r") as slurm_file:
    slurm_template = slurm_file.read()
slurm_template = string.Template(slurm_template)

# Loop over parameters
for i in range(0,len(cutOff)):
    # three random model for each alloy
    for j in range(0, len(moveAtoms)): 
        for k in range(0, len(seed)): 
        
            # Create a unique directory for the simulation
            _cutOff = cutOff[i]
            _disX, _disY, _disZ = moveAtoms[j][:3]
            _disY1 = _disY*2

            _xx1,_xy1,_xz1 = x1[:3]
            _yx1,_yy1,_yz1 = y1[:3]
            _zx1,_zy1,_zz1 = z1[:3]

            _xx2,_xy2,_xz2 = x2[:3]
            _yx2,_yy2,_yz2 = y2[:3]
            _zx2,_zy2,_zz2 = z2[:3]

            _dis_inf = f'{_disX}_{_disY}_{_disZ}'
            sim_dir = os.path.join(simulation_dir, f"{k}/{_cutOff}_{_dis_inf}")
            _seed = seed[k]
            os.makedirs(sim_dir, exist_ok=True)

            # Generate LAMMPS input file
            lammps_input = lammps_template.safe_substitute({
                "latticeConst" : latticeConst,
            #lattice orientation
                "xp0": xp0, "xp1": xp1, 
                "yp0": yp0, "yp00": yp00,"yp1": yp1, "yp2": yp2, "yp3": yp3,  "yp4": yp4,  "yp5": yp5, "yp55": yp55, 
                "zp0": zp0, "zp1": zp1,
                "xx1": _xx1, "xy1": _xy1, "xz1": _xz1,  "yx1": _yx1, "yy1": _yy1, "yz1": _yz1, 
                "zx1": _zx1, "zy1": _zy1, "zz1": _zz1,
                "xx2": _xx2, "xy2": _xy2, "xz2": _xz2,  "yx2": _yx2, "yy2": _yy2, "yz2": _yz2, 
                "zx2": _zx2, "zy2": _zy2, "zz2": _zz2,
                "pair_style" : pair_style,
                "potential_file" : potential_file,
                "potential_element" : potential_element,
                "component" : component,
                "disX" : _disX,
                "disY0" : _disY,
                "disY1" : _disY1,
                "disZ" : _disZ,
                "cutOff" : _cutOff,
                "potential" : potential_index,
                "boundary_type" : boundary_type,
                "NiFrac" : Ni_fraction,
                "seed" : _seed,
                "pEnergy" : pEnergy

                })

            #lammps_input = lammps_input.replace("{", "${")
            with open(os.path.join(sim_dir, f"in.{sim_type}_{Ni_fraction}_{_disX}_{_disY}_{_disZ}"), "w") as f:
                f.write(lammps_input)

            # Write SLURM script
            slurm_script = slurm_template.safe_substitute({
                "Ni_fraction" : Ni_fraction,
                "inFile" : f"in.{sim_type}_{Ni_fraction}_{_disX}_{_disY}_{_disZ}",
                "component" : component,
                "cutOff" : _cutOff,
                "potential" : potential_index,
                "disX" : _disX,
                "disY" : _disY,
                "disZ" : _disZ
            })


            with open(os.path.join(sim_dir, "run.LAMMPS_ucsb"), "w") as f:
                f.write(slurm_script)

    # Copy the interatomic potential file to the simulation directory
    #shutil.copy(potential_file, sim_dir)

    # Submit the job
    #subprocess.run(["sbatch", os.path.join(sim_dir, "job.slurm")])
##


sim_type = 'GridSearch'
boundary_type =  'S3_112' #'MishinNiCr'
Ni_fraction = "1"
potential_tyep = 'eam'
potential_name = 'Ni_Foiles_1986.eam '