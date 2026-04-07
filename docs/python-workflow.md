---
layout: default
title: Python workflow
---

# Python workflow: createInput and autoRun scripts

## Overview

This repository includes two families of Python scripts:

1. **createInput scripts**
   - generate simulation folders,
   - fill LAMMPS templates,
   - fill SLURM run templates.

2. **autoRun scripts**
   - submit jobs with `sbatch`,
   - watch the SLURM queue,
   - optionally resubmit failed jobs,
   - stop over-submitting by respecting a maximum number of active jobs.

## Why these scripts are useful

For this workflow, repeated simulations are needed across combinations such as:

- temperature,
- composition,
- local atomic configuration,
- model index / seed,
- ECO driving force,
- boundary translation during grid search.

Manually creating and launching those cases is tedious and error-prone. The Python
workflow keeps the directory structure consistent.

## File layout

```text
scripts/
├── createInput/
│   ├── Step1_latticeConst.py
│   ├── Step2_GridSearch.py
│   ├── Step3_EqSigma3_112.py
│   └── Step4_ECOSigma3_112.py
└── autoRun/
    ├── job_runner.py
    ├── autoRun_Step1_LC.py
    ├── autoRun_Step2_GridSearch.py
    ├── autoRun_Step3_Eq.py
    └── autoRun_Step4_ECO_112.py
```

## Improvements in the cleaned public version

Compared with a lab-internal working version, the cleaned public scripts aim to:

- avoid hard-coded absolute paths when possible,
- group editable settings near the top of each file,
- remove unused imports,
- use clearer naming for folder generation,
- share queue-management logic through one helper module,
- make Step 2 directory generation and Step 2 auto-run logic consistent.

## Notes on the createInput scripts

### Step 1
Generates bulk-alloy runs used to estimate lattice constants at selected temperatures.

### Step 2
Generates rigid-body grid-search cases for a selected Σ3 boundary geometry.

### Step 3
Generates restart-based equilibration cases after a low-energy boundary structure has been selected.

### Step 4
Generates ECO-driven migration runs based on the equilibrated restart files from Step 3.

## Notes on the autoRun scripts

The auto-run wrappers are intentionally lightweight. Each wrapper:

- defines the set of job directories,
- optionally skips directories that already have a completion sentinel,
- calls the shared `job_runner.py` helper.

This keeps the scheduler logic in one place instead of copying it into four different files.

## Recommended usage

1. Test one manual example first.
2. Use the corresponding `createInput` script to generate a family of cases.
3. Check that a few case folders look correct.
4. Run the matching `autoRun` wrapper on the cluster.
5. Post-process the outputs after completion.
