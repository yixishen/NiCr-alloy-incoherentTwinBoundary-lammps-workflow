---
layout: default
title: Step 2 - Rigid-body grid search
---

# Step 2 — Rigid-body grid search

## Goal

The goal of this step is to identify a physically reasonable low-energy
boundary structure before running migration calculations.

## Why this step matters

Boundary structure strongly affects:

- boundary energy,
- local atomic arrangement,
- defect content near the interface,
- later migration behavior.

For this reason, it is important to avoid starting from an arbitrary boundary
translation or poorly chosen interface structure.

## What this example shows

In this tutorial example, one rigid-body grid search is performed manually
for a selected boundary type.

The purpose is to show:

- what parameter is being varied,
- how multiple trial structures are generated,
- how energy is compared across candidate structures,
- how a preferred low-energy structure is selected.

## Typical idea of a grid search

A rigid-body grid search usually works by:

1. constructing the two grains,
2. applying relative rigid-body translations between them,
3. relaxing each trial configuration,
4. comparing the resulting energies.

The lowest-energy or physically preferred structure is then used for later
production calculations.

## Example files

A minimal example may include:

- `examples/step2_gridSearch/in.example`
- `templates/in.gridSearch.template`
- one small table or output summary of trial energies

## What output to check

The user should examine:

- total energy or boundary energy for each trial,
- whether the structure relaxes cleanly,
- whether the selected minimum looks physically reasonable.

## Why this step is especially important

For interface migration studies, the measured response can depend strongly on
the initial boundary structure. A grid search helps reduce bias from an
unphysical or high-energy starting configuration.

## Common mistakes

Common mistakes include:

- comparing structures that were not relaxed consistently,
- choosing a configuration only by visual appearance,
- using too coarse a translation grid,
- failing to document which translation produced the chosen structure.

## Suggested next step

Once a low-energy structure has been selected, proceed to a single ECO-driven
migration example.
