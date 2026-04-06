import subprocess
import time
import os

# User-specific configuration
username = "yixishen"  # Replace with your actual username
max_jobs = 30  # Maximum allowed concurrent jobs
job_path = '/home/yixishen/DMREF/NiCr/MD/simulations/Step3_EqSigma3_112/MishinNiCr/0.8/'
temperatures = [600, 800, 1000, 1100, 1200, 1300, 1400]
seeds =  [0, 1, 2]
comp_index = [0] # [1, 2, 5] for Ni80Cr in Mishin as lower ITB energy
job_dirs = []
size = ['nz12']  #'nz6' for some model

#job names
job_name = 'NiFe_Step3_EqSigma3_0.7'

for _size in size:
    for i in comp_index:
        for j in range(0,len(temperatures)):
            for k in range(0,len(seeds)):    
                job_dirs.append(job_path + f"{_size}/comp{i}/Step3_EqSigma3_{temperatures[j]}/{k}/" )

# Track job submissions with a dictionary: {job_directory: jobID}
submitted_jobs = {}

def count_jobs(user,job_name):
    """Count the number of running or queued jobs for the user."""
    result = subprocess.run(["squeue", "-u", user, "-o \"%.18i %.40j %.8u %.10T %.10M %.10l %.6D %.10N\" "], stdout=subprocess.PIPE, text=True)
    # result = subprocess.run(["squeue", "-u", user, "-n", job_name],
    #                        stdout=subprocess.PIPE, text=True)
    lines = result.stdout.strip().split("\n")
    #return len(lines) - 1 if len(lines) > 1 else 0
    
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

