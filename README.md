# NiCr ITB MD Workflow

This repository shares a LAMMPS-based molecular dynamics (MD) workflow for studying
incoherent twin boundaries (ITBs), with a particular focus on boundary structure,
energy, and migration in Ni-based alloys.

The repository is organized in two complementary parts:

1. **Templates and automation**
   - input templates used by the Python workflow,
   - scripts that generate many simulation folders,
   - SLURM-based job submission and monitoring,
   - post-processing for repeated studies.

2. **Minimal manual examples**
   - one small example for each of the four main steps,
   - intended to help a new user understand the physics and file flow
     before using the automated workflow.

## Related paper

This workflow is associated with the following paper:

**Yixi Shen and Irene J. Beyerlein**  
*Temperature-induced migration of Σ3[112] twin boundaries in NiCr alloy*  
**Journal of Materials Science** (2025)  
DOI: [10.1007/s10853-025-11276-9](https://doi.org/10.1007/s10853-025-11276-9)

## Why both templates and examples are useful

The cleaned templates are useful for automation, but they still contain many variables
that are normally filled by Python scripts. For a new user, it is much easier to first
see one small example for each step:

1. lattice constant calculation,
2. rigid-body grid search,
3. restart-based equilibration of one selected Σ3{112} structure,
4. ECO-driven migration.

For that reason, this repository keeps **both**:

- `templates/` for the scalable workflow,
- `examples/` for tutorial-style manual understanding.

## Recommended order for new users

If you are new to this workflow, I recommend following this order:

1. Run or read the **Step 1** lattice constant example.
2. Read the **Step 2** grid-search example and parameter notes.
3. Read the **Step 3** equilibration example and understand the restart handoff.
4. Read the **Step 4** ECO example and understand what outputs are dumped.
5. Then move to the Python automation workflow.

This order helps users understand the physical meaning and file dependencies of each step
before using the automated scripts.

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
│   └── why-statistics.md
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
└── potentials/
```

## Example folders

### `examples/step1_latticeConst/`
Contains one concrete bulk-alloy example input showing how the lattice constant
calculation is run manually.

### `examples/step2_gridSearch/`
Contains notes for one representative Σ3{112} grid-search case, including the
main variables that must be specified before the template is run.

### `examples/step3_equilibrate/`
Shows how the restart from the selected boundary structure is re-equilibrated
and heated to the target temperature.

### `examples/step4_eco/`
Shows how the equilibrated restart is used for the ECO-driven migration run.

## Important note about the examples

The examples are intentionally minimal. Their purpose is to document the workflow,
file handoff, and key variables. For production studies, users should still rely on
the Python automation framework to generate consistent families of cases.

## Notes on public sharing

This repository focuses on sharing the **workflow** rather than all raw simulation data.

In general, the repository should include:

- scripts,
- templates,
- example inputs,
- documentation.

Large outputs, temporary files, and cluster-specific raw results are usually better
kept out of the public repository.

## Citation

If you use this workflow, please cite the related paper above and, if appropriate,
this repository.
