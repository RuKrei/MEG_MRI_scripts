import nipype.pipeline.engine as pe
from nipype.interfaces.freesurfer import ReconAll
import os
import glob

do_recon_folder = os.environ['DO_RECON_FOLDER']
#subjects_dir = os.environ[SUBJECTS_DIR]
openmp = int(os.environ['FS_OPENMP'])

# Overwrite env-variable input?
#do_recon_folder = '/Users/idrael/Playground/FS_Pipeline_Test'
subjects_dir = os.environ['SUBJECTS_DIR']


subjects = os.listdir(do_recon_folder)
for s in subjects:
    if '.DS_Store' in s or 'derivat' in s:
        subjects.remove(s)

def append_dcm_dir(s):
    subjects_base = os.path.join(do_recon_folder, s)
    try:
        counter = 1
        for file in glob.glob((subjects_base + '/1*/**/1000*'), recursive=True):
            do_recon_dict[s] = file
            counter += 1
            if counter > 4:
                return file
                break
    except OSError as e:
        print(e)

do_recon_dict = dict()
for s in subjects:
    do_recon_dict[s] = []
    do_recon_dict[s] = append_dcm_dir(s)
for s in subjects:
    print(do_recon_dict[s])

print('#'*50)
print('#'*50)
print('#'*50)
print('#'*50)
print(f'The following subjects are supposed to be processed: {subjects}')
print('#'*50)
print('#'*50)
print('#'*50)
print('#'*50)

#ReconAll
if not os.path.exists(subjects_dir):
    os.mkdir(subjects_dir)
for key in do_recon_dict:
    if do_recon_dict[key] == None:
        print(f'ReconAll for SUBJECT {key} FAILED - no dicom file found')
    else:
        reconall = ReconAll()
        reconall.inputs.subject_id = key
        reconall.inputs.T1_files = do_recon_dict[key]
        reconall.inputs.directive = 'all'
        reconall.inputs.subjects_dir = subjects_dir
        reconall.inputs.openmp = openmp
        reconall.run()