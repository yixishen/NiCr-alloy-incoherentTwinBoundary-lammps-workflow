import subprocess
import time
import os

# User-specific configuration
username = "yixishen"  # Replace with your actual username
max_jobs = 30  # Maximum allowed concurrent jobs
job_path = '/home/yixishen/DMREF/NiCr/MD/simulations/Step1_latticeConst/BelandFeNiCr/NiCr/'
Niratio = ['0.7','0.8','0.9']
temperatures = [800, 900, 1000, 1100, 1200, 1300, 1400]
seeds =  [412443, 723343, 643453]
job_dirs = []
for i in range(0,len(temperatures)):
    for j in range(0,len(seeds)):
        for k in Niratio:
            job_dirs.append(job_path + f"{k}/Step1_latticeConst_{temperatures[i]}/{j}/" )

def count_jobs(user):
    """
    Count the number of jobs in the queue for a specific user.
    The first line of squeue output is the header, so subtract one.
    """
    result = subprocess.run(["squeue", "-u", user], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.strip().split("\n")
    return len(lines) - 1  if len(lines) > 1 else 0

job_index = 0

while job_index < len(job_dirs):
    current_jobs = count_jobs(username)
    print(f"Current job count: {current_jobs}")
    
    if current_jobs < max_jobs:
        job_dir = job_dirs[job_index]
        print(f"Submitting job from directory: {job_dir}")
        # Change to the job's directory
        os.chdir(job_dir)
        # Submit the job (adjust the file name if necessary)
        subprocess.run(["sbatch", "run.LAMMPS_ucsb"])
        job_index += 1
    else:
        print("Maximum number of jobs running. Waiting before checking again...")
        time.sleep(120)  # Wait for 60 seconds before checking again

print("All jobs have been submitted.")

