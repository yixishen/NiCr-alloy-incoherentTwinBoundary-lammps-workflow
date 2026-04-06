import subprocess
import time
import os
import numpy as np

# User-specific configuration
username = "yixishen"  # Replace with your actual username
max_jobs = 10  # Maximum allowed concurrent jobs

cutOff =  [0.3, 1]   #A

# def motion   #lattice unit
#disX = np.round(np.arange(0, 1.1, 0.1), 1).tolist()
disX = np.round(np.arange(0, 1.1, 0.1), 1).tolist()
disY = [0]
disZ = np.round(np.arange(0, 1.1, 0.1), 1).tolist()

seed = [1, 2]

job_dirs = []

sim_type = 'Step2_GridSearch'
boundary_type =  'S3_112' #'MishinNiCr'
component =  "NiCr"
Ni_fraction = "0.7"
size = ["nz12"]

potential_index = 'MishinNiCr' #"NiFoiles1986" #
job_name = 'GridSearch_MishinNiCr'
check_restart = "restart.al_S3_112_NiCr"

#####################################
#---------- Directory---------------#
#####################################
base_dir = '/home/yixishen/DMREF/NiCr/MD/'  # cluster
templates_dir = base_dir + "templates/"  # direction for lammps input templates
simulation_dir = base_dir + f"/simulations/{sim_type}/{component}/{boundary_type}/{potential_index}/{Ni_fraction}/" 

moveAtoms = []
for i in disX:
    for j in disY:
        for k in disZ:
            moveAtoms.append([i,j,k])
 #lattice unit

#job names


# Loop over parameters
for k in range(0, len(seed)):
    # three random model for each alloy
    for j in range(0, len(moveAtoms)): 
        for i in range(0,len(cutOff)):
            for _size in size:
                # Create a unique directory for the simulation
                _cutOff = cutOff[i]
                _disX, _disY, _disZ = moveAtoms[j][:3]

                _dis_inf = f'{_disX}_{_disY}_{_disZ}'
                sim_dir = os.path.join(simulation_dir, f"{_size}/{seed[k]}/{_cutOff}_{_dis_inf}")
                restart_file = os.path.join(sim_dir, check_restart)

                if os.path.isfile(restart_file):
                    print(f"Skipping {sim_dir} — restart file exists.")
                    continue
                job_dirs.append(sim_dir)

# Track job submissions with a dictionary: {job_directory: jobID}
submitted_jobs = {}

def count_jobs(user,job_name):
    """Count the number of running or queued jobs for the user."""
    result = subprocess.run(["squeue", "-u", user, "-o \"%.18i %.40j %.8u %.10T %.10M %.10l %.6D %.10N\" "], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.strip().split("\n")
    #print(lines)
    # Skip header and filter lines that contain the substring
    count = sum(1 for line in lines[1:] if job_name in line)
    
    return count

def get_job_state(job_id):
    """Use sacct to get the state of a job."""
    result = subprocess.run(
        ["sacct", "-j", str(job_id), "--format=JobID,State", "--noheader"],
        stdout=subprocess.PIPE, text=True
    )
    # Expect output like: "123456  FAILED"
    output = result.stdout.strip()
    if output:
        parts = output.split()
        if len(parts) >= 2:
            return parts[1]
    return None

job_index = 0


while job_index < len(job_dirs) or submitted_jobs:
    # Check for failed jobs and re-submit them
    for job_dir, job_id in list(submitted_jobs.items()):
        state = get_job_state(job_id)
        if state in ["FAILED", "NODE_FAIL"]:
            print(f"Job {job_id} from {job_dir} failed with state {state}. Resubmitting...")
            os.chdir(job_dir)
            #result = subprocess.run(["sbatch", "run.LAMMPS_ucsb"], stdout=subprocess.PIPE, text=True)
            # Parse new job id from output (assuming standard sbatch output, e.g., "Submitted batch job 123457")
            new_job_id = result.stdout.strip().split()[-1]
            submitted_jobs[job_dir] = new_job_id
        elif state in ["COMPLETED"]:
            # Remove completed jobs from tracking
            print(f"Job {job_id} from {job_dir} completed successfully.")
            submitted_jobs.pop(job_dir)
    
    # Check current job count
    
    current_jobs = count_jobs(username, job_name)
    print(f"Current job count: {current_jobs}")
    
    # Submit new jobs if below threshold and pending jobs exist
    if current_jobs < max_jobs and job_index < len(job_dirs):
        job_dir = job_dirs[job_index]
        print(f"Submitting job from directory: {job_dir}")
        os.chdir(job_dir)
        result = subprocess.run(["sbatch", "run.LAMMPS_ucsb"], stdout=subprocess.PIPE, text=True)
        new_job_id = result.stdout.strip().split()[-1]
        submitted_jobs[job_dir] = new_job_id
        job_index += 1
    else:
        print("Waiting for job slots to be available or for job status updates...")
        time.sleep(60)  # Wait for 60 seconds before checking again

print("All jobs have been successfully submitted and completed.")
