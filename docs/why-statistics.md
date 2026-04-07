---
layout: default
title: Why repeated simulations are needed
---

# Why repeated simulations are needed

## Main idea

The four templates in this repository are useful for understanding one complete
manual workflow, but one trajectory is usually not enough for alloy-interface
migration studies.

## Why a single run is not sufficient

The example templates themselves already show several sources of variation:

- Step 1 uses `${seed}` during alloy assignment.
- Step 2 uses `${seed}` again together with rigid-body translation variables.
- Step 3 uses `${seed}` for thermal velocity initialization.
- Step 4 depends on the equilibrated structure passed in from earlier steps.

Because local chemistry and thermal realization both matter, two runs with the
same nominal composition can still produce different migration behavior.

## What is repeated in practice

In a production study, you typically repeat over:

- multiple chemical configurations
- multiple velocity seeds
- multiple temperatures
- multiple driving-force values
- sometimes multiple candidate boundary structures

## Why automation is necessary

After Step 1–Step 4 are understood manually, the workflow becomes repetitive:

1. generate many input files,
2. place them in organized folders,
3. submit them to the cluster,
4. monitor failures,
5. collect the outputs for analysis.

That is exactly why the Python `CreateInput`, `autoRun`, and `postProcess`
scripts become important.

## Best practice for new users

Use the four manual templates to learn the workflow first. Then switch to the
automated scripts only after you understand:

- what each variable means,
- what file is passed from one step to the next,
- what output confirms that each step worked,
- what quantity you ultimately want to measure.
