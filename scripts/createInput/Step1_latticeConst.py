#!/usr/bin/env python3
"""Generate Step 1 lattice-constant calculation cases."""

from __future__ import annotations

from pathlib import Path
from string import Template
import os


# =========================
# Editable settings
# =========================
TEMPERATURES = [800, 900, 1000, 1100, 1200, 1300, 1400]
SEEDS = [412443, 723343, 643453]

SIM_TYPE = "Step1_latticeConst"
POTENTIAL_TYPE = "BelandFeNiCr"
COMPONENT = "NiCr"
NI_FRACTION = "0.9"

TEMPLATE_NAME = "in.Step1_latticeConst_Beland_NiCr_temp"
SLURM_TEMPLATE_NAME = "run.LAMMPS_latConst"
POTENTIAL_FILE_REL = "potentials/FeNiCr_ArturV3.eam"
# =========================


def get_repo_root() -> Path:
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def main() -> None:
    repo_root = get_repo_root()
    templates_dir = repo_root / "templates"
    simulation_root = (
        repo_root / "simulations" / SIM_TYPE / POTENTIAL_TYPE / COMPONENT / NI_FRACTION
    )
    potential_file = repo_root / POTENTIAL_FILE_REL

    lammps_template = Template((templates_dir / TEMPLATE_NAME).read_text())
    slurm_template = Template((templates_dir / SLURM_TEMPLATE_NAME).read_text())

    for temperature in TEMPERATURES:
        for model_index, seed in enumerate(SEEDS):
            case_dir = simulation_root / f"{SIM_TYPE}_{temperature}" / str(model_index)
            case_dir.mkdir(parents=True, exist_ok=True)

            input_name = f"in.{SIM_TYPE}_{NI_FRACTION}_{temperature}K_{model_index}"

            lammps_text = lammps_template.safe_substitute(
                potential=str(potential_file),
                Tend=temperature,
                seed=seed,
                NiFrac=NI_FRACTION,
                modelNum=model_index,
            )
            (case_dir / input_name).write_text(lammps_text)

            slurm_text = slurm_template.safe_substitute(
                Ni_fraction=NI_FRACTION,
                temp=temperature,
                inFile=input_name,
                modelNum=model_index,
            )
            (case_dir / "run.LAMMPS_ucsb").write_text(slurm_text)

    print(f"Created Step 1 cases under: {simulation_root}")


if __name__ == "__main__":
    main()
