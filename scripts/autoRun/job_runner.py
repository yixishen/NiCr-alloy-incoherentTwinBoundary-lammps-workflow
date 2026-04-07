#!/usr/bin/env python3
"""Shared SLURM submission utilities for the autoRun scripts."""

from __future__ import annotations

from pathlib import Path
import subprocess
import time
from typing import Iterable


TERMINAL_SUCCESS_STATES = {"COMPLETED"}
TERMINAL_FAILURE_STATES = {"FAILED", "NODE_FAIL", "TIMEOUT", "CANCELLED", "OUT_OF_MEMORY"}


def count_jobs(user: str, job_name_filter: str | None = None) -> int:
    """Count running or queued jobs for a user, optionally filtering by job-name substring."""
    result = subprocess.run(
        ["squeue", "-u", user],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    lines = result.stdout.strip().splitlines()
    if len(lines) <= 1:
        return 0

    data_lines = lines[1:]
    if not job_name_filter:
        return len(data_lines)

    return sum(1 for line in data_lines if job_name_filter in line)


def get_job_state(job_id: str) -> str | None:
    """Return the SLURM state from sacct, if available."""
    result = subprocess.run(
        ["sacct", "-j", str(job_id), "--format=JobID,State", "--noheader"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    output = result.stdout.strip()
    if not output:
        return None

    first_line = output.splitlines()[0].strip()
    parts = first_line.split()
    return parts[1] if len(parts) >= 2 else None


def submit_job(case_dir: Path, submit_script_name: str = "run.LAMMPS_ucsb") -> str | None:
    """Submit one job and return the SLURM job ID."""
    submit_script = case_dir / submit_script_name
    if not submit_script.exists():
        print(f"[skip] Missing submit script: {submit_script}")
        return None

    result = subprocess.run(
        ["sbatch", submit_script_name],
        cwd=case_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"[submit failed] {case_dir}\n{result.stderr}")
        return None

    output = result.stdout.strip()
    print(f"[submitted] {case_dir} -> {output}")
    return output.split()[-1]


def filter_existing_cases(job_dirs: Iterable[Path], sentinel_name: str | None = None) -> list[Path]:
    """Skip cases that already contain a sentinel file."""
    if not sentinel_name:
        return [Path(p) for p in job_dirs]

    filtered: list[Path] = []
    for case_dir in map(Path, job_dirs):
        sentinel = case_dir / sentinel_name
        if sentinel.exists():
            print(f"[skip completed] {case_dir} (found {sentinel_name})")
            continue
        filtered.append(case_dir)
    return filtered


def run_submission_loop(
    job_dirs: Iterable[Path],
    username: str,
    max_jobs: int,
    job_name_filter: str | None = None,
    submit_script_name: str = "run.LAMMPS_ucsb",
    poll_seconds: int = 60,
    resubmit_failed_jobs: bool = True,
) -> None:
    """Submit and monitor jobs until all directories have been processed."""
    pending_dirs = [Path(p) for p in job_dirs]
    submitted_jobs: dict[Path, str] = {}
    job_index = 0

    while job_index < len(pending_dirs) or submitted_jobs:
        for case_dir, job_id in list(submitted_jobs.items()):
            state = get_job_state(job_id)

            if state in TERMINAL_SUCCESS_STATES:
                print(f"[done] {job_id} | {case_dir}")
                submitted_jobs.pop(case_dir)

            elif state in TERMINAL_FAILURE_STATES:
                print(f"[failed] {job_id} | {case_dir} | state={state}")
                submitted_jobs.pop(case_dir)
                if resubmit_failed_jobs:
                    new_job_id = submit_job(case_dir, submit_script_name)
                    if new_job_id:
                        submitted_jobs[case_dir] = new_job_id

        active_jobs = count_jobs(username, job_name_filter)
        print(
            f"[status] active_jobs={active_jobs}, "
            f"remaining_dirs={len(pending_dirs) - job_index}, "
            f"tracked={len(submitted_jobs)}"
        )

        while active_jobs < max_jobs and job_index < len(pending_dirs):
            case_dir = pending_dirs[job_index]
            if not case_dir.exists():
                print(f"[missing] {case_dir}")
                job_index += 1
                continue

            new_job_id = submit_job(case_dir, submit_script_name)
            if new_job_id:
                submitted_jobs[case_dir] = new_job_id
                active_jobs += 1

            job_index += 1

        if job_index < len(pending_dirs) or submitted_jobs:
            time.sleep(poll_seconds)

    print("All tracked jobs have finished.")
