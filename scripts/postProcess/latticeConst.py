#!/usr/bin/env python3
"""Summarize Step 1 lattice-constant outputs."""

from __future__ import annotations

from pathlib import Path
import csv
import os
from typing import Iterable

import numpy as np
import pandas as pd


# =========================
# Editable settings
# =========================
SIMULATION_SUBROOT = Path("simulations/Step1_latticeConst/BelandFeNiCr/NiCr/0.9")
TEMPERATURES = [800, 900, 1000, 1100, 1200, 1300, 1400]
CELL_REPEAT_DIVISOR = 20

CASE_OUTPUT_NAME = "lattice_constants_cases.csv"
SUMMARY_OUTPUT_NAME = "lattice_constants_summary.csv"
WRITE_EXCEL = True
# =========================


def get_repo_root() -> Path:
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def extract_lattice_constants(
    base_path: Path,
    temperatures: Iterable[int],
    output_dir: Path,
    cell_repeat_divisor: int = 20,
    write_excel: bool = True,
) -> None:
    """Extract lattice constants from Step 1 outputs.

    The script searches for:
      Step1_latticeConst_<T>/<model_index>/lattice_constant.dat

    It writes:
    - a case-level CSV
    - a temperature-averaged CSV
    - optional Excel copies
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    case_rows: list[list[object]] = []
    summary_rows: list[list[object]] = []

    for temp in temperatures:
        temp_dir = base_path / f"Step1_latticeConst_{temp}"
        if not temp_dir.is_dir():
            print(f"[warning] Missing directory: {temp_dir}")
            continue

        lx_values: list[float] = []
        ly_values: list[float] = []
        lz_values: list[float] = []

        subfolders = sorted([p for p in temp_dir.iterdir() if p.is_dir()])

        for subfolder in subfolders:
            lattice_file = subfolder / "lattice_constant.dat"
            if not lattice_file.is_file():
                print(f"[warning] Missing file: {lattice_file}")
                continue

            with lattice_file.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    parts = line.split()
                    if len(parts) != 4:
                        continue

                    timestep = int(float(parts[0]))
                    lx = float(parts[1]) / cell_repeat_divisor
                    ly = float(parts[2]) / cell_repeat_divisor
                    lz = float(parts[3]) / cell_repeat_divisor

                    lx_values.append(lx)
                    ly_values.append(ly)
                    lz_values.append(lz)
                    case_rows.append([temp, subfolder.name, timestep, lx, ly, lz])

        if lx_values:
            summary_rows.append([
                temp,
                float(np.average(lx_values)),
                float(np.average(ly_values)),
                float(np.average(lz_values)),
            ])

    case_df = pd.DataFrame(case_rows, columns=["Temperature", "Case", "TimeStep", "lx", "ly", "lz"])
    summary_df = pd.DataFrame(summary_rows, columns=["Temperature", "lx", "ly", "lz"])

    case_csv = output_dir / "lattice_constants_cases.csv"
    summary_csv = output_dir / "lattice_constants_summary.csv"
    case_df.to_csv(case_csv, index=False)
    summary_df.to_csv(summary_csv, index=False)

    if write_excel:
        case_df.to_excel(output_dir / "lattice_constants_cases.xlsx", index=False)
        summary_df.to_excel(output_dir / "lattice_constants_summary.xlsx", index=False)

    print(f"[done] Wrote: {case_csv}")
    print(f"[done] Wrote: {summary_csv}")


if __name__ == "__main__":
    repo_root = get_repo_root()
    base_path = repo_root / SIMULATION_SUBROOT
    output_dir = repo_root / "results" / "postProcess" / "Step1_latticeConst"
    extract_lattice_constants(
        base_path=base_path,
        temperatures=TEMPERATURES,
        output_dir=output_dir,
        cell_repeat_divisor=CELL_REPEAT_DIVISOR,
        write_excel=WRITE_EXCEL,
    )
