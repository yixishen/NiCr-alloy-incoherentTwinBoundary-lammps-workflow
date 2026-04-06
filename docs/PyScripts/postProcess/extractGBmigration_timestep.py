#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 15:50:43 2024

@author: yixishen
"""

import logging
import time
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import os
from itertools import product

def parse_lammps_dump(filename):
    """
    Generator that reads the LAMMPS dump file and yields a dictionary with:
      'timestep': int
      'natoms': int
      'box': np.array of shape (3, 2) for the box bounds
      'columns': list of atom property columns
      'atoms': pd.DataFrame of atom data
    """
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.strip() != "ITEM: TIMESTEP":
                continue
            
            # Timestep
            timestep = int(f.readline().strip())
            
            # Number of atoms
            line = f.readline()  # ITEM: NUMBER OF ATOMS
            natoms = int(f.readline().strip())
            
            # Box bounds
            line = f.readline()  # ITEM: BOX BOUNDS ...
            box_bounds = []
            for _ in range(3):
                bounds_line = f.readline().strip().split()
                box_bounds.append(list(map(float, bounds_line)))
            box_bounds = np.array(box_bounds)
            
            # Atoms header
            atom_header = f.readline().strip().split()
            columns = atom_header[2:]  # after "ITEM: ATOMS"
            
            # Atom data
            atom_data = []
            for _ in range(natoms):
                vals = list(map(float, f.readline().split()))
                atom_data.append(vals)
            df = pd.DataFrame(atom_data, columns=columns)
            
            yield {
                'timestep': timestep,
                'natoms': natoms,
                'box': box_bounds,
                'columns': columns,
                'atoms': df
            }

def identify_two_gbs(df, f_gb2_max=0.2):
    """
    Identify the two distinct GB groups from a DataFrame of atoms.
    Criteria for GB atoms: -f_gb2_max <= f_gb[2] <= f_gb2_max
    Return:
      gb1, gb2: DataFrames of the two GB groups or (None, None) if not found.
    """
    gb_atoms = df[(df['f_gb[2]'] <= f_gb2_max) & (df['f_gb[2]'] >= -f_gb2_max)]
    
    if len(gb_atoms) == 0:
        return None, None
    
    # Extract Y positions
    y_positions = gb_atoms[['y']].values

    # Use KMeans with 2 clusters (if there's a chance only one cluster exists, handle that)
    # If gb_atoms < 2, KMeans can fail. Check that:
    if len(gb_atoms) < 2:
        # Not enough atoms to form two groups
        return None, None

    kmeans = KMeans(n_clusters=2, random_state=0)
    labels = kmeans.fit_predict(y_positions)
    
    gb1 = gb_atoms[labels == 0]
    gb2 = gb_atoms[labels == 1]
    
    # Ensure gb1 is the one with smaller average y
    if gb1['y'].mean() > gb2['y'].mean():
        gb1, gb2 = gb2, gb1
    
    return gb1, gb2

def write_gb_dump(input_file, output_file, f_gb2_max=0.2):
    """
    Writes a new LAMMPS-style dump file containing only the GB atoms.
    Adds a new column 'gb_group' to distinguish the two GB groups.
    """
    with open(output_file, 'w') as out:
        for data in parse_lammps_dump(input_file):
            timestep = data['timestep']
            box = data['box']
            columns = data['columns']
            df = data['atoms']
            
            # Identify GB atoms
            gb1, gb2 = identify_two_gbs(df, f_gb2_max=f_gb2_max)
            
            # If we have no GBs, we can either skip writing this timestep or write zero atoms.
            if gb1 is None or gb2 is None:
                # Write timestep with zero atoms or skip entirely?
                # Let's write a block with zero atoms for completeness.
                out.write("ITEM: TIMESTEP\n")
                out.write(f"{timestep}\n")
                out.write("ITEM: NUMBER OF ATOMS\n0\n")
                out.write("ITEM: BOX BOUNDS pp pp pp\n")
                for (lo, hi) in box:
                    out.write(f"{lo} {hi}\n")
                out.write("ITEM: ATOMS " + " ".join(columns) + " gb_group\n")
                # no atoms to write
                continue
            
            # Combine GB atoms and assign gb_group
            gb1 = gb1.copy()
            gb2 = gb2.copy()
            gb1['gb_group'] = 1
            gb2['gb_group'] = 2
            gb_atoms = pd.concat([gb1, gb2], ignore_index=True)
            
            # Write the timestep block
            out.write("ITEM: TIMESTEP\n")
            out.write(f"{timestep}\n")
            out.write("ITEM: NUMBER OF ATOMS\n")
            out.write(f"{len(gb_atoms)}\n")
            out.write("ITEM: BOX BOUNDS pp pp pp\n")
            for (lo, hi) in box:
                out.write(f"{lo} {hi}\n")
            
            # Append gb_group to columns list for writing
            out.write("ITEM: ATOMS " + " ".join(columns) + " gb_group\n")
            
            # Write only GB atoms
            # Ensuring we print in the correct order of columns plus gb_group
            write_cols = columns + ['gb_group']
            for _, row in gb_atoms.iterrows():
                out.write(" ".join(map(str, row[write_cols].values)) + "\n")

'''
def compute_gb_positions(input_file, f_gb2_max=0.2):
    """
    Parses the input dump file and computes the average y-position of both GBs at each timestep.
    Returns a DataFrame with columns: ['timestep', 'gb1_y', 'gb2_y'].
    """
    results = []
    for data in parse_lammps_dump(input_file):
        timestep = data['timestep']
        df = data['atoms']
        gb1, gb2 = identify_two_gbs(df, f_gb2_max=f_gb2_max)
        
        if gb1 is not None and gb2 is not None:
            avg_y_gb1 = gb1['y'].mean()
            avg_y_gb2 = gb2['y'].mean()
        else:
            avg_y_gb1 = np.nan
            avg_y_gb2 = np.nan
        
        results.append([timestep, avg_y_gb1, avg_y_gb2])
    
    return pd.DataFrame(results, columns=['timestep', 'gb1_y', 'gb2_y'])
'''
def compute_gb_positions(input_file, f_gb2_max=0.2):
    """
    Parses the input dump file and computes the average y-position of both GBs at each timestep.
    Also computes the migration distance relative to the first timestep for each GB.
    Returns a DataFrame with columns: ['timestep', 'gb1_y', 'gb2_y', 'gb1_distance', 'gb2_distance'].
    """
    results = []
    initial_gb1_y = None
    initial_gb2_y = None

    for data in parse_lammps_dump(input_file):
        timestep = data['timestep']
        df = data['atoms']
        gb1, gb2 = identify_two_gbs(df, f_gb2_max=f_gb2_max)
        
        if gb1 is not None and gb2 is not None:
            avg_y_gb1 = gb1['y'].mean()
            avg_y_gb2 = gb2['y'].mean()
        else:
            avg_y_gb1 = np.nan
            avg_y_gb2 = np.nan
        
        # Store initial positions if this is the first timestep with valid data
        if initial_gb1_y is None and not np.isnan(avg_y_gb1):
            initial_gb1_y = avg_y_gb1
        if initial_gb2_y is None and not np.isnan(avg_y_gb2):
            initial_gb2_y = avg_y_gb2

        results.append([timestep, avg_y_gb1, avg_y_gb2])
    
    # Convert to DataFrame
    df_positions = pd.DataFrame(results, columns=['timestep', 'gb1_y', 'gb2_y'])
    
    # If initial positions were found, compute distances
    # Distance is defined as the difference from the initial position.
    if initial_gb1_y is not None:
        df_positions['gb1_distance'] = df_positions['gb1_y'] - initial_gb1_y
    else:
        # If no initial found (no valid GB in the first steps), set distances to NaN
        df_positions['gb1_distance'] = np.nan

    if initial_gb2_y is not None:
        df_positions['gb2_distance'] = df_positions['gb2_y'] - initial_gb2_y
    else:
        df_positions['gb2_distance'] = np.nan

    return df_positions

# Configure logging to write to a file
logging.basicConfig(
    filename="output.log",  # Log file name
    level=logging.INFO,  # Log level
    format="%(asctime)s - %(levelname)s - %(message)s"
)


if __name__ == "__main__":
    logging.info("Starting job...")
    time.sleep(5)  # Simulate work
    logging.info("Job completed.")
    ECO_DF = [0.01]
    temp = ['600', '800']
    sub_path = ['0', '1', '2']
    potential = 'MishinNiCr'
    Ni_fraction = [0.7]
    size = ['nz8']
    composition = ['0', '1', '2']
    
    path = '/home/yixishen/DMREF/NiCr/MD/simulations/Step4_ECO_112/'
    path_out = '/home/yixishen/DMREF/NiCr/MD/PyScripts/postProcess/Step4_ECO_112/'



missing_log = 'missing_files_log_MishinNi.txt'

with open(missing_log, 'w') as log_file:
    for temp_i, sub_i, _ECO_DF ,_size, _comp, _Ni_frac in product(temp, sub_path, ECO_DF, size, composition, Ni_fraction):
        folder = f'{potential}/{_Ni_frac}/{_ECO_DF}/{_size}/comp{_comp}/Step4_ECOS3_112_{_ECO_DF}_{temp_i}/{sub_i}/'
        path_lmp = path + folder
        path_gb_out = path_out + folder

        file_to_check = os.path.join(path_lmp, f'dump.ECODF_{temp_i}')  # <-- Change to your actual filename

        if not os.path.exists(file_to_check):
            log_file.write(f'File not found: {file_to_check}\n')
            continue
        
        os.makedirs(path_gb_out, exist_ok=True)

        input_file = file_to_check  # Replace with your input file
        output_file = os.path.join(path_gb_out, f'dump_gb_only_{sub_i}') # The new dump file containing only GB atoms
                    
        write_gb_dump(input_file, output_file, f_gb2_max=0.2)
    
        df_positions = compute_gb_positions(input_file, f_gb2_max=0.2)
        df_positions.to_csv( path_gb_out + "gb_positions_and_distances.csv", index=False)
        df_positions.to_excel(path_gb_out + "gb_positions_and_distances.xlsx", 
                              sheet_name="gb_positions_and_distances", index=False)

        log_file.write(f'GB extration Done: {file_to_check}\n')




'''
    for temp_i in temp:
        for sub_i in sub_path:
            for _size in size:
                for _comp in composition:
                    for _Ni_frac in Ni_fraction:
                    path_lmp = path + f'{potential}/{_Ni_frac}/{ECO_DF}/{_size}/comp{_comp}/Step4_ECOS3_112_{ECO_DF}_{temp_i}/{sub_i}/'
                    path_gb_out = path_out + f'{potential}/{_Ni_frac}/{ECO_DF}/{_size}/comp{_comp}/Step4_ECOS3_112_{ECO_DF}_{temp_i}/{sub_i}/'

                    os.makedirs(path_gb_out, exist_ok=True)

                    input_file = path_lmp + f'dump.ECODF_{temp_i}'  # Replace with your input file
                    output_file = path_gb_out + "dump_gb_only" + '_' + sub_i # The new dump file containing only GB atoms
                    
                    write_gb_dump(input_file, output_file, f_gb2_max=0.2)
                    print("GB-only dump file written to:", output_file)
    
                    df_positions = compute_gb_positions(input_file, f_gb2_max=0.2)
                    df_positions.to_csv( path_gb_out + "gb_positions_and_distances.csv", index=False)
                    df_positions.to_excel(path_gb_out + "gb_positions_and_distances.xlsx", sheet_name="gb_positions_and_distances", index=False)

'''