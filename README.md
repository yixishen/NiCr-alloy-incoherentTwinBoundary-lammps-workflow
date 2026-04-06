# NiCr ITB MD Workflow

This repository shares a LAMMPS-based molecular dynamics (MD) workflow for studying
incoherent twin boundary (ITB) structure, energy, and migration in Ni-based alloys.

The workflow is organized in two parts:

1. **Tutorial / manual examples**  
   A step-by-step introduction to the main calculations, including:
   - lattice constant calculation,
   - rigid-body grid search,
   - a single ECO-driven boundary migration case.

2. **Automated workflow for statistical studies**  
   A Python-based framework for:
   - generating many input files from templates,
   - submitting repeated jobs on SLURM,
   - organizing outputs for post-processing.

This structure is intended to help new users first understand each physical calculation
in a transparent way, and then scale up to production studies where many repeated MD
simulations are needed.

## Related paper

This workflow is associated with the following paper:

**Yixi Shen and Irene J. Beyerlein**  
*Temperature-induced migration of Σ3[112] twin boundaries in NiCr alloy*  
**Journal of Materials Science** (2025)  
DOI: [10.1007/s10853-025-11276-9](https://doi.org/10.1007/s10853-025-11276-9)

## Why this repository exists

For alloy/interface migration problems, a single MD simulation is usually not enough
to characterize the response. The measured migration behavior can depend on:

- the local atomic configuration near the boundary,
- the initial thermal state,
- the chosen temperature and driving force,
- the boundary structure used as the starting point.

For that reason, this repository is designed not only to show how to run one example,
but also how to automate repeated simulations and organize the results for statistical analysis.

## Repository structure

```text
.
├── README.md
├── docs/
│   ├── index.md
│   ├── step1-lattice-constant.md
│   ├── step2-grid-search.md
│   ├── step3-eco-single-case.md
│   ├── why-statistics.md
│   └── ...
├── templates/
│   ├── README.md
│   ├── in.step1_latticeConst.template
│   ├── in.gridSearch.template
│   ├── in.ECO.template
│   └── run.LAMMPS.template
├── scripts/
│   ├── createInput/
│   ├── autoRun/
│   └── postProcess/
├── examples/
│   ├── step1_latticeConst/
│   ├── step2_gridSearch/
│   └── step3_ECO_single_case/
└── potentials/
