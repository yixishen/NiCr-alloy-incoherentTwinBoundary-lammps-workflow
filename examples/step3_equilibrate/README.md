# Step 3 example

This folder documents one representative **restart-based equilibration** case.

## What Step 3 does

This step:

- reads the restart written in Step 2,
- minimizes the selected boundary structure again,
- applies box relaxation,
- ramps temperature from `Tstart` to `Tend`,
- equilibrates at the target temperature,
- writes a new restart for the ECO run.

## Representative case label

`Ni90Cr / Σ3{112} / 600 K equilibration`

## Key variables to define

- `restart_file`
- `potential_file`
- `Tend`
- `Tstep`
- `seed`
- `modelNum`
- `Comp`
- `NiFrac`
- `size`
- `comp_index`

## File handoff into the next step

The important output of Step 3 is the final restart:

```text
restart.${Comp}_${NiFrac}_sig3_112_${size}_comp${comp_index}_${Tend}K
```

That restart becomes the input to Step 4.

## Suggested example values

See `step3_example_parameters.txt`.
