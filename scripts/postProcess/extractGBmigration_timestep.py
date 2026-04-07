#!/usr/bin/env python3
"""Extract grain-boundary trajectories from Step 4 ECO dump files."""

from __future__ import annotations

from pathlib import Path
from itertools import product
import logging
import os

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


# =========================
# Editable settings
# =========================
POTENTIAL = "MishinNiCr"
NI_FRACTIONS = [0.7]
ECO_DF_VALUES = [0.01]
TEMPERATURES = ["600", "800"]
MODEL_INDEX = ["0", "1", "2"]
SIZE_LABELS = ["nz8"]
COMP_INDEX = ["0", "1", "2"]

DUMP_TEMPLATE = "dump.ECODF_{temp}"
GB_THRESHOLD = 0.2
WRITE_GB_ONLY_DUMP = True
WRITE_EXCEL = True

SIMULATION_ROOT = Path("simulations/Step4_ECO_112")
OUTPUT_ROOT = Path("results/postProcess/Step4_ECO_112")
# =========================


def get_repo_root() -> Path:
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def parse_lammps_dump(filename: Path):
    """Yield one timestep block at a time from a LAMMPS dump file."""
    with filename.open("r", encoding="utf-8", errors="ignore") as handle:
        while True:
            line = handle.readline()
            if not line:
                break
            if line.strip() != "ITEM: TIMESTEP":
                continue

            timestep = int(handle.readline().strip())

            handle.readline()  # ITEM: NUMBER OF ATOMS
            natoms = int(handle.readline().strip())

            handle.readline()  # ITEM: BOX BOUNDS ...
            box_bounds = []
            for _ in range(3):
                lo_hi = handle.readline().strip().split()
                box_bounds.append(list(map(float, lo_hi)))
            box_bounds = np.array(box_bounds)

            atom_header = handle.readline().strip().split()
            columns = atom_header[2:]

            atom_data = []
            for _ in range(natoms):
                atom_data.append(list(map(float, handle.readline().split())))

            yield {
                "timestep": timestep,
                "natoms": natoms,
                "box": box_bounds,
                "columns": columns,
                "atoms": pd.DataFrame(atom_data, columns=columns),
            }


def identify_two_gbs(df: pd.DataFrame, f_gb2_max: float = 0.2):
    """Identify the two GB groups from a dataframe using y-position clustering."""
    if "f_gb[2]" not in df.columns or "y" not in df.columns:
        return None, None

    gb_atoms = df[(df["f_gb[2]"] <= f_gb2_max) & (df["f_gb[2]"] >= -f_gb2_max)]
    if len(gb_atoms) < 2:
        return None, None

    y_positions = gb_atoms[["y"]].values
    kmeans = KMeans(n_clusters=2, random_state=0, n_init=10)
    labels = kmeans.fit_predict(y_positions)

    gb1 = gb_atoms[labels == 0]
    gb2 = gb_atoms[labels == 1]

    if gb1["y"].mean() > gb2["y"].mean():
        gb1, gb2 = gb2, gb1

    return gb1, gb2


def write_gb_dump(input_file: Path, output_file: Path, f_gb2_max: float = 0.2) -> None:
    """Write a dump containing only GB atoms, with a gb_group label."""
    with output_file.open("w", encoding="utf-8") as out:
        for data in parse_lammps_dump(input_file):
            timestep = data["timestep"]
            box = data["box"]
            columns = data["columns"]
            df = data["atoms"]

            gb1, gb2 = identify_two_gbs(df, f_gb2_max=f_gb2_max)

            out.write("ITEM: TIMESTEP\n")
            out.write(f"{timestep}\n")

            if gb1 is None or gb2 is None:
                out.write("ITEM: NUMBER OF ATOMS\n0\n")
                out.write("ITEM: BOX BOUNDS pp pp pp\n")
                for lo, hi in box:
                    out.write(f"{lo} {hi}\n")
                out.write("ITEM: ATOMS " + " ".join(columns) + " gb_group\n")
                continue

            gb1 = gb1.copy()
            gb2 = gb2.copy()
            gb1["gb_group"] = 1
            gb2["gb_group"] = 2
            gb_atoms = pd.concat([gb1, gb2], ignore_index=True)

            out.write("ITEM: NUMBER OF ATOMS\n")
            out.write(f"{len(gb_atoms)}\n")
            out.write("ITEM: BOX BOUNDS pp pp pp\n")
            for lo, hi in box:
                out.write(f"{lo} {hi}\n")
            out.write("ITEM: ATOMS " + " ".join(columns) + " gb_group\n")

            write_cols = columns + ["gb_group"]
            for _, row in gb_atoms.iterrows():
                out.write(" ".join(map(str, row[write_cols].values)) + "\n")


