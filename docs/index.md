---
layout: default
title: NiCr ITB MD Workflow
---

# NiCr ITB MD Workflow

This site documents a four-step molecular dynamics workflow for studying
incoherent twin boundaries (ITBs) in Ni-based alloys.

The example inputs in this repository are lightly cleaned versions of the
original research templates. The main change is that private absolute paths
have been replaced by reusable placeholders such as `${potential_file}`.

## Related paper

**Yixi Shen and Irene J. Beyerlein**  
*Temperature-induced migration of Σ3[112] twin boundaries in NiCr alloy*  
**Journal of Materials Science** (2025)  
DOI: [10.1007/s10853-025-11276-9](https://doi.org/10.1007/s10853-025-11276-9)

## Recommended order for new users

1. [Step 1: Lattice constant calculation](step1-lattice-constant.md)
2. [Step 2: Rigid-body grid search](step2-grid-search.md)
3. [Step 3: Build and equilibrate one Σ3{112} ITB model](step3-eco-single-case.md)
4. [Step 4: ECO-driven migration run and basic interpretation](step4-basic-postprocess.md)
5. [Why repeated simulations are needed](why-statistics.md)

## What the four steps do

### Step 1 — Lattice constant calculation
Runs a bulk alloy calculation with minimization, NPT equilibration, and
time-averaging of `lx`, `ly`, and `lz` into `lattice_constant.dat`.

### Step 2 — Rigid-body grid search
Builds a three-region bicrystal, applies rigid-body translations, deletes
overlaps, minimizes the structure, and reports grain-boundary energy.

### Step 3 — Restart-based equilibration of the selected Σ3{112} ITB
Reads the restart from the previous step, minimizes again, ramps the
temperature from `Tstart` to `Tend`, and writes a new restart for ECO.

### Step 4 — ECO-driven migration
Reads the equilibrated restart, applies `fix orient/eco`, and dumps
boundary-driving-force information through `f_gb[1]` and `f_gb[2]`.

## Example templates included

- `templates/in.Step1_latticeConst_example.in`
- `templates/in.Step2_GridSearch_example.in`
- `templates/in.Step3_EqSigma3_112TB_example.in`
- `templates/in.Step4_ECO_example.in`

## Important note

These files are intentionally kept close to the originals. That makes them
good teaching examples, but it also means users should still check:

- potential-file compatibility,
- element ordering in `pair_coeff`,
- variable definitions passed in from Python or the command line,
- simulation cell dimensions and orientation choices.
