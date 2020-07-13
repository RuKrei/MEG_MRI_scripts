import nipype
from nipype.interfaces.freesurfer import ReconAll
import nipype.interfaces.io as nio
import nipype.pipeline.engine as pe
import os

#do_recon_folder = '/media/idrael/DATA/MEG/4freesurfer'
do_recon_folder = os.environ['DO_RECON_FOLDER']
subjects_dir = os.environ['SUBJECTS_DIR']
#subjects_dir = os.path.join(do_recon_folder, 'derivatives/anat')
openmp = int(os.environ['FS_OPENMP'])
#openmp = 16
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


recon_pipe = pe.Workflow(name='ReconAll_Pipeline')
recon_pipe.base_dir = do_recon_folder


#Datagrabber
data = pe.MapNode(
            interface = nio.DataGrabber(infields=['subject_id'], outfields=['struct']),
            name='data', iterfield=['subject_id'])   
data.inputs.base_directory = do_recon_folder
data.iterables = [('subject_id', subjects)]
data.inputs.template = '*'
data.inputs.template_args = dict(struct = [['subject_id', 'struct']])
data.inputs.subject_id = subjects
data.inputs.sort_filelist = True
results = data.run()

data.run().outputs

#ReconAll
reconall = pe.MapNode(
    interface = ReconAll(), name='recon_all',
    iterfield=['subject_id', 'T1_files'])
reconall.inputs.subject_id = subjects
if not os.path.exists(subjects_dir):
    os.mkdir(subjects_dir)
reconall.inputs.directive = all
reconall.inputs.subjects_dir = subjects_dir
reconall.inputs.openmp = 5

recon_pipe.connect(data, 'struct', reconall, 'T1_files')


recon_pipe.run()
