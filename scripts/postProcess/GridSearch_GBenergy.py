#!/usr/bin/env python3
"""Summarize Step 2 grid-search boundary energies from log.lammps files."""

from __future__ import annotations

from pathlib import Path
import os
import re

import pandas as pd


# =========================
# Editable settings
# =========================
SIMULATION_SUBROOT = Path("simulations/Step2_GridSearch/NiCr/S3_112/MishinNiCr/0.8/nz12nx15")
OUTPUT_SUBROOT = Path("results/postProcess/Step2_GridSearch")
WRITE_EXCEL = True
# =========================


GB_ENERGY_PATTERN = re.compile(r"GB energy is\s+([-+]?[\d\.eE-]+)")


def get_repo_root() -> Path:
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def extract_last_gb_energy(file_path: Path) -> float | None:
    """Return the numeric value from the last occurrence of 'GB energy is'."""
    last_energy: float | None = None
    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
            for line in handle:
                if "GB energy is" not in line:
                    continue
                match = GB_ENERGY_PATTERN.search(line)
                if match:
                    last_energy = float(match.group(1))
    except Exception as exc:
        print(f"[error] Failed to read {file_path}: {exc}")
    return last_energy


def summarize_gb_energies(root_directory: Path, output_dir: Path, write_excel: bool = True) -> None:
    """Walk through Step 2 outputs and summarize final GB energies."""
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, object]] = []

    for log_file in root_directory.rglob("log.lammps"):
        gb_energy = extract_last_gb_energy(log_file)
        if gb_energy is None:
            continue

        relative_dir = log_file.parent.relative_to(root_directory)
        results.append({
            "Subdirectory": str(relative_dir),
            "GB Energy": gb_energy,
        })

    if not results:
        print("[info] No GB energy data found.")
        return

    df = pd.DataFrame(results).sort_values(by=["Subdirectory"]).reset_index(drop=True)

    csv_path = output_dir / "GB_Energy.csv"
    df.to_csv(csv_path, index=False)
    if write_excel:
        df.to_excel(output_dir / "GB_Energy.xlsx", index=False)

    print(f"[done] Wrote: {csv_path}")


if __name__ == "__main__":
    repo_root = get_repo_root()
    summarize_gb_energies(
        root_directory=repo_root / SIMULATION_SUBROOT,
        output_dir=repo_root / OUTPUT_SUBROOT,
        write_excel=WRITE_EXCEL,
    )
