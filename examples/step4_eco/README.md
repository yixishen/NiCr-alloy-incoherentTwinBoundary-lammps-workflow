# Step 4 example

This folder documents one representative **ECO-driven migration** case.

## What Step 4 does

This step:

- reads the equilibrated restart from Step 3,
- performs a short equilibration at the target temperature,
- applies `fix orient/eco`,
- runs the migration simulation,
- dumps `f_gb[1]` and `f_gb[2]` together with atomic coordinates.

## Representative case label

`Ni90Cr / Σ3{112} / 600 K / ECO migration`

## Key variables to define

- `restart_file`
- `potential_file`
- `Tend`
- `eco_df`
- `cut_off`
- `oriFile`
- `total_steps`

## What a newcomer should notice

- `fix orient/eco` is the key operation in this stage,
- the dump file now includes `f_gb[1]` and `f_gb[2]`,
- this is the stage where interface motion is driven and later post-processed.

## Suggested example values

See `step4_example_parameters.txt`.
