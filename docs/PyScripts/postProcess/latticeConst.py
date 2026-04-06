##
import os
import csv
import numpy as np

def extract_lattice_constants(base_path, temps, output_csv, modelSize):
    """
    Search in base_path/ for directories named, e.g., latticeConstant_300, latticeConstant_400, etc.
    Within each directory, look for subdirectories (like 0_1, 0_2, ... or however they're named)
    containing a file called 'lattice_constant.dat'.
    
    Then extract data from that file and write to output_csv.
    """
    
    # Prepare to store results
    results = []
    results_ave = []

    # Loop over each temperature in the list
    for temp in temps:
        lx_ave = []
        ly_ave = []
        lz_ave = []
        # Construct the path for the given temperature directory, e.g. "latticeConstant_300"
        temp_dir_name = f"Step1_latticeConst_{temp}"
        temp_dir_path = os.path.join(base_path, temp_dir_name)
        
        # Safety check: if the directory doesn't exist, skip it
        if not os.path.isdir(temp_dir_path):
            print(f"Warning: {temp_dir_path} not found; skipping.")
            continue
        
        # Now list the subfolders (there should be 5 subfolders for each temperature)
        subfolders = [
            d for d in os.listdir(temp_dir_path) 
            if os.path.isdir(os.path.join(temp_dir_path, d))
        ]
        
        # Go through each subfolder
        for subfolder in subfolders:
            subfolder_path = os.path.join(temp_dir_path, subfolder)
            # The file we want to read
            lattice_file = os.path.join(subfolder_path, "lattice_constant.dat")
            
            if os.path.isfile(lattice_file):
                with open(lattice_file, "r") as f:
                    lines = f.readlines()
                    
                    # Typically, the first lines might be headers. We'll parse each line after the headers.
                    # Example lines:
                    #   # Time-averaged data for fix 3
                    #   # TimeStep v_lx v_ly v_lz
                    #   10000 71.9158 71.9158 71.9158
                    #   ...
                    # We'll skip lines starting with '#'
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('#') or not line:
                            continue
                        # Split columns
                        parts = line.split()
                        # Typically: TimeStep, v_lx, v_ly, v_lz
                        if len(parts) == 4:
                            timestep = parts[0]
                            lx = float(parts[1]) / 20
                            ly = float(parts[2]) / 20
                            lz = float(parts[3]) / 20
                            # Store the data (you can store just the final line if you only want the last time step)
                            lx_ave.append(lx)
                            ly_ave.append(ly)
                            lz_ave.append(lz)
                            results.append([temp, subfolder, timestep, lx, ly, lz])
            else:
                print(f"File not found: {lattice_file}. Skipping...")
        lx_mean = np.average(lx_ave)
        ly_mean = np.average(ly_ave)
        lz_mean = np.average(lz_ave)
        results_ave.append([temp, lx_mean, ly_mean, lz_mean])

    # Write results to CSV
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Temperature", "lx", "ly", "lz"])
        writer.writerows(results_ave)


if __name__ == "__main__":
    modelSize = 20
    
    # Adjust this base directory to the folder that contains latticeConstant_300, latticeConstant_400, etc.
    BASE_PATH = "/home/yixishen/DMREF/NiCr/MD/simulations/Step1_latticeConst/BelandFeNiCr/NiFe/0.9/"
    
    # Temperatures from 300 to 1400 in steps of 100
    TEMPERATURES = [800, 1000, 1100, 1200, 1300, 1400]
    
    # Output CSV file name
    OUTPUT_CSV = "lattice_constants_summary_BolandNiFe0.7.csv"
    
    # Run the extractor
    extract_lattice_constants(BASE_PATH, TEMPERATURES, OUTPUT_CSV, 20)
    
    print(f"Done! Data has been written to {OUTPUT_CSV}")
