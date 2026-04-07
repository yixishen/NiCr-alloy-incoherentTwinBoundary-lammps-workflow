#!/usr/bin/env python3
"""Generate Step 3 restart-based equilibration cases for Σ3{112} boundaries."""

from __future__ import annotations

from pathlib import Path
from string import Template
import os


# =========================
# Editable settings
# =========================
TEMPERATURES = [600, 800, 1000, 1100, 1200, 1300, 1400]
TSTEP_VALUES = [60, 80, 100, 110, 120, 130, 140]

SEEDS = [513243, 142391, 824534]
COMP_INDEX = [0, 1, 2]
SIZE_LABELS = ["nz12"]

POTENTIAL_LABEL = "MishinNiCr"
COMPONENT = "NiCr"
NI_FRACTION = 0.8

TEMPLATE_NAME = "in.Step3_EqSigma3_112TB_Beland_templates"
SLURM_TEMPLATE_NAME = "run.LAMMPS_Step3_Eq112"

POTENTIAL_FILE_REL = "potentials/CrNi.adp.Howells_Mishin.txt"
ORI_REF_SUBDIR = f"OriRef/{POTENTIAL_LABEL}/{NI_FRACTION}"

LAMMPS_ELEMENTS = "Cr Ni"
LAMMPS_PAIR_STYLE = "adp"
RUN_TIME_HOURS = "20"
# =========================


def get_repo_root() -> Path:
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def main() -> None:
    repo_root = get_repo_root()
    templates_dir = repo_root / "templates"
    simulation_root = repo_root / "simulations" / "Step3_EqSigma3_112" / POTENTIAL_LABEL / str(NI_FRACTION)
    potential_file = repo_root / POTENTIAL_FILE_REL
    ori_ref_root = repo_root / ORI_REF_SUBDIR

    lammps_template = Template((templates_dir / TEMPLATE_NAME).read_text())
    slurm_template = Template((templates_dir / SLURM_TEMPLATE_NAME).read_text())

    for size_label in SIZE_LABELS:
        for comp_index in COMP_INDEX:
            for temperature, tstep in zip(TEMPERATURES, TSTEP_VALUES):
                for model_index, seed in enumerate(SEEDS):
                    case_dir = (
                        simulation_root / size_label / f"comp{comp_index}" / f"Step3_EqSigma3_{temperature}" / str(model_index)
                    )
                    case_dir.mkdir(parents=True, exist_ok=True)

                    restart_file = (
                        repo_root
                        / "simulations"
                        / "Step2_GridSearch"
                        / COMPONENT
                        / "S3_112"
                        / POTENTIAL_LABEL
                        / str(NI_FRACTION)
                        / f"restart.al_S3_112_{COMPONENT}_{size_label}_comp{comp_index}"
                    )
                    ori_file = ori_ref_root / f"sigma3_112Ni{NI_FRACTION}_{temperature}K.ori"
                    input_name = f"in.Step3_EqSigma3_{NI_FRACTION}_{temperature}K_{model_index}"

                    lammps_text = lammps_template.safe_substitute(
                        Comp=COMPONENT,
                        comp_index=comp_index,
                        size=size_label,
                        potential=str(potential_file),
                        Tend=temperature,
                        Tstep=tstep,
                        seed=seed,
                        NiFrac=NI_FRACTION,
                        modelNum=model_index,
                        restart_file=str(restart_file),
                        oriFile=str(ori_file),
                        lammps_ele=LAMMPS_ELEMENTS,
                        lammps_potential_com=LAMMPS_PAIR_STYLE,
                    )
                    (case_dir / input_name).write_text(lammps_text)

                    slurm_text = slurm_template.safe_substitute(
                        Ni_fraction=NI_FRACTION,
                        sim_type="Step3_EqSigma3",
                        temp=temperature,
                        j=model_index,
                        Tend=temperature,
                        seed=seed,
                        NiFrac=NI_FRACTION,
                        run_time=RUN_TIME_HOURS,
                        Comp=COMPONENT,
                    )
                    (case_dir / "run.LAMMPS_ucsb").write_text(slurm_text)

    print(f"Created Step 3 cases under: {simulation_root}")


if __name__ == "__main__":
    main()
