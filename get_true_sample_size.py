from glob import glob
import os
import pandas as pd

## Written to check -- caught a bug with

def get_true_sample_size(_df, label):
    wav_files = glob(f'cv-corpus-6.1-2020-12-11\\{label}\\clips\\*.wav')

    _df.loc[_df['Label'] == label, 'Sample Size'] = sum([os.path.getsize(wav_file) for wav_file in wav_files]) / b_in_mb


b_in_mb = 2**20

df = pd.read_csv('data_links.csv')

[get_true_sample_size(df, label) for label in df['Label'].values]

df.to_csv('data_links.csv', index=False)