#!/usr/bin/python

import glob
#import nipype
from nipype.interfaces.freesurfer import ReconAll
from dicom2nifti import convert_directory
import os
import argparse
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
import subprocess


# grab parsed arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--folder', type=str)
parser.add_argument('-s', '--subject', type=str)
parser.add_argument('-sd', '--subjects_dir', type=str)
parser.add_argument('-p', '--proc', type=int)

args = parser.parse_args()

if args.proc == 999:
    n_jobs=mp.cpu_count()
else:
    n_jobs=args.proc

print(" ")
print("######################################")
print(f"Now running do_recon_all_nipype.py with {n_jobs} streams")
print(f" - there are {mp.cpu_count()} processors available on your computer.")
print("######################################")
print(" ")

subject = args.subject
subjects_dir = args.subjects_dir

if subjects_dir == None:
    subjects_dir = os.path.join(args.folder, "freesurfered")

# get a list of available subjects
subject_list = os.listdir(args.folder)

#make sure desired subject exists, if one was specified
if subject != "all":
    assert (subject in subject_list), f"Your desired subject ({subject}) does not exist in {args.folder}."
    subject_list = [subject]
    
if subject == "all":
    print(f"\n\n\nBaseline folder contents are:\n{subject_list}\n--> those will be treated as Subjects")
    

# convert Dicom-folder to nifti-file
def convert_dcm_folder(subject=None):
    try:
        anafolder = os.path.join(args.folder, subject)
        folder = str(glob.glob((anafolder + '/1*/100*/100*'), recursive=True)[0])
        convert_directory(folder, anafolder, compression=True, reorient=True)
        return f"{subject} - DICOM folder converted to .nii.gz"
    except Exception as e:
        print(e)


# start a process for every subject
with ProcessPoolExecutor(max_workers=n_jobs) as executor:
    res = executor.map(convert_dcm_folder, subject_list)
    for r in res:
        print(r)


# run recon-all + hippocampal subfield segmentation on nifti-file
# helpers
def run_recon_all(subject=None, subjects_dir=subjects_dir, openmp=1):
    reconall = ReconAll()
    if not os.path.isdir(subjects_dir):
        print(f"Subjects directory {subjects_dir} does not exist, creating it.")
        os.mkdir(subjects_dir)
    if not os.path.isdir(os.path.join(subjects_dir, subject, "mri")):    
        anafolder = os.path.join(args.folder, subject)
        # catch error, if no .nii exists
        try:
            nii_file = glob.glob(anafolder + "/*.nii*")[0]
            reconall.inputs.subject_id = subject
            reconall.inputs.T1_files = nii_file
            reconall.inputs.directive = 'all'
            reconall.inputs.subjects_dir = subjects_dir
            reconall.inputs.openmp = openmp
            reconall.inputs.flags = "-3T"
            return f"Now running recon-all for subject {subject}."
            reconall.run()
        except Exception as e:
            print(e)
    else:
        print(f"A freesurfer segmentation of subject {subject} already exists in {subjects_dir} - aborting")

with ProcessPoolExecutor(max_workers=n_jobs) as executor:
    res = executor.map(run_recon_all, subject_list)
    for r in res:
        print(r)

# Hippocampal subfield segmentation
# helper
def run_shell_command(command):
    subprocess.run(command, shell=True, capture_output=True, check=True)

def do_hippo_seg(subject, subjects_dir=subjects_dir):
    hippofile = os.path.join(subjects_dir, subject, "mri", "lh.hippoSfVolumes-T1.v21.txt")
    if not os.path.isfile(hippofile):
        print(f"Now running hippocampal segmentation for subject: {subject}")
        hipposeg = f"segmentHA_T1.sh {subject} {subjects_dir}"
        run_shell_command(hipposeg)
        return f"{subject} - Hippocampal subfield segmentation completed"  
    else:
        print(f"Omitting hippocampal segmentation for subject {subj}, as it already exists")

with ProcessPoolExecutor(max_workers=n_jobs) as executor:
    res = executor.map(do_hippo_seg, subject_list)
    for r in res:
        print(r)