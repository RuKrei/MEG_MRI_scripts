#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 10:59:18 2020

@author: Rudi Kreidenhuber
"""

import mne
import os
import glob


base_dir = '/home/idrael/DATA/Playground/MEG/LAK20091989'
# base_dir = os.environ['BASE_DIR']
data_dir = os.path.join(base_dir, 'data')
derivatives_dir = os.path.join(base_dir, 'derivatives')
subjectname = os.path.split(base_dir)[-1]


rawfiles = glob.glob(data_dir + "/*_tsss.fif")
raws = dict()

print(f"\n\n##############\nSubjectcode = {subjectname} \nThe following fif-files were resampled and concatenated:\n##############\n\n")
for n, f in enumerate(rawfiles):
    print(f" - {n}: {f} \n")
    raws[n] = mne.io.read_raw(f)
    raws[n] = raws[n].crop(tmax=20).resample(350).load_data()
    print('\n\n\n\n')

raw_concat = mne.io.concatenate_raws([raws[n]])
raw_concat.resample(350)
print(f'\n\n\n\nThe new file has the following Info-Field:\n\n{raw_concat.info}')
savename = subjectname + '_concat_tsss_raw.fif'
savename = os.path.join(derivatives_dir, savename)
raw_concat.save(savename)
