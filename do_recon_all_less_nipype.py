import nipype
from nipype.interfaces.freesurfer import ReconAll
import nipype.interfaces.io as nio
import nipype.pipeline.engine as pe
import os

do_recon_folder = '/Users/idrael/Playground/FS_Pipeline_Test'
#do_recon_folder = os.environ['DO_RECON_FOLDER']
#subjects_dir = os.environ[SUBJECTS_DIR]
subjects_dir = os.path.join(do_recon_folder, 'derivatives/anat')
#openmp = int(os.environ[OPENMP])
openmp = 1
#n_jobs = int(os.environ['N_JOBS'])

subjects = os.listdir(do_recon_folder)
print('#'*50)
print('#'*50)
print('#'*50)
print('#'*50)
print(f'The following subjects are supposed to be processed: {subjects}')
print('#'*50)
print('#'*50)
print('#'*50)
print('#'*50)


def get_dcm(subj, folder):
    for s in subj:
        files = os.walk(os.path.join(folder, s))
        return (s, files.next())

sj, rf = get_dcm(subjects, do_recon_folder)

print(sj)
print(rf)
