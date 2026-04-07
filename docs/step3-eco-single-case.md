---
layout: default
title: Step 3 - Build and equilibrate one Σ3{112} ITB model
---

# Step 3 — Build and equilibrate one Σ3{112} ITB model

## What this file does

The example input for this step is:

- `templates/in.Step3_EqSigma3_112TB_example.in`

This file reads a restart generated in Step 2 and prepares it for the ECO run.
It performs:

1. `read_restart ${restart_file}`
2. another minimization,
3. box relaxation with `fix box/relax x 0.0 y 0.0 z 0.0`
4. gradual heating from `Tstart` to `Tend`
5. final NPT equilibration at `${Tend}`
6. writing of a new restart for Step 4

## Why this step matters

The output of the grid search is a low-energy geometric structure, but Step 4
needs a thermally equilibrated model at the target temperature. This step
bridges those two requirements.

## Main variables in this template

- `${restart_file}` — restart written in Step 2
- `${potential_file}` — path to the potential file
- `${Tend}` — target temperature
- `${modelNum}` — label used in dump names
- `${seed}` — velocity seed
- `${Tstep}` — temperature increment used in the heating loop
- `${Comp}`, `${NiFrac}`, `${size}`, `${comp_index}` — labels used in the restart filename

## Heating logic in this file

The template uses:

```lammps
variable step loop 160
variable T equal ${Tstart}+${step}*${Tstep}
```

and repeatedly applies NPT for 2000 steps per increment until the target
temperature is reached. After that, it performs a longer equilibration run of
30000 steps at `${Tend}`.

## Minimal example run

```bash
lmp -in in.Step3_EqSigma3_112TB_example.in \
    -var restart_file restart.al_sig3_112_NiCr \
    -var potential_file potentials/FeNiCr_ArturV3.eam \
    -var Tend 800 \
    -var modelNum 0 \
    -var seed 12345 \
    -var Tstep 5 \
    -var Comp NiCr \
    -var NiFrac 0.9 \
    -var size regular \
    -var comp_index 0
```

## Important outputs

- `dump.afterRestart_${Tend}_${modelNum}`
- `dump.equilibration_${Tend}_${modelNum}`
- `restart.${Comp}_${NiFrac}_sig3_112_${size}_comp${comp_index}_${Tend}K`

## Important note

The original template uses:

```lammps
pair_coeff * * ${potential_file} Fe Ni
```

This example keeps that mapping unchanged to stay close to the source file.
Before production use, verify that the element order matches your actual
potential file and atom-type convention.
