#!/bin/bash

# Configuration 
export DO_RECON_FOLDER=$1
export FS_OPENMP=16
export SUBJECTS_DIR="/media/idrael/DATA/MEG/anat"


python -m do_recon_all_nipype