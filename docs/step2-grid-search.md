---
layout: default
title: Step 2 - Rigid-body grid search
---

# Step 2 — Rigid-body grid search

## What this file does

The example input for this step is:

- `templates/in.Step2_GridSearch_example.in`

This file builds a three-region bicrystal model (`g21`, `g1`, and `g22`) using
orientation matrices passed in through variables. It then:

1. assigns alloy composition,
2. applies rigid-body displacement to region `g1`,
3. deletes overlapping atoms,
4. minimizes the structure,
5. relaxes the box,
6. computes grain-boundary energy,
7. writes a restart for the selected structure.

## Why this step matters

The boundary structure used in later mobility calculations should not be chosen
arbitrarily. This template is meant to be used repeatedly with different
rigid-body translations such as `${disX}`, `${disY0}`, and `${disZ}` so that
different candidate structures can be compared.

## Main variables in this template

This file depends on many geometry variables. The most important groups are:

### Cell and region geometry
- `${latticeConst}`
- `${xp0}`, `${xp1}`
- `${yp00}`, `${yp55}`
- `${yp0}` through `${yp5}`
- `${zp0}`, `${zp1}`

### Orientation matrices
- `${xx1}` ... `${zz1}`
- `${xx2}` ... `${zz2}`

### Grid-search and chemistry variables
- `${NiFrac}`
- `${seed}`
- `${disX}`, `${disY0}`, `${disZ}`
- `${cutOff}`
- `${pEnergy}`

### Labels used in output files
- `${boundary_type}`
- `${component}`

### Potential files
- `${potential_alloy}`
- `${potential_fs}`

## Minimal example run

A manual run would usually look like:

```bash
lmp -in in.Step2_GridSearch_example.in \
    -var latticeConst 3.538 \
    -var NiFrac 0.9 \
    -var seed 12345 \
    -var disX 0.0 \
    -var disY0 0.0 \
    -var disZ 0.0 \
    -var cutOff 0.35 \
    -var pEnergy -4.244136667 \
    -var boundary_type sig3_112 \
    -var component NiCr \
    -var potential_alloy potentials/FeCrNi_d.eam.alloy \
    -var potential_fs potentials/FeCrNi_s.eam.fs
```

In practice, the geometry and orientation variables are normally supplied by a
Python generation script.

## How the boundary energy is computed

The script computes total atomic energy through:

```lammps
compute eng all pe/atom
compute eatoms all reduce sum c_eng
```

and then evaluates grain-boundary energy with:

```lammps
variable gbe equal "(c_eatoms - (v_minimumenergy * count(all)))/v_gbarea"
variable gbemJm2 equal ${gbe}*16021.7733
```

This makes the template useful for scanning candidate structures and ranking
them by boundary energy.

## Important outputs

- `dump.minimized_${boundary_type}_${component}`
- `restart.al_${boundary_type}_${component}`
- printed grain-boundary energy in mJ/m²

## What to do next

Once a low-energy translation state is selected, its restart file becomes the
starting point for Step 3.