def compute_gb_positions(input_file: Path, f_gb2_max: float = 0.2) -> pd.DataFrame:
    """Compute average GB positions and migration distances versus timestep."""
    results = []
    initial_gb1_y = None
    initial_gb2_y = None

    for data in parse_lammps_dump(input_file):
        timestep = data["timestep"]
        df = data["atoms"]
        gb1, gb2 = identify_two_gbs(df, f_gb2_max=f_gb2_max)

        if gb1 is not None and gb2 is not None:
            avg_y_gb1 = gb1["y"].mean()
            avg_y_gb2 = gb2["y"].mean()
        else:
            avg_y_gb1 = np.nan
            avg_y_gb2 = np.nan

        if initial_gb1_y is None and not np.isnan(avg_y_gb1):
            initial_gb1_y = avg_y_gb1
        if initial_gb2_y is None and not np.isnan(avg_y_gb2):
            initial_gb2_y = avg_y_gb2

        results.append([timestep, avg_y_gb1, avg_y_gb2])

    df_positions = pd.DataFrame(results, columns=["timestep", "gb1_y", "gb2_y"])

    if initial_gb1_y is not None:
        df_positions["gb1_distance"] = df_positions["gb1_y"] - initial_gb1_y
    else:
        df_positions["gb1_distance"] = np.nan

    if initial_gb2_y is not None:
        df_positions["gb2_distance"] = df_positions["gb2_y"] - initial_gb2_y
    else:
        df_positions["gb2_distance"] = np.nan

    return df_positions


def process_case(
    simulation_case_dir: Path,
    output_case_dir: Path,
    dump_filename: str,
    f_gb2_max: float = 0.2,
    write_gb_only_dump: bool = True,
    write_excel: bool = True,
) -> tuple[bool, str]:
    """Process one Step 4 ECO case directory."""
    input_file = simulation_case_dir / dump_filename
    if not input_file.exists():
        return False, f"Missing file: {input_file}"

    output_case_dir.mkdir(parents=True, exist_ok=True)

    if write_gb_only_dump:
        gb_dump_out = output_case_dir / "dump_gb_only.lammpstrj"
        write_gb_dump(input_file, gb_dump_out, f_gb2_max=f_gb2_max)

    df_positions = compute_gb_positions(input_file, f_gb2_max=f_gb2_max)
    csv_path = output_case_dir / "gb_positions_and_distances.csv"
    df_positions.to_csv(csv_path, index=False)

    if write_excel:
        df_positions.to_excel(output_case_dir / "gb_positions_and_distances.xlsx", index=False)

    return True, f"Processed: {input_file}"


def main() -> None:
    repo_root = get_repo_root()
    simulation_root = repo_root / SIMULATION_ROOT
    output_root = repo_root / OUTPUT_ROOT
    output_root.mkdir(parents=True, exist_ok=True)

    missing_log = output_root / f"missing_files_log_{POTENTIAL}.txt"

    with missing_log.open("w", encoding="utf-8") as log_file:
        for temp, model_index, eco_df, size_label, comp_index, ni_fraction in product(
            TEMPERATURES, MODEL_INDEX, ECO_DF_VALUES, SIZE_LABELS, COMP_INDEX, NI_FRACTIONS
        ):
            relative_case = Path(
                f"{POTENTIAL}/{ni_fraction}/{eco_df}/{size_label}/comp{comp_index}/"
                f"Step4_ECOS3_112_{eco_df}_{temp}/{model_index}"
            )
            simulation_case_dir = simulation_root / relative_case
            output_case_dir = output_root / relative_case
            dump_filename = DUMP_TEMPLATE.format(temp=temp)

            ok, message = process_case(
                simulation_case_dir=simulation_case_dir,
                output_case_dir=output_case_dir,
                dump_filename=dump_filename,
                f_gb2_max=GB_THRESHOLD,
                write_gb_only_dump=WRITE_GB_ONLY_DUMP,
                write_excel=WRITE_EXCEL,
            )
            log_file.write(message + "\n")
            print(message)

    print(f"[done] Wrote log: {missing_log}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    main()
