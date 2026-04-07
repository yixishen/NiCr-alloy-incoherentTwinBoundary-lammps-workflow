# Python scripts

This folder contains the public-facing Python workflow used to create, submit,
and post-process LAMMPS runs for the four main MD workflow steps.

## `createInput/`

These scripts read text templates and write case folders, LAMMPS inputs, and SLURM scripts.

## `autoRun/`

These scripts submit and monitor jobs on a SLURM cluster.

## `postProcess/`

These scripts summarize outputs after the runs have completed:

- `latticeConst.py` for Step 1 lattice-constant results
- `GridSearch_GBenergy.py` for Step 2 grid-search results
- `extractGBmigration_timestep.py` for Step 4 ECO migration trajectories

## Important note

The scripts depend on a consistent directory structure.
See:

- `docs/directory-structure.md`
- `docs/postprocess.md`
