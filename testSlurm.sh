#!/bin/bash

#SBATCH --time=1:30:10
#SBATCH --job-name="NUMBER"
#SBATCH --output="outNUMBER"

echo "$SLURMD_NODENAME JOB_PID=$SLURM_JOB_ID"
date