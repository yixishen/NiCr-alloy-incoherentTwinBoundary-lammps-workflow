#!/usr/bin/env python3
"""Submit Step 2 grid-search jobs on SLURM."""

from __future__ import annotations

from pathlib import Path
import os
import numpy as np
from job_runner import filter_existing_cases, run_submission_loop


USERNAME = "your_cluster_username"
MAX_JOBS = 10
JOB_NAME_FILTER = "GridSearch_MishinNiCr"

CUTOFF_VALUES = [0.3, 1.0]
DIS_X = np.round(np.arange(0, 1.1, 0.1), 1).tolist()
DIS_Y = [0.0]
DIS_Z = np.round(np.arange(0, 1.1, 0.1), 1).tolist()

BOUNDARY_TYPE = "S3_112"
COMPONENT = "NiCr"
NI_FRACTION = "0.7"
SIZE_LABEL = "nz8nx15"
POTENTIAL_LABEL = "MishinNiCr"
CONFIG_INDEX = [0, 1, 2]

COMPLETION_SENTINEL = "restart.al_S3_112_NiCr"


def get_repo_root() -> Path:
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def main() -> None:
    repo_root = get_repo_root()
    job_root = (
        repo_root
        / "simulations"
        / "Step2_GridSearch"
        / COMPONENT
        / BOUNDARY_TYPE
        / POTENTIAL_LABEL
        / NI_FRACTION
        / SIZE_LABEL
    )

    job_dirs = []
    for config_index in CONFIG_INDEX:
        for cutoff in CUTOFF_VALUES:
            for dx in DIS_X:
                for dy in DIS_Y:
                    for dz in DIS_Z:
                        job_dirs.append(
                            job_root / f"config{config_index}" / f"{cutoff}_{dx}_{dy}_{dz}"
                        )

    job_dirs = filter_existing_cases(job_dirs, COMPLETION_SENTINEL)

    run_submission_loop(
        job_dirs=job_dirs,
        username=USERNAME,
        max_jobs=MAX_JOBS,
        job_name_filter=JOB_NAME_FILTER,
        submit_script_name="run.LAMMPS_ucsb",
        poll_seconds=60,
        resubmit_failed_jobs=True,
    )


if __name__ == "__main__":
    main()
