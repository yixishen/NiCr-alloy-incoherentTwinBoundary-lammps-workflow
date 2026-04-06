
# NiCr ITB LAMMPS workflow template

This repository is a public-facing template for sharing a LAMMPS workflow built around:

1. template-based input generation,
2. batch execution on a SLURM cluster, and
3. post-processing of simulation outputs.

It is designed around the workflow used for the NiCr incoherent twin-boundary study reported in:

> Y. Shen and I. J. Beyerlein, *Temperature-induced migration of Σ3[112] twin boundaries in NiCr alloy*, Journal of Materials Science (2025).
[Read the paper here](https://doi.org/10.1007/s10853-025-11276-9)

## What this repo is for

This repo is meant to share the workflow logic behind the paper, not to dump every raw file from a cluster run.

The goal is to make the project understandable and reusable for someone who wants to:

- generate large numbers of LAMMPS inputs from templates,
- organize simulations by composition / potential / temperature / seed,
- submit and monitor many jobs on SLURM,
- collect outputs for later analysis,
- understand how the paper workflow maps onto code and folders.

## Workflow summary

The folder naming in this project follows a multi-step workflow:

- Step 1 – lattice constant / reference properties
- Step 2 – rigid-body grid search
- Step 3 – create equal-Σ3 boundary models
- Step 4 – ECO-driven migration simulations
- Post-processing – extract energies, positions, and velocities

## Repository layout

```text
scripts/create_input/   # write case folders and LAMMPS inputs from templates
scripts/autorun/        # submit and monitor jobs on SLURM
scripts/postprocess/    # extract measurable quantities from outputs
templates/              # LAMMPS and SLURM templates
simulations/            # generated case folders (usually ignored in Git)
docs/                   # GitHub Pages site
```

## Quick start

1. Put your clean LAMMPS and SLURM templates in `templates/`.
2. Edit the configuration block at the top of the Python scripts.
3. Run a `scripts/create_input/*.py` script to generate cases.
4. Run `scripts/autorun/*.py` on your cluster login node.
5. Use your post-processing scripts to extract final results.

## What to edit before running

- potential file locations
- cluster partition / walltime / ntasks
- composition list
- temperature list
- seeds
- directory conventions

## Recommended public-sharing rules

### Keep in the repo
- Python scripts that generate inputs
- job-management scripts
- clean template files
- tiny example inputs
- documentation and usage notes

### Usually do not keep in the repo
- large dump files
- SLURM output logs
- massive generated `simulations/` trees
- cluster-specific absolute paths
- copyrighted or redistribution-restricted files

## Citation

If this workflow helps your work, please cite both the repository and the related paper.
```

---

## 5. Draft GitHub Pages site

GitHub Pages can be very simple. A clean site in `docs/` is enough.

### `docs/_config.yml`

```yaml
title: "NiCr ITB LAMMPS workflow"
description: "Template repo for LAMMPS + SLURM research workflows"
theme: jekyll-theme-cayman
markdown: kramdown
```

### `docs/index.md`

```md
---
layout: default
title: NiCr ITB LAMMPS workflow
---

# NiCr ITB LAMMPS workflow

A lightweight public-facing site for a research workflow built around:

- LAMMPS input generation from text templates,
- SLURM job submission and monitoring,
- post-processing of boundary-migration simulations.

## What this site covers

This site explains how to share a clean public version of a local research workflow.

## Pages

- [Getting started](getting-started.md)
- [Workflow map](workflow.md)
- [GitHub upload guide](github-guide.md)
- [Troubleshooting](troubleshooting.md)

## Recommended release philosophy

Start with the parts that are most valuable to other researchers:

1. the templates,
2. the input-generation scripts,
3. the job-submission logic,
4. a clear README,
5. one small example.

Then add post-processing scripts later after cleanup.
```

### `docs/getting-started.md`

```md
---
layout: default
title: Getting started
---

# Getting started

## 1. Decide what the repo should contain

A strong first public version does not need every raw simulation file.

Good first-release contents:
- cleaned templates,
- cleaned Python scripts,
- one or two tiny examples,
- documentation,
- citation information.

## 2. Clean the local workflow

Before uploading, remove:
- absolute paths,
- usernames,
- huge outputs,
- temporary backups,
- anything you are not allowed to redistribute.

## 3. Make the repo understandable to a stranger

Pretend the reader is a materials modeler who knows LAMMPS but has never seen your folder tree.
```

### `docs/workflow.md`

```md
---
layout: default
title: Workflow map
---

# Workflow map

## How the workflow is organized

### Step 1 — reference-property calculations
Use template-based LAMMPS inputs to determine quantities such as lattice constants or other basic reference values.

### Step 2 — rigid-body grid search
Build many trial boundary configurations and identify low-energy structures.

### Step 3 — boundary model construction
Create the selected Σ3 boundary model to be used for production simulations.

### Step 4 — ECO or migration simulations
Run temperature- and seed-dependent migration simulations for the target structure.

### Step 5 — post-processing
Extract the measurable quantities of interest, assemble them, and generate publication-ready plots.
```

### `docs/github-guide.md`

```md
---
layout: default
title: GitHub upload guide
---

# GitHub upload guide

This guide is written for someone who wants the lowest-stress path to publishing a research workflow.

## Option A — browser upload only
1. Create a new repository on GitHub.
2. Download this template ZIP and unzip it locally.
3. Drag the cleaned files into the repository using GitHub’s web upload interface.
4. Commit the upload.
5. Turn on GitHub Pages using the `docs/` folder.

## Option B — GitHub Desktop
1. Create the repository on GitHub.
2. Clone it with GitHub Desktop.
3. Copy the template files into the local repo folder.
4. Commit and push from GitHub Desktop.

## Turn on GitHub Pages
1. Open the repository on GitHub.
2. Go to **Settings**.
3. Open **Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Choose your default branch.
6. Choose the `/docs` folder.
7. Save.
```

### `docs/troubleshooting.md`

```md
---
layout: default
title: Troubleshooting
---

# Troubleshooting

## My scripts still contain private paths
Search the repository for:
- `/home/`
- your username
- old project roots

## My GitHub Pages site shows 404
Common causes:
- Pages is not pointed at the `docs/` folder
- the site has not finished building yet
- the repo was not pushed successfully

## I do not want to share every potential file
That is fine. Keep the workflow public and document where users should obtain the potentials themselves.
```

---

## 6. Draft `.gitignore`

```gitignore
# macOS
.DS_Store

# Python
__pycache__/
*.pyc
.ipynb_checkpoints/

# Editors
.vscode/
.idea/

# Temporary / backup
*~
*.tmp
*.bak

# LAMMPS / simulation outputs
*.out
log.lammps*
*.lammpstrj
*.dump
*.cfg
*.dat
*.restart
*.gz

# SLURM
slurm-*.out
slurm-*.err

# Generated simulations
simulations/*
!simulations/README.md
```

---

## 7. Draft `CHECKLIST_BEFORE_PUBLISHING.md`

```md
# Checklist before publishing

## Clean up paths
- [ ] Remove absolute paths like `/home/yourname/...`
- [ ] Remove usernames, account names, or private directories
- [ ] Replace hard-coded cluster paths with relative paths or a small config block

## Clean up files
- [ ] Remove large dump files
- [ ] Remove `*.out`, `log.lammps*`, and temporary files
- [ ] Remove accidental backups like `file~`
- [ ] Keep only tiny example inputs in the repo

## Review legal / sharing issues
- [ ] Confirm you are allowed to redistribute each interatomic potential file
- [ ] Do not upload the published journal PDF unless your publishing agreement allows it
- [ ] Decide whether to share raw data, processed data, or only code

## Improve readability
- [ ] Add comments at the top of each script explaining what it does
- [ ] Rename files that are too cryptic for first-time users
- [ ] Add one minimal worked example
- [ ] Add a diagram or one-page workflow summary
```

---

## 8. Cleaned example scripts

These are not necessarily your final production scripts. They are **public-facing cleaned versions** that are much better suited for a GitHub repo.

### `scripts/create_input/create_step1_lattice_const.py`

```python
#!/usr/bin/env python3
"""Generate Step-1 lattice-constant simulation folders and inputs."""

from pathlib import Path
from string import Template

# =========================================================
# USER SETTINGS
# =========================================================
component = "NiCr"
potential_label = "BonnyNiCr"
potential_file = "../potentials/FeNiCr_ArturV3.eam"   # edit this path
element_order = "Cr Ni"
lattice_constant = 3.538
ni_fractions = [0.9]
temperatures = [600, 800, 1000, 1400]
seeds = [722302, 512342, 412352]
partition = "your_partition"
walltime = "02:00:00"
nodes = 1
ntasks = 16
# =========================================================

repo_root = Path(__file__).resolve().parents[2]
templates_dir = repo_root / "templates"
sim_root = repo_root / "simulations" / "Step1_latticeConst" / component / potential_label

lammps_template = Template((templates_dir / "in.step1_lattice_const.template").read_text())
slurm_template = Template((templates_dir / "run.lammps.slurm.template").read_text())

for ni_fraction in ni_fractions:
    for temperature in temperatures:
        for seed_index, seed in enumerate(seeds):
            case_dir = sim_root / str(ni_fraction) / str(temperature) / str(seed_index)
            case_dir.mkdir(parents=True, exist_ok=True)

            infile_name = f"in.step1_latticeConst_{potential_label}_{ni_fraction}_{temperature}"
            job_name = f"LC_{potential_label}_{ni_fraction}_{temperature}_{seed_index}"

            lammps_text = lammps_template.safe_substitute(
                lattice_const=lattice_constant,
                ni_fraction=ni_fraction,
                seed=seed,
                temperature=temperature,
                potential_file=potential_file,
                element_order=element_order,
            )
            (case_dir / infile_name).write_text(lammps_text)

            slurm_text = slurm_template.safe_substitute(
                job_name=job_name,
                infile=infile_name,
                walltime=walltime,
                nodes=nodes,
                ntasks=ntasks,
                partition=partition,
            )
            (case_dir / "run.LAMMPS").write_text(slurm_text)

print(f"Created cases under: {sim_root}")
```

### `scripts/create_input/create_sfe.py`

```python
#!/usr/bin/env python3
"""Example script for generating SFE calculation inputs from templates."""

from pathlib import Path
from string import Template

component = "NiCr"
sim_type = "SFE"
potential_label = "MishinNiCr"
potential_file = "../potentials/FeNiCr_ArturV3.eam"
ni_fraction = 0.9
seeds = [722302, 512342, 412352]
partition = "your_partition"
walltime = "02:00:00"
nodes = 1
ntasks = 16

repo_root = Path(__file__).resolve().parents[2]
templates_dir = repo_root / "templates"
sim_root = repo_root / "simulations" / sim_type / component / potential_label / str(ni_fraction)

lammps_template = Template((templates_dir / "in.sfe.template").read_text())
slurm_template = Template((templates_dir / "run.lammps.slurm.template").read_text())

for seed_index, seed in enumerate(seeds):
    case_dir = sim_root / str(seed_index)
    case_dir.mkdir(parents=True, exist_ok=True)

    infile_name = f"in.SFE_{ni_fraction}"
    job_name = f"SFE_{component}_{potential_label}_{ni_fraction}_{seed_index}"

    lammps_text = lammps_template.safe_substitute(
        seed=seed,
        ni_fraction=ni_fraction,
        potential_name=potential_label,
    )
    (case_dir / infile_name).write_text(lammps_text)

    slurm_text = slurm_template.safe_substitute(
        job_name=job_name,
        infile=infile_name,
        walltime=walltime,
        nodes=nodes,
        ntasks=ntasks,
        partition=partition,
    )
    (case_dir / "run.LAMMPS").write_text(slurm_text)
```

### `scripts/autorun/autorun_eco_1185.py`

```python
#!/usr/bin/env python3
"""Submit and monitor ECO_1185 jobs on a SLURM cluster."""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

username = "your_cluster_username"
max_jobs = 16
component = "Ni"
sim_type = "ECO_1185"
potential = "FoilesNi"
ni_ratio = 1.0
eco_driving_force = 0.025
temperatures = [50, 100, 200, 300, 600, 800, 1000, 1400]
seeds = [0, 1, 2]
submit_script_name = "run.LAMMPS"
poll_seconds = 60
resubmit_failed_jobs = True

repo_root = Path(__file__).resolve().parents[2]
job_root = (
    repo_root
    / "simulations"
    / sim_type
    / potential
    / str(ni_ratio)
    / str(eco_driving_force)
)
job_name_fragment = f"{component}_{sim_type}_{eco_driving_force}_{ni_ratio}"


def count_jobs(user: str, name_fragment: str) -> int:
    result = subprocess.run(["squeue", "-u", user], stdout=subprocess.PIPE, text=True, check=False)
    lines = result.stdout.strip().split("\n")
    if len(lines) <= 1:
        return 0
    return sum(1 for line in lines[1:] if name_fragment in line)


def get_job_state(job_id: str):
    result = subprocess.run(
        ["sacct", "-j", str(job_id), "--format=JobID,State", "--noheader"],
        stdout=subprocess.PIPE,
        text=True,
        check=False,
    )
    output = result.stdout.strip()
    if not output:
        return None
    parts = output.split()
    return parts[1] if len(parts) >= 2 else None
```

---

## 9. Draft templates

### `templates/in.step1_lattice_const.template`

```text
# Step 1: lattice constant / reference-property input template

units           metal
dimension       3
boundary        p p p
atom_style      atomic

lattice         fcc ${lattice_const}
region          whole block 0 20 0 20 0 20 units lattice
create_box      2 whole
create_atoms    1 box

set             type 1 type/fraction 2 ${ni_fraction} ${seed}

pair_style      eam/alloy
pair_coeff      * * ${potential_file} ${element_order}

neighbor        2.0 bin
neigh_modify    delay 10

fix             0 all box/relax iso 0.0 vmax 0.001
min_style       cg
minimize        1.0e-12 1.0e-12 2000 10000
unfix           0

reset_timestep  0
thermo          1000
thermo_style    custom step temp press pe lx ly lz pxx pyy pzz

timestep        0.001
velocity        all create ${temperature} 634534
fix             1 all npt temp ${temperature} ${temperature} 0.1 iso 0.0 0.0 1.0
run             50000
```

### `templates/run.lammps.slurm.template`

```bash
#!/bin/bash
#SBATCH --job-name=${job_name}
#SBATCH --output=${job_name}.out
#SBATCH --time=${walltime}
#SBATCH --nodes=${nodes}
#SBATCH --ntasks=${ntasks}
#SBATCH --partition=${partition}

module purge
# module load lammps
# module load mpi

srun lmp_mpi -in ${infile}
```

---

## 10. Very important cautions before publishing

### A. Remove absolute paths
Your sample files still contain cluster-specific absolute paths. Those should be replaced with relative paths or clearly labeled placeholders.

### B. Do not upload the published journal PDF by default
For a workflow repo, it is much safer to cite the paper and link the DOI than to upload the final published PDF.

### C. Think carefully about potential files
Interatomic potential files often come from other sources. Only upload them if redistribution is clearly okay.

### D. Do not upload all generated simulation folders
Those are usually better kept on HPC storage, not GitHub.

---

## 11. The easiest GitHub path for you

Because you said you are not very comfortable with GitHub, I strongly recommend this path:

### Phase 1 — browser-only upload
1. Create a new GitHub repository.
2. Copy the cleaned repo files into one local folder.
3. Upload them with GitHub’s web interface.
4. Commit.
5. Turn on Pages from `docs/`.

### Phase 2 — later move to GitHub Desktop
After the repo is live, you can start using GitHub Desktop for easier updates.

That keeps the first publication simple and low risk.

---

## 12. Suggested repo name and description

### Repo name
- `nicr-itb-lammps-workflow`
- `lammps-itb-migration-workflow`
- `nicr-twin-boundary-workflow`

### Description
Template-based LAMMPS + SLURM workflow for studying Σ3 incoherent twin-boundary migration in NiCr alloys.

---

## 13. What I recommend you do next

### Best next move
Send me one real `postProcess` script next.

That will let me turn this from a **clean skeleton** into a much more complete public release package.


