---
layout: default
title: Suggested / required directory structure
---

# Suggested / required directory structure

## Why this page exists

In this workflow, directory structure is not a minor detail. It is part of the workflow logic.

The scripts do not simply process arbitrary folders. They assume:

- specific step names,
- specific temperature-folder names,
- specific model-index folders,
- specific composition and size labels,
- specific restart-file locations.

That means the directory layout below should be treated as the working contract between:

- `createInput`
- `autoRun`
- `postProcess`

## Top-level structure

```text
.
├── docs/
├── examples/
├── templates/
├── scripts/
│   ├── createInput/
│   ├── autoRun/
│   └── postProcess/
├── simulations/
├── results/
│   └── postProcess/
└── potentials/
```

## Simulation directories

```text
simulations/
├── Step1_latticeConst/<potential>/<component>/<ni_fraction>/Step1_latticeConst_<T>/<model_index>/
├── Step2_GridSearch/<component>/<boundary_type>/<potential>/<ni_fraction>/<size_label>/config<k>/<cutoff>_<dx>_<dy>_<dz>/
├── Step3_EqSigma3_112/<potential>/<ni_fraction>/<size_label>/comp<k>/Step3_EqSigma3_<T>/<model_index>/
└── Step4_ECO_112/<potential>/<ni_fraction>/<eco_df>/<size_label>/comp<k>/Step4_ECOS3_112_<eco_df>_<T>/<model_index>/
```

## Results directories

```text
results/
└── postProcess/
    ├── Step1_latticeConst/
    ├── Step2_GridSearch/
    └── Step4_ECO_112/
```

## Dependency chain

### Step 1
Independent bulk calculations used to estimate lattice constants.

### Step 2
Generates trial boundary structures and writes restart files.

### Step 3
Consumes the selected restart from Step 2 and writes a new equilibrated restart.

### Step 4
Consumes the equilibrated restart from Step 3 and writes ECO dump files.

### postProcess
Searches these step-specific directories and summarizes the outputs.

## Practical advice

If you want to change the directory structure, do it deliberately and update the Python scripts at the same time.
Otherwise, `autoRun` and `postProcess` will silently point to the wrong locations or fail to find the expected files.
