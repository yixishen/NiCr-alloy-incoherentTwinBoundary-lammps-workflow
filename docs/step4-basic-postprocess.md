---
layout: default
title: Step 4 - ECO-driven migration run and basic interpretation
---

# Step 4 — ECO-driven migration run and basic interpretation

## What this file does

The example input for this step is:

- `templates/in.Step4_ECO_example.in`

This file reads the equilibrated restart from Step 3, performs a short NPT
equilibration at the target temperature, and then applies the ECO driving force
through:

```lammps
fix gb all orient/eco ${eco_df} 0.25 ${cut_off} ${oriFile}
```

It then runs the production migration simulation while dumping two quantities
from `fix gb`:

- `f_gb[1]`
- `f_gb[2]`

## Why this step matters

This is the actual driven-migration stage of the workflow. Earlier steps prepare
the structure and the temperature state; this step is where boundary motion is
measured.

## Main variables in this template

- `${restart_file}` — restart from Step 3
- `${potential_file}` — path to the potential file
- `${Tend}` — target temperature
- `${eco_df}` — ECO driving-force magnitude
- `${cut_off}` — orientational cutoff distance
- `${oriFile}` — file used by `fix orient/eco`
- `${total_steps}` — total production run length

## Minimal example run

```bash
lmp -in in.Step4_ECO_example.in \
    -var restart_file restart.NiCr_0.9_sig3_112_regular_comp0_800K \
    -var potential_file potentials/FeNiCr_ArturV3.eam \
    -var Tend 800 \
    -var eco_df 0.025 \
    -var cut_off 3.9 \
    -var oriFile orient_file.dat \
    -var total_steps 100000
```

## Important outputs

- `dump.ECODF_${Tend}`
- `log.lammps`

The dump file includes:

```lammps
id type x y z f_gb[1] f_gb[2]
```

which means it stores both structural coordinates and ECO-related per-atom
quantities for later analysis.

## How this connects to post-processing

A basic post-processing workflow usually extracts:

- boundary position versus time
- total migration distance
- average migration velocity
- qualitative migration mode from the snapshots

## Common pitfalls

- using the wrong restart file from Step 3
- not checking that `oriFile` is present and compatible with the system
- using an ECO driving force that is too small to measure or too large to remain physical
- forgetting that one ECO trajectory is only one realization, not a full statistical result
