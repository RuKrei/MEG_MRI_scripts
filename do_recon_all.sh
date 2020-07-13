#!/bin/bash

export DO_RECON_FOLDER=$1
export N_JOBS=16
export FS_OPENMP=16
export SUBJECTS_DIR="/media/idrael/DATA/MEG/anat"

FREESURFER_HOME="/usr/local/freesurfer/"

python -m do_recon_all.py