# Step 0: Build LAMMPS on a Cluster

This page explains how to download, configure, compile, and verify a LAMMPS build on an HPC cluster using CMake. It also explains how to make sure your SLURM job uses the same environment as the one used during compilation.

---

## 1. Get the LAMMPS source code

You can either clone the official repository or download a release tarball.

### Option A. Clone with Git

```bash
git clone https://github.com/lammps/lammps.git
cd lammps
```

### Option B. Download a release tarball

```bash
wget https://download.lammps.org/tars/lammps.tar.gz
tar -xzf lammps.tar.gz
cd lammps-*
```

If your cluster blocks outbound downloads on compute nodes, do this on a login node.

---

## 2. Start from a clean environment

On clusters, the most common source of build and runtime errors is environment mismatch. Before building, clean your environment and load only what you need.

```bash
module purge
module load cmake
module list
```

Depending on your cluster, you may also need to load MPI or compiler-related modules explicitly, for example:

```bash
module load openmpi
```

or:

```bash
module load intel-oneapi-compilers
module load intel-oneapi-mpi
```

The exact module names depend on your cluster.

---

## 3. Create a separate build directory

Always build LAMMPS out of source.

```bash
mkdir build
cd build
```

If you already built before and want a completely fresh start:

```bash
cd ..
rm -rf build
mkdir build
cd build
```

This is the safest method if you changed compilers, MPI, package selections, or preset files.

---

## 4. Configure with a LAMMPS CMake preset file

LAMMPS provides preset cache scripts in `cmake/presets/`. These are loaded with `-C`.

For example:

```bash
cmake -C ../cmake/presets/basic.cmake ../cmake
```

You can also combine presets:

```bash
cmake -C ../cmake/presets/gcc.cmake -C ../cmake/presets/most.cmake ../cmake
```

Typical examples:

- `basic.cmake` : a minimal basic build
- `most.cmake` : enables many common packages
- `gcc.cmake` : GCC-oriented configuration
- other preset files may exist depending on your LAMMPS version

### Important note about presets

These preset files initialize the CMake cache. If `CMakeCache.txt` already exists, some previous settings may remain. That is why deleting the whole `build/` directory is often safer than only re-running `cmake`.

---

## 5. Compile LAMMPS

After configuration:

```bash
make -j8
```

Replace `8` with a suitable number of cores for your login/build node.

You can also use:

```bash
cmake --build . -j8
```

Both methods compile the code.

---

## 6. Clean a previous compilation

If you only want to remove compiled object files and binaries:

```bash
make clean
```

or:

```bash
cmake --build . --target clean
```

This does **not** rerun CMake and does **not** remove `CMakeCache.txt`.

If you changed:

- compiler
- MPI stack
- preset file
- package selection
- optional libraries

then do a full clean rebuild instead:

```bash
cd ..
rm -rf build
mkdir build
cd build
cmake -C ../cmake/presets/basic.cmake ../cmake
make -j8
```

---

## 7. Check which packages are enabled

There are several ways to verify which LAMMPS packages were configured and compiled.

### Check CMake cache

```bash
grep PKG_ CMakeCache.txt
```

This prints entries like:

```bash
PKG_MANYBODY:BOOL=ON
PKG_KSPACE:BOOL=ON
PKG_GPU:BOOL=OFF
```

### Check from the executable

After building, run:

```bash
./lmp -h
```

This usually shows an "Installed packages" section. This is one of the best final checks because it reflects the actual built executable.

---

## 8. Record the build environment

This is very important on clusters.

Save the following information right after a successful build:

```bash
module list
which cmake
which gcc
which g++
which mpicc
which mpicxx
gcc --version
mpicc --version
```

Also save compiler information from the CMake cache:

```bash
grep CMAKE_C_COMPILER CMakeCache.txt
grep CMAKE_CXX_COMPILER CMakeCache.txt
grep MPI_C_COMPILER CMakeCache.txt
grep MPI_CXX_COMPILER CMakeCache.txt
```

A simple way is to redirect all this information into a text file:

```bash
{
  echo "=== module list ==="
  module list 2>&1
  echo
  echo "=== compiler paths ==="
  which cmake
  which gcc
  which g++
  which mpicc
  which mpicxx
  echo
  echo "=== compiler versions ==="
  gcc --version
  mpicc --version
  echo
  echo "=== CMake cache ==="
  grep CMAKE_C_COMPILER CMakeCache.txt
  grep CMAKE_CXX_COMPILER CMakeCache.txt
  grep MPI_C_COMPILER CMakeCache.txt
  grep MPI_CXX_COMPILER CMakeCache.txt
} > build_environment.txt
```

