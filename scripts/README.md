# Python scripts

This folder contains the public-facing Python workflow used to create and submit
LAMMPS runs for the four main MD workflow steps.

## `createInput/`

- `Step1_latticeConst.py`
- `Step2_GridSearch.py`
- `Step3_EqSigma3_112.py`
- `Step4_ECOSigma3_112.py`

These scripts read text templates and write case folders, LAMMPS inputs, and SLURM scripts.

## `autoRun/`

- `job_runner.py`
- `autoRun_Step1_LC.py`
- `autoRun_Step2_GridSearch.py`
- `autoRun_Step3_Eq.py`
- `autoRun_Step4_ECO_112.py`

These scripts submit and monitor jobs on a SLURM cluster.

## Public-facing cleanup principles used here

- editable settings grouped near the top,
- repo-relative paths instead of hard-coded `/home/...` paths,
- reduced duplicated queue-management logic,
- clearer directory-generation logic for Step 2,
- minimal structural changes to keep the workflow recognizable.
