#!/usr/bin/env python3
"""Generate Step 2 rigid-body grid-search cases for Σ3{112} boundaries."""

from __future__ import annotations

from pathlib import Path
from string import Template
import math
import os
import numpy as np


# =========================
# Editable settings
# =========================
CR_FRACTION = 0.3
LATTICE_CONSTANT = 3.582
BULK_ENERGY_PER_ATOM = -4.358

COMPONENT = "NiCr"
POTENTIAL_LABEL = "MishinNiCr"
BOUNDARY_TYPE = "S3_112"
PAIR_STYLE = "adp"
POTENTIAL_NAME = "CrNi.adp.Howells_Bonny.txt"
POTENTIAL_ELEMENT = "Cr Ni"

TEMPLATE_NAME = "in.Step2_GridSearch_Bonny_template_NiCr"
SLURM_TEMPLATE_NAME = "run.LAMMPS_GridSearch"

CUTOFF_VALUES = [0.3, 1.0]
DIS_X = np.round(np.arange(0, 1.1, 0.1), 1).tolist()
DIS_Y = [0.0]
DIS_Z = np.round(np.arange(0, 1.1, 0.1), 1).tolist()

# Separate chemistry/structure seeds from folder index naming
CHEMISTRY_SEEDS = [722302, 512342, 412352]

# Σ3 {112}
X1 = [1, -1, 0]
Y1 = [1, 1, 2]
Z1 = [-1, -1, 1]

X2 = [1, 0, 1]
Y2 = [-1, 2, 1]
Z2 = [-1, -1, 1]

NX = 15
NY1 = 30
NY2 = 20
NZ = 8
# =========================


def get_repo_root() -> Path:
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def axis_length(vec: list[int], lattice_const: float) -> float:
    return math.sqrt(sum(x * x for x in vec)) * lattice_const


def main() -> None:
    repo_root = get_repo_root()
    templates_dir = repo_root / "templates"
    ni_fraction = f"{1 - CR_FRACTION:.1f}"
    size_label = f"nz{NZ}nx{NX}"

    simulation_root = (
        repo_root
        / "simulations"
        / "Step2_GridSearch"
        / COMPONENT
        / BOUNDARY_TYPE
        / POTENTIAL_LABEL
        / ni_fraction
        / size_label
    )
    potential_file = repo_root / "potentials" / POTENTIAL_NAME

    xd1 = axis_length(X1, LATTICE_CONSTANT)
    yd1 = axis_length(Y1, LATTICE_CONSTANT)
    zd1 = axis_length(Z1, LATTICE_CONSTANT)

    xd2 = axis_length(X2, LATTICE_CONSTANT)
    yd2 = axis_length(Y2, LATTICE_CONSTANT)
    zd2 = axis_length(Z2, LATTICE_CONSTANT)

    xp0 = -NX * xd1
    xp1 = NX * xd1

    yp0 = -NY1 * yd1 + 0.005
    yp1 = -NY2 * yd1 + 0.005
    yp2 = -NY2 * yd1 - 0.005
    yp3 = NY2 * yd1 + 0.005
    yp4 = NY2 * yd1 - 0.005
    yp5 = NY1 * yd2 + 0.01

    zp0 = -NZ * zd1
    zp1 = NZ * zd1

    yp00 = yp0 - 0.01
    yp55 = yp5 + 0.01

    translations = [(dx, dy, dz) for dx in DIS_X for dy in DIS_Y for dz in DIS_Z]

    lammps_template = Template((templates_dir / TEMPLATE_NAME).read_text())
    slurm_template = Template((templates_dir / SLURM_TEMPLATE_NAME).read_text())

    for config_index, seed in enumerate(CHEMISTRY_SEEDS):
        for cutoff in CUTOFF_VALUES:
            for dx, dy, dz in translations:
                case_dir = (
                    simulation_root
                    / f"config{config_index}"
                    / f"{cutoff}_{dx}_{dy}_{dz}"
                )
                case_dir.mkdir(parents=True, exist_ok=True)

                input_name = f"in.Step2_GridSearch_{ni_fraction}_{dx}_{dy}_{dz}"

                lammps_text = lammps_template.safe_substitute(
                    latticeConst=LATTICE_CONSTANT,
                    xp0=xp0, xp1=xp1,
                    yp0=yp0, yp00=yp00, yp1=yp1, yp2=yp2, yp3=yp3, yp4=yp4, yp5=yp5, yp55=yp55,
                    zp0=zp0, zp1=zp1,
                    xx1=X1[0], xy1=X1[1], xz1=X1[2],
                    yx1=Y1[0], yy1=Y1[1], yz1=Y1[2],
                    zx1=Z1[0], zy1=Z1[1], zz1=Z1[2],
                    xx2=X2[0], xy2=X2[1], xz2=X2[2],
                    yx2=Y2[0], yy2=Y2[1], yz2=Y2[2],
                    zx2=Z2[0], zy2=Z2[1], zz2=Z2[2],
                    pair_style=PAIR_STYLE,
                    potential_file=str(potential_file),
                    potential_element=POTENTIAL_ELEMENT,
                    component=COMPONENT,
                    disX=dx,
                    disY0=dy,
                    disY1=dy * 2,
                    disZ=dz,
                    cutOff=cutoff,
                    potential=POTENTIAL_LABEL,
                    boundary_type=BOUNDARY_TYPE,
                    NiFrac=ni_fraction,
                    seed=seed,
                    pEnergy=BULK_ENERGY_PER_ATOM,
                )
                (case_dir / input_name).write_text(lammps_text)

                slurm_text = slurm_template.safe_substitute(
                    Ni_fraction=ni_fraction,
                    inFile=input_name,
                    component=COMPONENT,
                    cutOff=cutoff,
                    potential=POTENTIAL_LABEL,
                    disX=dx,
                    disY=dy,
                    disZ=dz,
                )
                (case_dir / "run.LAMMPS_ucsb").write_text(slurm_text)

    print(f"Created Step 2 cases under: {simulation_root}")


if __name__ == "__main__":
    main()
