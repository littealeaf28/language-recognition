from glob import glob
import os
import pandas as pd


def clear_unprocessed_samples(label):
    wav_files = glob(f'cv-corpus-6.1-2020-12-11\\{label}\\clips\\*.wav')

    [os.remove(wav_file) for wav_file in wav_files]


lang_dirs = glob('cv-corpus-6.1-2020-12-11\\*')

# df = pd.read_csv('data_links.csv')
# df = df.drop(columns=['Num Samples', 'Sample Size', 'Finished Sampling'])

[clear_unprocessed_samples(lang_dir[25:]) for lang_dir in lang_dirs]

# df.to_csv('data_links.csv', index=False)
