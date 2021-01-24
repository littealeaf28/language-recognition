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

    if ~np.isnan(df.loc[df['Label'] == label, 'Num Possible Samples'].values[0]):
        continue

    print(f'Processing {label}...')

    mp3_files = glob(f'{lang_dir}\\clips\\*.mp3')

    total_size_mb = sum([os.path.getsize(mp3_file) for mp3_file in mp3_files]) / b_in_mb
    avg_size_mb = total_size_mb / len(mp3_files)

    df.loc[df['Label'] == label, 'Num Possible Samples'] = round(max_lang_mp3_size / avg_size_mb)

df.to_csv('data_links.csv', index=False)
