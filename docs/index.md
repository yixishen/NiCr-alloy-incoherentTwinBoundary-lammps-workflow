---
layout: default
title: NiCr ITB MD Workflow
---

# NiCr ITB MD Workflow

This site documents a LAMMPS-based molecular dynamics workflow for studying
incoherent twin boundaries (ITBs), with a particular focus on boundary structure,
energy, and migration in Ni-based alloys.

## Related paper

**Yixi Shen and Irene J. Beyerlein**  
*Temperature-induced migration of Σ3[112] twin boundaries in NiCr alloy*  
**Journal of Materials Science** (2025)  
DOI: [10.1007/s10853-025-11276-9](https://doi.org/10.1007/s10853-025-11276-9)

## How this site is organized

This documentation is divided into two parts:

### 1. Tutorial / manual examples
These pages introduce each main calculation step in a transparent way before
moving to automation:

- [Step 1: Lattice constant calculation](step1-lattice-constant.md)
- [Step 2: Rigid-body grid search](step2-grid-search.md)
- [Step 3: ECO single-case migration](step3-eco-single-case.md)
- [Step 4: Basic post-processing](step4-basic-postprocess.md)

### 2. Statistical workflow and automation
These pages explain why repeated MD simulations are needed and how the Python
workflow is used to scale up from one example to many production runs:

- [Why repeated simulations are needed](why-statistics.md)

## Recommended order for new users

If you are new to this repository, I recommend following this order:

1. Read **Step 1: Lattice constant calculation**
2. Read **Step 2: Rigid-body grid search**
3. Read **Step 3: ECO single-case migration**
4. Read **Step 4: Basic post-processing**
5. Then read **Why repeated simulations are needed**

This order helps users first understand the physical meaning of each calculation
step before using the automated workflow.

## What this repository provides

- tutorial-style manual examples,
- templates for LAMMPS input generation,
- Python scripts for automated input creation,
- job submission logic for SLURM-based clusters,
- a structure for post-processing repeated simulations.

## What this repository does not try to provide

This site is not meant to store all raw outputs from large production runs.
Instead, it focuses on sharing the workflow in a reusable and understandable form.
