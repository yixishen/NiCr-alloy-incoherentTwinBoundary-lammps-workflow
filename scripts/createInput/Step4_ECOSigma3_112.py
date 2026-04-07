#!/usr/bin/env python3
"""Generate Step 4 ECO-driven migration cases for Σ3{112} boundaries."""

from __future__ import annotations

from pathlib import Path
from string import Template
import os


# =========================
# Editable settings
# =========================
LATTICE_CONSTANTS = [3.611518, 3.6222298]
TEMPERATURES = [600, 800]
TOTAL_STEPS = [300000, 300000]

SEEDS = [0, 1, 2]
COMP_INDEX = [0, 1, 2]
SIZE_LABELS = ["nz8"]

POTENTIAL_LABEL = "MishinNiCr"
SIM_TYPE_CREATE_GB = "Step3_EqSigma3"
COMPONENT = "NiCr"
NI_FRACTION = 0.7
ECO_DRIVING_FORCE = 0.01

PAIR_STYLE = "adp"
PAIR_ELEMENTS = "Cr Ni"

TEMPLATE_NAME = "in.Step4_ECO_Beland_templates"
SLURM_TEMPLATE_NAME = "run.LAMMPS_ucsb"

POTENTIAL_FILE_REL = "potentials/CrNi.adp.Howells_Mishin.txt"
RUN_TIME_HOURS = "60"
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
        repo_root / "simulations" / "Step4_ECO_112" / POTENTIAL_LABEL / str(NI_FRACTION) / str(ECO_DRIVING_FORCE)
    )
    restart_root = repo_root / "simulations" / "Step3_EqSigma3_112" / POTENTIAL_LABEL / str(NI_FRACTION)
    potential_file = repo_root / POTENTIAL_FILE_REL
    ori_ref_root = repo_root / "OriRef" / POTENTIAL_LABEL / str(NI_FRACTION)

    lammps_template = Template((templates_dir / TEMPLATE_NAME).read_text())
    slurm_template = Template((templates_dir / SLURM_TEMPLATE_NAME).read_text())

    for size_label in SIZE_LABELS:
        for lattice_constant, temperature, step_count in zip(LATTICE_CONSTANTS, TEMPERATURES, TOTAL_STEPS):
            cutoff = round(1.1 * lattice_constant, 4)
            for model_index, seed in enumerate(SEEDS):
                for comp_index in COMP_INDEX:
                    case_dir = (
                        simulation_root
                        / size_label
                        / f"comp{comp_index}"
                        / f"Step4_ECOS3_112_{ECO_DRIVING_FORCE}_{temperature}"
                        / str(model_index)
                    )
                    case_dir.mkdir(parents=True, exist_ok=True)

                    restart_file = (
                        restart_root
                        / size_label
                        / f"comp{comp_index}"
                        / f"{SIM_TYPE_CREATE_GB}_{temperature}"
                        / str(model_index)
                        / f"restart.{COMPONENT}_{NI_FRACTION}_sig3_112_{size_label}_comp{comp_index}_{temperature}K"
                    )
                    ori_file = ori_ref_root / f"sigma3_112{COMPONENT}{NI_FRACTION}_{temperature}K.ori"
                    input_name = f"in.Step4_ECOS3_112_{ECO_DRIVING_FORCE}_{NI_FRACTION}_{temperature}K_{model_index}"

                    lammps_text = lammps_template.safe_substitute(
                        a=lattice_constant,
                        cut_off=cutoff,
                        potential_file=str(potential_file),
                        pair_style=PAIR_STYLE,
                        component=PAIR_ELEMENTS,
                        Tend=temperature,
                        seed=seed,
                        NiFrac=NI_FRACTION,
                        modelNum=model_index,
                        eco_df=ECO_DRIVING_FORCE,
                        restart_file=str(restart_file),
                        oriFile=str(ori_file),
                        total_steps=step_count,
                    )
                    (case_dir / input_name).write_text(lammps_text)

                    slurm_text = slurm_template.safe_substitute(
                        Ni_fraction=NI_FRACTION,
                        sim_type="Step4_ECO_112",
                        temp=temperature,
                        j=model_index,
                        Tend=temperature,
                        seed=seed,
                        NiFrac=NI_FRACTION,
                        eco_df=ECO_DRIVING_FORCE,
                        run_time=RUN_TIME_HOURS,
                    )
                    (case_dir / "run.LAMMPS_ucsb").write_text(slurm_text)

    print(f"Created Step 4 cases under: {simulation_root}")


if __name__ == "__main__":
    main()