Keep this file with your build.

---

## 9. Make sure SLURM uses the same environment as the build

This is one of the most important rules.

If you compile LAMMPS with one compiler/MPI environment and run it with a different one, you may get:

- missing library errors
- MPI launch failures
- symbol lookup errors
- segmentation faults at startup
- inconsistent performance or behavior

### Rule

Your SLURM script should load the **same environment** used during compilation.

If you built with:

```bash
module purge
module load cmake
module load openmpi
```

then your SLURM script should load the same relevant runtime/compiler/MPI environment before calling `srun` or `mpirun`.

### Example SLURM script

```bash
#!/bin/bash
#SBATCH --job-name=lammps_test
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --output=job.%j.out
#SBATCH --error=job.%j.err

module purge
module load cmake
module load openmpi

module list

LAMMPS_EXE=/path/to/lammps/build/lmp
INPUT=in.test

srun $LAMMPS_EXE -in $INPUT
```

### Better practice

Do not rely on memory. Copy the module loads directly from the environment you used when building.

If your cluster uses a different launcher, replace `srun` accordingly.

---

## 10. How to check whether your runtime environment matches the build

Inside the build directory, inspect:

```bash
grep CMAKE_C_COMPILER CMakeCache.txt
grep CMAKE_CXX_COMPILER CMakeCache.txt
grep MPI_C_COMPILER CMakeCache.txt
grep MPI_CXX_COMPILER CMakeCache.txt
```

Then, in the shell or SLURM job where you plan to run LAMMPS, check:

```bash
module list
which gcc
which g++
which mpicc
which mpicxx
mpicc --version
```

Also inspect linked libraries:

```bash
ldd ./lmp
```

If `ldd` shows anything like:

```bash
libmpi.so => not found
libstdc++.so.6 => not found
```

then the runtime environment does not match the build environment.

---

## 11. Recommended workflow

For most users on a cluster, the safest workflow is:

1. Log in to the cluster
2. `module purge`
3. Load the compiler/MPI/CMake environment you want
4. Build LAMMPS in a fresh `build/` directory
5. Save `module list` and compiler info
6. Use the same module loads in your SLURM script
7. If anything important changes, rebuild from scratch

---

## 12. Example full workflow

```bash
git clone https://github.com/lammps/lammps.git
cd lammps

module purge
module load cmake
module load openmpi

mkdir build
cd build
cmake -C ../cmake/presets/basic.cmake ../cmake
make -j8

./lmp -h

grep PKG_ CMakeCache.txt
module list
```

Then, in your SLURM script, use the same environment:

```bash
#!/bin/bash
#SBATCH --job-name=lmp_run
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=00:30:00
#SBATCH --output=slurm.%j.out

module purge
module load cmake
module load openmpi

srun /path/to/lammps/build/lmp -in in.example
```

---

## 13. Common troubleshooting notes

### Problem: `make clean` does not fix the issue

Reason: `make clean` removes compiled files only. It does not remove cached CMake settings.

Fix:

```bash
rm -rf build
```

then reconfigure and rebuild.

### Problem: LAMMPS builds, but does not run in a job

Possible reason: different MPI/compiler environment in the SLURM script.

Fix: compare `module list`, `which mpicc`, `which gcc`, and `ldd ./lmp`.

### Problem: `module spider gcc` does not show the GCC version recorded in `CMakeCache.txt`

Possible reason: GCC may be provided by the system, another module, or a default toolchain rather than as a separately loadable module.

Fix: check:

```bash
which gcc
gcc --version
```

What matters is whether the same compiler runtime is available at run time.

---

## 14. Suggested repository placement

A good documentation structure is:

- `README.md` : short quick-start instructions
- `docs/step0-build-lammps.md` : detailed build instructions
- `docs/step1-lattice-constant.md` : first scientific example
- `docs/step2-grid-search.md` : parameter search example
- `docs/step3-single-boundary.md` : one boundary workflow
- `docs/step4-why-statistics.md` : why repeated MD runs are needed

This keeps the README clean while preserving all cluster-specific details in a separate page.
