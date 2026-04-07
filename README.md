# NiCr ITB MD Workflow

This repository shares a LAMMPS-based molecular dynamics (MD) workflow for studying
incoherent twin boundaries (ITBs), with a focus on boundary structure, energy, and migration
in Ni-based alloys.

The repository is organized in four complementary parts:

1. **Templates**
   - LAMMPS input templates,
   - SLURM run templates,
   - reusable placeholders filled by Python.

2. **Minimal manual examples**
   - one small example for each of the main workflow steps,
   - intended to help a new user understand the physics and file flow before using the automated workflow.

3. **Python automation workflow**
   - `scripts/createInput/` generates simulation folders and input files,
   - `scripts/autoRun/` submits and monitors jobs on a SLURM cluster.

4. **Post-processing**
   - `scripts/postProcess/` extracts lattice constants, grid-search boundary energies,
     and ECO migration trajectories from the generated outputs.

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

## Recommended order for new users

If you are new to this workflow, I recommend following this order:

1. Read or run the **Step 1** lattice constant example manually.
2. Read the **Step 2** grid-search example and understand the geometry variables.
3. Read the **Step 3** equilibration example and understand the restart handoff.
4. Read the **Step 4** ECO example and understand what outputs are dumped.
5. Then read the **Python workflow** and **Post-processing** sections.

This order helps users first understand the physical meaning and file dependencies of each calculation step
before using the automated workflow.

## Suggested / required directory structure

The directory structure is not just for convenience. It is part of the workflow itself.

The `createInput`, `autoRun`, and `postProcess` scripts all assume specific folder names
for temperatures, model indices, compositions, and restart handoff between steps.
That means the structure below is strongly recommended, and in practice should be treated
as the required structure unless you also edit the Python scripts.

```text
.
├── README.md
├── docs/
│   ├── index.md
│   ├── step1-lattice-constant.md
│   ├── step2-grid-search.md
│   ├── step3-eco-single-case.md
│   ├── step4-basic-postprocess.md
│   ├── why-statistics.md
│   ├── python-workflow.md
│   ├── postprocess.md
│   └── directory-structure.md
├── templates/
├── examples/
│   ├── step1_latticeConst/
│   ├── step2_gridSearch/
│   ├── step3_equilibrate/
│   └── step4_eco/
├── scripts/
│   ├── createInput/
│   ├── autoRun/
│   └── postProcess/
├── simulations/
│   ├── Step1_latticeConst/
│   ├── Step2_GridSearch/
│   ├── Step3_EqSigma3_112/
│   └── Step4_ECO_112/
├── results/
│   └── postProcess/
└── potentials/
```

### Step-specific simulation layout

```text
simulations/
├── Step1_latticeConst/<potential>/<component>/<ni_fraction>/Step1_latticeConst_<T>/<model_index>/
├── Step2_GridSearch/<component>/<boundary_type>/<potential>/<ni_fraction>/<size_label>/config<k>/<cutoff>_<dx>_<dy>_<dz>/
├── Step3_EqSigma3_112/<potential>/<ni_fraction>/<size_label>/comp<k>/Step3_EqSigma3_<T>/<model_index>/
└── Step4_ECO_112/<potential>/<ni_fraction>/<eco_df>/<size_label>/comp<k>/Step4_ECOS3_112_<eco_df>_<T>/<model_index>/
```

### Why this matters

- Step 3 needs restart files written by Step 2.
- Step 4 needs restart files written by Step 3.
- The post-processing scripts search for files using these directory names.
- If you rename the folders, you must update the scripts accordingly.

## Python workflow section

The Python workflow is split into three parts:

### `scripts/createInput/`
These scripts read text templates and write case folders, LAMMPS inputs, and SLURM scripts.

### `scripts/autoRun/`
These scripts submit and monitor jobs on a SLURM cluster.

### `scripts/postProcess/`
These scripts summarize the outputs:

- `latticeConst.py` for Step 1 lattice-constant results,
- `GridSearch_GBenergy.py` for Step 2 grid-search energies,
- `extractGBmigration_timestep.py` for Step 4 ECO trajectory analysis.

## Post-processing section

The post-processing scripts assume the simulation folders already exist and follow the expected layout.

### Step 1 post-processing
Reads `lattice_constant.dat` files from Step 1 directories and writes summary CSV/Excel tables.

### Step 2 post-processing
Searches recursively for `log.lammps` files, extracts the last reported GB energy, and writes a summary table.

### Step 4 post-processing
Reads ECO dump files, identifies the two grain boundaries from `f_gb[2]`, writes a GB-only dump,
and exports boundary positions and migration distances.

For details, see:

- `docs/postprocess.md`
- `docs/directory-structure.md`
- `docs/python-workflow.md`

## Notes on public sharing

This repository focuses on sharing the **workflow** rather than all raw simulation data.

In general, the repository should include:

- scripts,
- templates,
- example inputs,
- documentation.

Large outputs, temporary files, and cluster-specific raw results are usually better kept out
of the public repository.

## Citation

If you use this workflow, please cite the related paper above and, if appropriate,
this repository.
