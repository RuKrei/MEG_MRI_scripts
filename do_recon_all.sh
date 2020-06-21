#!/bin/bash

export DO_RECON_FOLDER=$1
export N_JOBS=5
export OPENMP=5


python -m do_recon_all.py