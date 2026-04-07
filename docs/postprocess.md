---
layout: default
title: Post-processing workflow
---

# Post-processing workflow

## Overview

The post-processing scripts turn raw simulation outputs into compact tables and trajectory summaries.

This repository currently includes three main post-processing scripts:

- `scripts/postProcess/latticeConst.py`
- `scripts/postProcess/GridSearch_GBenergy.py`
- `scripts/postProcess/extractGBmigration_timestep.py`

## Step 1: lattice constant summary

### What it reads
- `lattice_constant.dat` files inside Step 1 case directories

### What it writes
- per-case CSV summary
- temperature-averaged CSV summary
- optional Excel versions of those summaries

### Typical use
Use this after many Step 1 runs have completed and you want one table of lattice constants versus temperature.

## Step 2: grid-search GB energy summary

### What it reads
- `log.lammps` files inside Step 2 case directories

### What it extracts
- the last occurrence of a line containing `GB energy is ...`

### What it writes
- CSV summary
- Excel summary

### Typical use
Use this after grid search to compare trial translations and identify low-energy structures.

## Step 4: ECO trajectory extraction

### What it reads
- ECO dump files, typically named like `dump.ECODF_<T>`

### What it extracts
- a GB-only dump file
- average y-position of the two GBs over time
- migration distances relative to the first valid timestep

### Why it matters
This is the key post-processing step for migration analysis. It transforms the raw dump file
into a compact table that can be used for velocity fitting and later plotting.

## Output location

The cleaned public scripts write post-processing outputs into:

```text
results/postProcess/
```

instead of mixing analysis outputs into the original simulation tree.

That keeps simulation inputs and processed summaries separate.

## Important dependency

These scripts assume the simulation folders follow the expected layout. If the simulation directories
are reorganized, the post-processing scripts must be updated as well.

See:

- [Suggested / required directory structure](directory-structure.md)
