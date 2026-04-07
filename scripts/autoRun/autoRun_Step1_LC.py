#!/usr/bin/env python3
"""Submit Step 1 lattice-constant jobs on SLURM."""

from __future__ import annotations

from pathlib import Path
import os
from job_runner import run_submission_loop


USERNAME = "your_cluster_username"
MAX_JOBS = 30
JOB_NAME_FILTER = None  # count all jobs for this user, like the original script

POTENTIAL_TYPE = "BelandFeNiCr"
COMPONENT = "NiCr"
NI_RATIOS = ["0.7", "0.8", "0.9"]
TEMPERATURES = [800, 900, 1000, 1100, 1200, 1300, 1400]
MODEL_INDEX = [0, 1, 2]


def get_repo_root() -> Path:
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def main() -> None:
    repo_root = get_repo_root()
    job_root = repo_root / "simulations" / "Step1_latticeConst" / POTENTIAL_TYPE / COMPONENT

    job_dirs = []
    for ni_ratio in NI_RATIOS:
        for temperature in TEMPERATURES:
            for model_index in MODEL_INDEX:
                job_dirs.append(
                    job_root / ni_ratio / f"Step1_latticeConst_{temperature}" / str(model_index)
                )

    run_submission_loop(
        job_dirs=job_dirs,
        username=USERNAME,
        max_jobs=MAX_JOBS,
        job_name_filter=JOB_NAME_FILTER,
        submit_script_name="run.LAMMPS_ucsb",
        poll_seconds=120,
        resubmit_failed_jobs=False,
    )


if __name__ == "__main__":
    main()
