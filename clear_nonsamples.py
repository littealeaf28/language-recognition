from glob import glob
import os
import pandas as pd
import numpy as np


def clear_nonsamples(_df, label):
    if ~np.isnan(_df.loc[_df['Label'] == label, 'Finished Sampling'].values[0]):
        return

    print(f'Processing {label}...')

    mp3_files = glob(f'cv-corpus-6.1-2020-12-11\\{label}\\clips\\*.mp3')
    misc_files = glob(f'cv-corpus-6.1-2020-12-11\\{label}\\*.tsv')

    for mp3_file in mp3_files:
        os.remove(mp3_file)

    for misc_file in misc_files:
        os.remove(misc_file)

    _df.loc[_df['Label'] == label, 'Finished Sampling'] = True


max_lang_wav_size = 49

df = pd.read_csv('data_links.csv')

samp_df = df.loc[df['Sample Size'] > max_lang_wav_size]
[clear_nonsamples(df, label) for label in samp_df['Label'].values]

df.to_csv('data_links.csv', index=False)
