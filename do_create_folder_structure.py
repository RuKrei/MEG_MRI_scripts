import os


subject_names = ['MJ16061975', 'LAK20091989', 'WF14031952', 'MA17011989', 'PP05071984', 'LM13011946']



for subj in subject_names:
    base_dir = os.path.join('/media/idrael/DATA/MEG/clinic', subj)
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



