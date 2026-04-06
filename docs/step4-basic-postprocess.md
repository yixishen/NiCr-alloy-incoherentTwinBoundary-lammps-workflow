---
layout: default
title: Step 4 - Basic post-processing
---

# Step 4 — Basic post-processing

## Goal

The goal of this step is to inspect the output from one migration simulation and
extract the quantities needed for interpretation.

## Why this step matters

A simulation is not useful unless the output can be converted into meaningful
quantities such as:

- boundary energy,
- boundary position,
- migration distance,
- migration velocity,
- comparison across conditions.

## What this example shows

This tutorial page focuses on the logic of post-processing one case manually.

The main objectives are to show:

- which output files matter,
- how to locate the boundary in the saved data,
- how to convert boundary position versus time into migration velocity,
- what kind of plots or tables are useful.

## Typical outputs to inspect

Depending on the workflow, these may include:

- `log.lammps`
- dump or trajectory files
- intermediate text files written during the run
- processed CSV or text summaries

## Common measurements

Typical measurements in this step include:

### Boundary position
Determine the interface location as a function of time.

### Migration distance
Convert position changes into total displacement.

### Migration velocity
Estimate velocity from the slope of position versus time, possibly after
excluding transient or noisy segments.

## Why this step is useful before automation

Manual post-processing of one case helps users understand what the automated
post-processing scripts are actually doing and what assumptions they rely on.

## Common mistakes

Common mistakes include:

- measuring the wrong interface,
- mixing two boundaries in one cell,
- fitting noisy data without checking the trajectory,
- treating a single realization as a final statistical result.

## Suggested next step

After understanding one case manually, read the page on why repeated
simulations are needed for statistical studies.
