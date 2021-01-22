from glob import glob
import os
import pandas as pd
import numpy as np

lang_dirs = glob('cv-corpus-6.1-2020-12-11\\*')

b_in_mb = 2**20
max_lang_mp3_size = 18

df = pd.read_csv('data_links.csv')

for lang_dir in lang_dirs:
    label = lang_dir[25:]

    if ~np.isnan(df.loc[df['Label'] == label, 'Num Samples'].values[0]):
        continue

    print(f'Processing {label}...')

    mp3_files = glob(f'{lang_dir}\\clips\\*.mp3')

    total_size_b = 0
    for mp3_file in mp3_files:
        total_size_b += os.path.getsize(mp3_file)

    total_size_mb = total_size_b / b_in_mb
    avg_size_mb = total_size_mb / len(mp3_files)

    num_wav_files = round(max_lang_mp3_size / avg_size_mb) + 1

    df.loc[df['Label'] == label, 'Num Samples'] = num_wav_files

df.to_csv('data_links.csv', index=False)
