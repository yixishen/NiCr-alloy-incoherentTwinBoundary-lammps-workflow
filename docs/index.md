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

### Tutorial / manual examples

- [Step 1: Lattice constant calculation](step1-lattice-constant.md)
- [Step 2: Rigid-body grid search](step2-grid-search.md)
- [Step 3: ECO single-case migration](step3-eco-single-case.md)
- [Step 4: Basic post-processing](step4-basic-postprocess.md)

### Statistical workflow and automation

- [Why repeated simulations are needed](why-statistics.md)
- [Python workflow: createInput and autoRun scripts](python-workflow.md)

## Recommended order for new users

1. Step 1: lattice constant calculation
2. Step 2: rigid-body grid search
3. Step 3: one restart-based equilibration / ECO example
4. Step 4: basic post-processing
5. Why repeated simulations are needed
6. Python workflow and automation
