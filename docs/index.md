---
layout: default
title: NiCr ITB LAMMPS workflow
---

# NiCr ITB LAMMPS workflow

A lightweight public-facing site for a research workflow built around:

- LAMMPS input generation from text templates,
- SLURM job submission and monitoring,
- post-processing of boundary-migration simulations.

## What this site covers

This site explains how to share a clean public version of a local research workflow.

## Pages

- [Getting started](getting-started.md)
- [Workflow map](workflow.md)
- [GitHub upload guide](github-guide.md)
- [Troubleshooting](troubleshooting.md)

## Recommended release philosophy

Start with the parts that are most valuable to other researchers:

1. the templates,
2. the input-generation scripts,
3. the job-submission logic,
4. a clear README,
5. one small example.

Then add post-processing scripts later after cleanup.
