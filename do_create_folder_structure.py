import os
import shutil


subject_names = os.listdir('/home/idrael/DATA/MEG/new_patients')
new_subects_dir = '/home/idrael/DATA/MEG/new_patients'
fsaverage_sym_dir = '/home/idrael/DATA/MEG/clinic/copy_blaupause/anat'
report_files = '/home/idrael/DATA/MEG/clinic/copy_blaupause/report'




def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        shutil.copyfile(src, dest)

for subj in subject_names:
    base_dir = os.path.join('/home/idrael/DATA/MEG/clinic', subj)
    epi_subjects_dir = os.path.join(base_dir, 'derivatives', 'anat')
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    data_dir = os.path.join(base_dir, 'data')
    ana_base_dir = os.path.join(data_dir, 'anat')
    for_report_dir = os.path.join(base_dir, 'derivatives', 'for_report')
    results_dir = os.path.join(base_dir, 'derivatives', 'intermediates')
    fs_result = os.path.join(epi_subjects_dir, subj, 'mri')

    for f in [base_dir, ana_base_dir, data_dir, epi_subjects_dir, results_dir, for_report_dir]:
        if not os.path.exists(f):
            os.makedirs(f, exist_ok=True)
            print(f"Directory >> {f} << created.")

    try:
        source = os.path.join(new_subects_dir, subj)
        destination = os.path.join(ana_base_dir, subj)
        recursive_overwrite(source, destination)
    except FileNotFoundError:
        print(f"No DICOM files found for Patient: {subj}")
    
    recursive_overwrite(fsaverage_sym_dir, epi_subjects_dir)
    recursive_overwrite(report_files, for_report_dir)




