# MEG_MRI_scripts

Contains utility-scripts for processing MRI and MEG files, some of them fresh, others outdated.

#### do_fs_folder.sh
- Executes do_recon_all_nipype.py 
- runs either on all subjects, or on a specified subset
- can be to run in parallel mode, or sequential
- Converts DICOM-Subfolders to nifti
- runs freesurfer (recon-all)
- runs SegmentHA_T1.sh (hippocampal subfield segmentation)

#### prepare_new_patients.sh
- utiliy script to put the data where I want it to be :-)
