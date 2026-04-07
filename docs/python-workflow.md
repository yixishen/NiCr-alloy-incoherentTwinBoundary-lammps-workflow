---
layout: default
title: Python workflow
---

# Python workflow: createInput, autoRun, and postProcess

## Overview

This repository includes three families of Python scripts:

1. **createInput scripts**
   - generate simulation folders,
   - fill LAMMPS templates,
   - fill SLURM run templates.

2. **autoRun scripts**
   - submit jobs with `sbatch`,
   - watch the SLURM queue,
   - optionally resubmit failed jobs,
   - stop over-submitting by respecting a maximum number of active jobs.

3. **postProcess scripts**
   - summarize Step 1 lattice-constant outputs,
   - summarize Step 2 grid-search GB energies,
   - extract GB trajectories from Step 4 ECO dump files.

## Why these scripts are useful

For this workflow, repeated simulations are needed across combinations such as:

- temperature,
- composition,
- local atomic configuration,
- model index / seed,
- ECO driving force,
- boundary translation during grid search.

Manually creating, launching, and summarizing those cases is tedious and error-prone.
The Python workflow keeps the directory structure consistent from input generation through output analysis.

## File layout

```text
scripts/
├── createInput/
├── autoRun/
└── postProcess/
    ├── latticeConst.py
    ├── GridSearch_GBenergy.py
    └── extractGBmigration_timestep.py
```

## Important note about directory structure

The scripts are not directory-agnostic. They assume a specific simulation layout.

That is especially true for:

- restart handoff from Step 2 → Step 3,
- restart handoff from Step 3 → Step 4,
- recursive searching of Step 1 and Step 2 outputs,
- structured batch traversal of Step 4 cases.

Before editing folder names, read:

- [Suggested / required directory structure](directory-structure.md)

## Recommended usage

1. Test one manual example first.
2. Use the corresponding `createInput` script to generate a family of cases.
3. Check that a few case folders look correct.
4. Run the matching `autoRun` wrapper on the cluster.
5. Use the `postProcess` scripts to summarize results after completion.
