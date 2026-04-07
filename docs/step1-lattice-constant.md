---
layout: default
title: Step 1 - Lattice constant calculation
---

# Step 1 — Lattice constant calculation

## What this file does

The example input for this step is:

- `templates/in.Step1_latticeConst_example.in`

This file creates a bulk FCC alloy box, randomly assigns a fraction of atoms to
type 2 using:

```lammps
set type 1 type/fraction 2 ${NiFrac} ${seed}
```

and then performs:

1. energy minimization with `fix box/relax iso 0.0`,
2. NPT equilibration at `${Tend}`,
3. time averaging of `lx`, `ly`, and `lz` into `lattice_constant.dat`.

## Why this step matters

Later steps build bicrystal and boundary structures using a lattice constant.
If the lattice constant is inconsistent with the potential, composition, or
temperature, artificial strain can be introduced into the model.

## Main variables in this template

This template expects at least:

- `${NiFrac}` — alloy fraction used in the `set type/fraction` command
- `${seed}` — random seed for alloy assignment
- `${Tend}` — target equilibration temperature
- `${potential_file}` — path to the potential file

## Minimal example run

If you want to run this file manually, you would typically pass the variables
from the command line, for example:

```bash
lmp -in in.Step1_latticeConst_example.in \
    -var NiFrac 0.9 \
    -var seed 12345 \
    -var Tend 800 \
    -var potential_file potentials/FeNiCr_ArturV3.eam
```

## What to inspect

This step writes several outputs that are useful for checking the calculation:

- `dump.afterCreate`
- `dump.afterMini`
- `log.lammps`
- `lattice_constant.dat`

The most important one is `lattice_constant.dat`, which stores time-averaged
box lengths during the data-collection stage.

## How to use the result

From `lattice_constant.dat`, you can extract an average box length and convert
it to the effective lattice constant for the chosen structure size. That value
is then passed into the structure-building stage of Step 2.

## Common pitfalls

- forgetting to pass `${potential_file}`
- using the wrong element order in `pair_coeff`
- reusing a lattice constant from a different potential or temperature
- treating one short equilibration as a final converged value
