
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



