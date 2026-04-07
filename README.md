# NiCr ITB MD Workflow

This repository shares a LAMMPS-based molecular dynamics (MD) workflow for studying
incoherent twin boundaries (ITBs), with a focus on boundary structure, energy, and migration
in Ni-based alloys.

The repository is organized in three complementary parts:

1. **Templates**
   - LAMMPS input templates,
   - SLURM run templates,
   - reusable placeholders filled by Python.

2. **Minimal manual examples**
   - one small example for each of the main workflow steps,
   - intended to help a new user understand the physics and file flow
     before using the automated workflow.

3. **Python automation workflow**
   - scripts that generate many simulation folders and input files,
   - job-submission scripts for SLURM,
   - a shared queue-management helper to reduce duplicated logic.

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
5. Then read the **Python workflow** section and use the automation scripts.

This order helps users first understand the physical meaning and file dependencies of each calculation step
before using the automated workflow.

## Repository structure

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
│   └── python-workflow.md
├── templates/
├── examples/
│   ├── step1_latticeConst/
│   ├── step2_gridSearch/
│   ├── step3_equilibrate/
│   └── step4_eco/
├── scripts/
│   ├── createInput/
│   │   ├── Step1_latticeConst.py
│   │   ├── Step2_GridSearch.py
│   │   ├── Step3_EqSigma3_112.py
│   │   └── Step4_ECOSigma3_112.py
│   └── autoRun/
│       ├── job_runner.py
│       ├── autoRun_Step1_LC.py
│       ├── autoRun_Step2_GridSearch.py
│       ├── autoRun_Step3_Eq.py
│       └── autoRun_Step4_ECO_112.py
└── potentials/
```

## Python workflow section

The Python workflow is split into two parts:

### `scripts/createInput/`
These scripts read text templates and generate organized simulation folders,
LAMMPS input files, and SLURM job scripts.

### `scripts/autoRun/`
These scripts submit and monitor many jobs on a SLURM cluster. A shared helper
module (`job_runner.py`) is used so that queue polling, submission, and resubmission
logic do not have to be repeated in every script.

For details, see:

- `docs/python-workflow.md`

## Why both templates and examples are useful

The cleaned templates are useful for automation, but they still contain many variables
that are normally filled by Python scripts. For a new user, it is much easier to first
see one small example for each step.

For that reason, this repository keeps **both**:

- `templates/` for the scalable workflow,
- `examples/` for tutorial-style manual understanding.

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
