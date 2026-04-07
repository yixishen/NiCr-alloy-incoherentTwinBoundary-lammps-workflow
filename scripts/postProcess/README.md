# postProcess

This folder contains cleaned public-facing post-processing scripts for the workflow.

## Included scripts

### `latticeConst.py`
Summarizes Step 1 `lattice_constant.dat` outputs.

### `GridSearch_GBenergy.py`
Recursively scans Step 2 `log.lammps` files and extracts the final reported GB energy.

### `extractGBmigration_timestep.py`
Reads Step 4 ECO dump files, identifies the two GBs from `f_gb[2]`, writes a GB-only dump,
and exports GB positions and migration distances.

## Output convention

These scripts write summaries into `results/postProcess/` by default, so processed outputs
are kept separate from the raw simulation tree.
