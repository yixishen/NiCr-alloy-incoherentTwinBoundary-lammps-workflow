import os
import re
import pandas as pd

def extract_last_gb_energy(file_path):
    """
    Reads a file and returns the numeric value from the last occurrence 
    of "GB energy is" in the file. If no such line is found, returns None.
    """
    last_energy = None
    # Pattern to extract a floating point or exponential number following the phrase
    pattern = re.compile(r"GB energy is\s+([-+]?[\d\.eE-]+)")
    try:
        with open(file_path, "r") as f:
            for line in f:
                if "GB energy is" in line:
                    match = pattern.search(line)
                    if match:
                        # Update the value each time a match is found so that the last one is retained
                        last_energy = float(match.group(1))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return last_energy

def main(root_directory):
    results = []
    # Walk through all subdirectories
    for current_dir, dirs, files in os.walk(root_directory):
        if "log.lammps" in files:
            file_path = os.path.join(current_dir, "log.lammps")
            gb_energy = extract_last_gb_energy(file_path)
            if gb_energy is not None:
                # Get the subdirectory relative to the provided root directory
                subdirectory = os.path.relpath(current_dir, root_directory)
                results.append({"Subdirectory": subdirectory, "GB Energy": gb_energy})
    
    if results:
        # Create a DataFrame and write the data to an Excel file
        df = pd.DataFrame(results)
        output_excel = os.path.join(root_directory, "GB_Energy.xlsx")
        try:
            df.to_excel(output_excel, index=False)
            print(f"Results successfully written to {output_excel}")
        except Exception as e:
            print(f"Error writing Excel file: {e}")
    else:
        print("No GB energy data found in any log.lammps files.")

if __name__ == "__main__":
    # Input the directory to search (it should be an absolute or relative path)
    #directory = input("Enter the directory path to search: ").strip()
    directory = '/home/yixishen/DMREF/NiCr/MD/simulations/Step2_GridSearch/NiCr/S3_112/MishinNiCr/0.8/nz12/0/'
    if os.path.isdir(directory):
        main(directory)
    else:
        print("The provided directory does not exist.")
