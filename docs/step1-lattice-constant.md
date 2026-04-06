---
layout: default
title: Step 1 - Lattice constant calculation
---

# Step 1 — Lattice constant calculation

## Goal

The goal of this step is to determine the lattice constant used to build the
initial structure for later calculations.

## Why this step matters

Before running boundary energy or migration calculations, the model should be
built using a physically consistent lattice constant for the chosen potential,
composition, and temperature.

Using an inappropriate lattice constant can introduce artificial strain into
the initial structure, which can then affect the measured boundary structure,
boundary energy, and migration response.

## What this example shows

In this tutorial example, one lattice constant calculation is run manually,
without using the automated Python workflow.

This example is meant to help users understand:

- the structure of the LAMMPS input,
- what quantities are being relaxed or measured,
- what output to inspect,
- what value will be passed into later steps.

## Typical input ingredients

A typical lattice constant calculation includes:

- definition of the crystal structure,
- specification of the alloy composition,
- definition of the interatomic potential,
- energy minimization or finite-temperature equilibration,
- extraction of the relaxed box size or lattice parameter.

## Example files

A minimal example may include files such as:

- `examples/step1_latticeConst/in.example`
- `templates/in.step1_latticeConst.template`
- `templates/run.LAMMPS.template`

## How to run manually

For a direct run:

```bash
lmp -in in.example
```

For a batch system:

```bash
sbatch run.LAMMPS
```

## What output to check

Common places to inspect the result include:

- `log.lammps`
- a dedicated output file such as `lattice_constant.dat`
- thermo output printed during the run

## How to interpret the result

At the end of this step, the user should obtain a lattice constant that is
consistent with:

- the selected potential,
- the selected composition,
- the selected temperature or equilibration condition.

This value is then used to construct later simulation cells more consistently.

## Common mistakes

Common mistakes in this step include:

- using the wrong potential file,
- using the wrong element ordering in `pair_coeff`,
- mixing lattice constants from different potentials,
- using one lattice constant for all temperatures without checking.

## Suggested next step

After the lattice constant is determined, proceed to the rigid-body grid search
used to identify a low-energy boundary structure.
