import mne
import os
import subprocess
import sys

os.environ['FREESURFER_HOME'] = '/usr/local/freesurfer'
mne.utils.set_config('MNE_USE_CUDA', 'True')
MNE_USE_CUDA=True
mne.cuda.init_cuda(verbose=True)
subjects_dir = '/media/idrael/DATA/Playground/watershed_test/'
n_jobs=32

subjectnames = os.listdir(subjects_dir)
subjectlist = str(subjectnames)

print('\n\n\nThe following subjects are being evaluated: ' + subjectlist)

for subject in subjectnames:
    if not os.path.isdir(subjects_dir + subject + '/bem/watershed/'):
        mne.bem.make_watershed_bem(subject=subject, subjects_dir=subjects_dir, overwrite=True)
    else:
        print(f'Directory exists, nothing to do')


