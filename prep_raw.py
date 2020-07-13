#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 23:17:18 2019

@author: idrael
"""

import mne
import matplotlib.pyplot as plt
import numpy as np

print(__doc__)

data_path = '/Users/idrael/MEG/test/data/'

fname = data_path + 'short_raw_tsss.fif'

raw = mne.io.read_raw_fif(fname)

# Set up pick list: MEG + STI 014 - bad channels
want_meg = True
want_eeg = False
want_stim = False
include = ['STI 014']
# raw.info['bads'] += ['MEG 2443', 'EEG 053']  # bad channels + 2 more

picks = mne.pick_types(raw.info, meg=want_meg, eeg=want_eeg, stim=want_stim,
                       include=include, exclude='bads')

some_picks = picks[:5]  # take 5 first
start, stop = raw.time_as_index([0, 15])  # read the first 15s of data
data, times = raw[some_picks, start:(stop + 1)]

# save 150s of MEG data in FIF file
# raw.save('sample_audvis_meg_trunc_raw.fif', tmin=0, tmax=150, picks=picks,
#          overwrite=True)


#######################
# Filter


raw.load_data()
raw.filter(2,40)
picks = mne.pick_types(raw.info, meg='mag', eeg=False, eog=False,
                       stim=False, exclude='bads')

raw.plot_psd(area_mode='range', tmax=10.0, picks=picks, average=False)











###############################################################################
# Show MEG data
raw.plot()


################################
# Detect heartbeats

event_id = 999
ecg_events, _, _ = mne.preprocessing.find_ecg_events(raw, event_id, ch_name='ECG001')

picks = mne.pick_types(raw.info, meg=False, eeg=False, stim=False, eog=False,
                       include=['ECG001'], exclude='bads')
tmin, tmax = -0.1, 0.1
raw.del_proj()
epochs = mne.Epochs(raw, ecg_events, event_id, tmin, tmax, picks=picks)
data = epochs.get_data()

print("Number of detected ECG artifacts : %d" % len(data))

plt.plot(1e3 * epochs.times, np.squeeze(data).T)
plt.xlabel('Times (ms)')
plt.ylabel('ECG')
plt.show()

###############################
## Detect EOG
#
#event_id = 998
#eog_events = mne.preprocessing.find_eog_events(raw, event_id)
#
## Read epochs
#picks = mne.pick_types(raw.info, meg=False, eeg=False, stim=False, eog=True,
#                       exclude='bads')
#tmin, tmax = -0.2, 0.2
#epochs = mne.Epochs(raw, eog_events, event_id, tmin, tmax, picks=picks)
#data = epochs.get_data()
#
#print("Number of detected EOG artifacts : %d" % len(data))
#

################################
# Power spectrum density

from mne.time_frequency import psd_multitaper

tmin, tmax = 0, 60  # use the first 60s of data
fmin, fmax = 2, 100  # look at frequencies between 2 and 100Hz
n_fft = 2048  # the FFT size (n_fft). Ideally a power of 2

raw.plot_psd(area_mode='range', tmax=10.0, show=True, average=True)

# Pick MEG magnetometers in the Left-temporal region
#selection = read_selection('Left-temporal')
#picks = mne.pick_types(raw.info, meg='mag', eeg=False, eog=False, stim=False, exclude='bads', selection=selection)

# Let's just look at the first few channels for demonstration purposes
#picks = picks[:4]
#
#plt.figure()
#ax = plt.axes()
#raw.plot_psd(tmin=tmin, tmax=tmax, fmin=fmin, fmax=fmax, n_fft=n_fft,
#             n_jobs=1, proj=False, ax=ax, color=(0, 0, 1),  picks=picks,
#             show=False, average=True)
#
#raw.plot_psd(tmin=tmin, tmax=tmax, fmin=fmin, fmax=fmax, n_fft=n_fft,
#             n_jobs=1, proj=True, ax=ax, color=(0, 1, 0), picks=picks,
#             show=False, average=True)

f, ax = plt.subplots()
psds, freqs = psd_multitaper(raw, low_bias=True, tmin=tmin, tmax=tmax,fmin=fmin, 
                             fmax=fmax, proj=True, picks=picks, n_jobs=1)
psds = 10 * np.log10(psds)
psds_mean = psds.mean(0)
psds_std = psds.std(0)

ax.plot(freqs, psds_mean, color='k')
ax.fill_between(freqs, psds_mean - psds_std, psds_mean + psds_std, color='k', alpha=.5)
ax.set(title='Multitaper PSD', xlabel='Frequency',
       ylabel='Power Spectral Density (dB)')
plt.show()






