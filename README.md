# NiCr ITB MD Workflow

This repository shares a LAMMPS-based molecular dynamics (MD) workflow for studying
incoherent twin boundaries (ITBs), with a focus on boundary structure, energy, and migration
in Ni-based alloys.

The repository is organized in two parts:

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
```

## Recommended order for new users

If you are new to this workflow, I recommend following this order:

1. Run the **lattice constant** example manually.
2. Run a **rigid-body grid search** example manually.
3. Run one **ECO-driven migration** example manually.
4. Check the output and basic post-processing.
5. Then move to the **Python automation workflow** for repeated simulations.

This order helps users first understand the physical meaning of each calculation step
before using the automated workflow.

## Tutorial section

The tutorial pages are intended to explain the scientific role of each step before automation.

### Step 1: Lattice constant calculation
This step determines the reference lattice constant used to build physically consistent structures
for later calculations.

### Step 2: Rigid-body grid search
This step identifies a low-energy boundary structure before migration calculations are performed.

### Step 3: Single ECO example
This step demonstrates one manual migration simulation for one boundary type so that users can
understand the input structure, the driving force setup, and the output.

### Step 4: Basic post-processing
This step shows how to inspect the simulation output and extract quantities such as energy,
boundary position, and migration velocity.

## Automated workflow section

After the manual examples, this repository shows how to scale up to many repeated simulations.

The automated workflow is based on three parts:

- **CreateInput**: read templates and generate simulation folders and input files
- **autoRun**: submit and monitor repeated LAMMPS jobs on SLURM
- **postProcess**: extract quantities such as energies, boundary position, and migration velocity

## Software assumptions

This repository assumes users have access to:

- LAMMPS
- Python 3
- a SLURM-based cluster for batch jobs
- OVITO or equivalent visualization / post-processing tools

## Notes on public sharing

This repository focuses on sharing the **workflow** rather than all raw simulation data.

In general, the repository should include:

- scripts,
- templates,
- example inputs,
- documentation.

Large outputs, temporary files, and cluster-specific raw results are usually better kept out of the public repository.

## Citation

If you use this workflow, please cite the related paper above and, if appropriate, this repository.
