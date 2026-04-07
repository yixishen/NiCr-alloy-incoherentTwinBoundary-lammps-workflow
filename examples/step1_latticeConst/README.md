# Step 1 example

This folder contains one **concrete manual example** for the lattice constant calculation.

## File included

- `in.step1_latticeConst_Ni90Cr_600K.example`

## What this example does

This example:

- builds an FCC alloy box,
- assigns a Ni/Cr ratio through `type/fraction`,
- minimizes the structure,
- equilibrates at 600 K with NPT,
- time-averages `lx`, `ly`, and `lz` into `lattice_constant.dat`.

## What you need to edit

Before running, check:

- the potential file exists at `../../potentials/FeNiCr_ArturV3.eam`,
- the element ordering in `pair_coeff` matches your file,
- the composition convention matches your own usage.

## Typical run command

```bash
lmp -in in.step1_latticeConst_Ni90Cr_600K.example
```
