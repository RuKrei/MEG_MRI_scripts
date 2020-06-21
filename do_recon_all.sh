#!/bin/bash

export DO_RECON_FOLDER=$1
export N_JOBS=2
export FS_OPENMP=2


python -m do_recon_all.py