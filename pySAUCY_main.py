# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 11:51:32 2018

@author: BPCHUNG
"""

"""
NOTES:
    1. Will need to create Conda ENV to include necessary libraries
        a. This includes the read_intan_format library


"""

## Debugging and trouble shooting libraries
import time


## Special libraries for data analysis
import load_intan_rhd_format as rhd


## General Python libraries
import glob

import scipy.signal as sig
import numpy as np

import matplotlib.pyplot as plt

## ===== ===== ===== ===== =====

plt.ion()
plt.close('all')

## ===== ===== ===== ===== =====

data_fldr = "D:/EMG_Data/chung/for_analysis/bl21lb21_20171218/bl21lb21_trial1_ch1_ch16/"
ch_analysis = 8

Fs = 30000
fHi = 7500
fLo = 300

## ===== ===== ===== ===== =====
## PREPROCESS DATA
## ===== ===== ===== ===== =====


# Break out into load_data function
rhd_files = glob.glob(data_fldr + "*.rhd")

fname = rhd_files[0]

start_time = time.clock()
print("Loading: " + fname)
fdata = rhd.read_data(fname)
print("Time to load and process: %.3f s" % (time.clock() - start_time))

print("Time: %.3f - %.3f s" % (fdata['t_amplifier'][0], fdata['t_amplifier'][-1]))


## Break out into bandpass_filtfilt function
print("Filtering data...")
if fHi >= 0.5*Fs-500:
    fHi = 0.5*Fs-1000
    print("WARNING! (bandpass): fHi >= 0.5*Fs-500")
    print("Using fHi = %.2f" % fHi)
    
# Implements Hanning filter
dLen = len(fdata['amplifier_data'][ch_analysis])
if dLen < 387:
    nfir = 64
elif dLen < 771:
    nfir = 128
elif dLen < 1539:
    nfir = 256
else:
    nfir = 512
    
b_win = sig.firwin(nfir, [fLo*2/Fs, fHi*2/Fs], window='hann', nyq=Fs, pass_zero=False)
# b = b_win; a = 1 implements an "all-pole" filter
ch_wav = sig.filtfilt(b_win, 1, fdata['amplifier_data'][ch_analysis])



    

