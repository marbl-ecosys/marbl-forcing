#!/bin/bash
#PBS -N ESMF_RegridWeightGen
#PBS -q regular
#PBS -A NCGD0011
#PBS -l select=12:ncpus=36:mpiprocs=4:mem=109GB
#PBS -l walltime=06:00:00
#PBS -o logs/
#PBS -e logs/
#PBS -j oe

set -e

module purge
module load ncarenv/1.2
module load intel/17.0.1
module load netcdf/4.6.1
module load mpt/2.19

module load esmf_libs/7.1.0r
module load esmf-7.1.0r-ncdfio-mpi-O


METHOD=conserve
SRC_GRID=etopo1
SRC=/glade/work/mclong/esmlab-regrid/${SRC_GRID}.nc

for DST_GRID in POP_tx0.1v3 POP_gx3v7 POP_gx1v7; do
    DST=/glade/work/mclong/esmlab-regrid/${DST_GRID}.nc
    WEIGHT_FILE=/glade/work/mclong/esmlab-regrid/${SRC_GRID}_to_${DST_GRID}_conservative.nc
    if [ ! -f ${WEIGHT_FILE} ]; then
        echo ------------------------
        echo generating ${WEIGHT_FILE}
        rm -f PET*.RegridWeightGen.Log  # Remove previous log files        
        mpirun -np 48 ESMF_RegridWeightGen --netcdf4 --ignore_unmapped -s ${SRC} -d ${DST} -m ${METHOD} -w ${WEIGHT_FILE}
        echo ------------------------
        echo
    fi
done