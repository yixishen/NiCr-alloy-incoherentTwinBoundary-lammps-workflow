---
layout: default
title: Step 3 - ECO single-case migration
---

# Step 3 — ECO single-case migration

## Goal

The goal of this step is to run one manual migration simulation for a selected
boundary structure using the ECO-based driving-force setup.

## Why this step matters

Before moving to automated large-scale studies, it is useful to understand one
single case in detail:

- how the input is built,
- how the driving force is introduced,
- what the trajectory looks like,
- how migration is measured from the output.

## What this example shows

This example demonstrates one boundary type, one composition, one temperature,
and one manual ECO-driven migration case.

The user should learn:

- the layout of the migration input file,
- how the selected low-energy structure is reused,
- what parameters control the run,
- how the moving boundary is monitored.

## Typical input ingredients

A typical ECO migration case may include:

- the selected minimized boundary structure,
- equilibration at the target temperature,
- definition of the orientational driving-force setup,
- output of structural snapshots and thermodynamic quantities.

## What to look for in the output

Useful quantities to monitor include:

- whether the boundary remains stable,
- whether migration is observable,
- the boundary position as a function of time,
- whether the motion appears smooth, jerky, or stepwise.

## Why manual understanding comes first

A single manual example helps users understand the physical meaning of the run
before automation hides the details behind loops and templates.

## Common mistakes

Common mistakes include:

- using a structure that was not prepared consistently,
- mixing boundary types or directions unintentionally,
- choosing a temperature or driving force that produces no measurable motion,
- failing to save outputs needed for later velocity analysis.

## Suggested next step

Once one manual ECO case is understood, the next step is to inspect the output
and extract quantities such as position and migration velocity.
