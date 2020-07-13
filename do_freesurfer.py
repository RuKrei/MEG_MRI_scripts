import mne
import os
import subprocess
import sys

os.environ['FREESURFER_HOME'] = '/usr/local/freesurfer'
mne.utils.set_config('MNE_USE_CUDA', 'True')
MNE_USE_CUDA=True
mne.cuda.init_cuda(verbose=True)
todo_fs_dir = '/media/idrael/DATA/Playground/watershed_test/'
n_jobs=32

fs_subjectsdir = '/media/idrael/DATA/Playground/freesurfer_pipe_test/surfered'
todo_subjectsdir = '/media/idrael/DATA/MEG/4freesurfer/'
subjectnames = os.listdir(todo_subjectsdir)
subjectlist = str(todo_subjectsdir)


def getfirstfile(folder):
    for topdir, dirs, files in os.walk(folder, topdown=True):
        dirs[:] = [d for d in dirs if d.startswith('1')]
        for dir in dirs:
            firstfile = sorted(files)[:]

#            with (os.scandir(folder) as files) if folder.startswith('1'):
#                for file in files:
#                    if file.is_file():
#                       return file.path
            print(firstfile)
print('Folgende MRIs werden prozessiert: ' + str(subjectnames))

subjects = dict()
for name in subjectnames:
    dcmfile = getfirstfile(todo_subjectsdir + name)
    print(dcmfile)






"""
print('\n\n\nThe following subjects are being evaluated: ' + subjectlist)

for subject in subjectnames:
## local function used in the bash commands below
    def run_process_and_write_output(command, subjects_dir):
        environment = os.environ.copy()
        environment["SUBJECTS_DIR"] = subjects_dir
        process = subprocess.Popen(command, stdout=subprocess.PIPE, env=environment)
    ## write bash output in python console
        for c in iter(lambda: process.stdout.read(1), b''):
            sys.stdout.write(c.decode('utf-8'))

    command = ['recon-all -i ' dcmfile, '-subject ', subject, '-openmp 4 -all',
                os.path.join(subjects_dir, subject, 'bem', 'watershed', this_surface['origin']),
                os.path.join(subjects_dir, subject, 'bem', this_surface['destination'])
                ]
        run_process_and_write_output(command, subjects_dir)  
        

##################################################################################
##### Solution + segmentation according to:
# Pipeline for group analysis of MEG data - operations functions
# @author: Lau Møller Andersen
# @email: lau.moller.andersen@ki.se | lau.andersen@cnru.dk
# @github: https://github.com/ualsbombe/omission_frontiers.git

"""