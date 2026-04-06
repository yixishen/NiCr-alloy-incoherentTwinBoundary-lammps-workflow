---
layout: default
title: Why repeated simulations are needed
---

# Why repeated simulations are needed

## Main idea

For this type of molecular dynamics study, one simulation is usually not enough
to characterize boundary migration behavior.

A single run can depend on the local atomic configuration and on the initial
thermal state. Therefore, repeated simulations are needed to obtain more
meaningful trends.

## Why this matters here

In alloy systems, the atomic arrangement near the boundary can vary from one
configuration to another.

In finite-temperature MD, the initial velocity assignment also changes the
thermal realization.

As a result, two runs with the same global composition may still produce
different migration responses.

## Sources of variation

### 1. Local chemical distribution

Different local solute arrangements can influence:

- boundary structure,
- boundary energy,
- migration pathway,
- migration velocity.

### 2. Initial thermal state

Different random seeds for the initial velocities can lead to different
trajectories, especially when migration is thermally activated.

### 3. Boundary-specific local environment

Even two boundaries inside the same simulation cell may behave differently if
the local environment along their migration paths differs.

## What a single manual example is still useful for

A single example is still important because it helps users understand:

- the physics of the setup,
- the structure of the input files,
- the meaning of the output,
- how migration is measured.

But it should not be treated as a complete statistical result.

## Why automation is needed

Once repeated simulations are required, manual folder creation and job
submission become inefficient and error-prone.

Automation helps by:

- generating many inputs from templates,
- organizing directory trees systematically,
- submitting jobs in batches,
- monitoring failures,
- simplifying post-processing.

## How this repository handles repetition

This workflow separates repeated studies into three parts:

### CreateInput

Generate folders and inputs for many cases.

### autoRun

Submit and monitor repeated jobs on a SLURM cluster.

### postProcess

Collect energies, positions, and velocities from many outputs.

## Practical recommendation

Use the tutorial pages first to understand one calculation.

Then use the automated workflow when studying:

- multiple temperatures,
- multiple seeds,
- multiple chemical distributions,
- multiple boundary structures or potentials.
