#!/bin/bash
# usage = ./do_fs_folder.sh -f PATH/TO/FOLDER -sd PATH/TO/SUBJECTS_DIR -proc N_PROC
# -f flag is mandatory
# -sd flag is optional, if not set it will default to /PATH/TO/FOLDER/freesurfered
# -proc flag is optional, if not set it will default to all available CPUs
# 
# --> treats every direct subdirectory-name as a new subject
# --> runs recon-all + hippocampal subfield segmentation on every subject


# Pipeline start
# parse arguments
while [ "$1" != "" ]; do
    case $1 in
        -f | --folder )
            shift
            FOLDER=$1
        ;;
        -sd | --subjects_dir )
            shift
            SUBJ_DIR=$1
        ;;
        -s | --subjects )
            shift
            SUBJECT=$1
        ;;              
        -h | --help )
            exit
        ;;
        -p | --proc )
            shift
            N_PROC=$1
        ;; 
        * )
            exit 1
        ;;
    esac
    shift
done

# count subject names
i=1
for d in $FOLDER/*
do
    dirs[i++]="${d%/}"
done

echo ""
echo "######################################"
echo "Processing folder --> $FOLDER"
echo "######################################"
echo ""

NUM_SUBJECTS=${#dirs[@]}
echo "- There are $NUM_SUBJECTS subjects in $FOLDER"

# test, if a subject was set
if [ -z ${SUBJECT+x} ]
then
    # set to all subjects, since variable wasn't set
    SUBJECT="all"
    echo "- SUBJECT was set to 'all', since none was specified"
fi

# test, if subjects_dir was set, otherwise set default
if [ -z ${SUBJ_DIR+x} ]
then
    FS=freesurfered
    SUBJ_DIR=$FOLDER$FS
    echo "- SUBJECTS_DIR was set to $SUBJ_DIR, as no other directory was specified."
fi

# test, if proc flag was set and give info
if [ -z ${N_PROC+x} ]
then
    N_PROC=999
    echo "- Calculations will be performed with all CPUs available, as no limitation was specified."
else
    echo "- The execution will use $N_PROC parallel processes"
fi

# some info for the user...
echo "- Nifti files will be stored in subjects subfolders, as they get funny names :-)"
echo "- Freesurfer-files go to SUBJECTS_DIR."
echo "- A python3 environment with nipype and dicom2nifti is necessary to run this program"
echo " "
echo " "
echo "This will take some time...)"
echo "----------------------------"
echo " "

#  Finally, execute python command
python do_recon_all_nipype.py -f $FOLDER -sd $SUBJ_DIR -p $N_PROC -s $SUBJECT