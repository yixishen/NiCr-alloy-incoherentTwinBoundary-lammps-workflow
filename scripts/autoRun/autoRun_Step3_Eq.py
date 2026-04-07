#!/usr/bin/env python3
"""Submit Step 3 equilibration jobs on SLURM."""

from __future__ import annotations

from pathlib import Path
import os
from job_runner import run_submission_loop


USERNAME = "your_cluster_username"
MAX_JOBS = 30
JOB_NAME_FILTER = "Step3_EqSigma3"

POTENTIAL_LABEL = "MishinNiCr"
NI_FRACTION = "0.8"
TEMPERATURES = [600, 800, 1000, 1100, 1200, 1300, 1400]
MODEL_INDEX = [0, 1, 2]
COMP_INDEX = [0]
SIZE_LABELS = ["nz12"]


def get_repo_root() -> Path:
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def main() -> None:
    repo_root = get_repo_root()
    job_root = repo_root / "simulations" / "Step3_EqSigma3_112" / POTENTIAL_LABEL / NI_FRACTION

    job_dirs = []
    for size_label in SIZE_LABELS:
        for comp_index in COMP_INDEX:
            for temperature in TEMPERATURES:
                for model_index in MODEL_INDEX:
                    job_dirs.append(
                        job_root / size_label / f"comp{comp_index}" / f"Step3_EqSigma3_{temperature}" / str(model_index)
                    )

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
