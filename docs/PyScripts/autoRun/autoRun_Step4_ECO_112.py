import subprocess
import time
import os

# User-specific configuration
username = "yixishen"  # Replace with your actual username
max_jobs = 15  # Maximum allowed concurrent jobs
component = "NiCr"
sim_type = 'Step4_ECO_112'
potential = 'MishinNiCr' #'NiFoiles1986' 
Ni_ratio = 0.7
ECO_DR = 0.01
job_path = '/home/yixishen/DMREF/NiCr/MD/simulations'+f"/{sim_type}/{potential}/{Ni_ratio}/{ECO_DR}/"
temperatures = [600, 800]  # [1100, 1300] is also required
comp_index = [0] # 1,2
size = ['nz8']
seeds =  [0,1,2]
job_dirs = []
job_name = "NiFe_Step4_ECOS3" #f" {sim_type}_{ECO_DR}_{Ni_ratio}" 
for _size in size:
    for k in comp_index:    
        for i in range(0,len(temperatures)):
            for j in range(0,len(seeds)):
                job_dirs.append(job_path + f"{_size}/comp{k}/Step4_ECOS3_112_{ECO_DR}_{temperatures[i]}/{j}/" )

# Track job submissions with a dictionary: {job_directory: jobID}
submitted_jobs = {}

def count_jobs(user,job_name):
    """Count the number of running or queued jobs for the user."""
    result = subprocess.run(["squeue", "-u", user, "-o \"%.18i %.40j %.8u %.10T %.10M %.10l %.6D %.10N\" "], stdout=subprocess.PIPE, text=True)

    lines = result.stdout.strip().split("\n")
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
            result = subprocess.run(["sbatch", "run.LAMMPS_ucsb"], stdout=subprocess.PIPE, text=True)
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
