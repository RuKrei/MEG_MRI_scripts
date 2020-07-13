import os
import sys
import subprocess


os.environ['FREESURFER_HOME'] = '/usr/local/freesurfer'
subjects_dir = '/media/idrael/DATA/Playground/watershed_test/'
subjectnames = os.listdir(subjects_dir)
subjectlist = str(subjectnames)

print('\n\n\nThe following subjects\' bem files are being processed: ' + subjectlist)

## local function used in the bash commands below
def run_process_and_write_output(command, subjects_dir):
    environment = os.environ.copy()
    environment["SUBJECTS_DIR"] = subjects_dir
    process = subprocess.Popen(command, stdout=subprocess.PIPE, env=environment)
    ## write bash output in python console
    for c in iter(lambda: process.stdout.read(1), b''):
        sys.stdout.write(c.decode('utf-8'))

for subject in subjectnames: 
    surfaces = dict(
            inner_skull=dict(
                             origin=subject + '_inner_skull_surface',
                             destination='inner_skull.surf'),
            outer_skin=dict(origin=subject + '_outer_skin_surface',
                            destination='outer_skin.surf'),
            outer_skull=dict(origin=subject + '_outer_skull_surface',
                             destination='outer_skull.surf'),
            brain=dict(origin=subject + '_brain_surface',
                       destination='brain_surface.surf')
                    )                           
   
    for surface in surfaces:
        this_surface = surfaces[surface]
        ## copy files from watershed into bem folder where MNE expects to find them
        command = ['cp', '-v',
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