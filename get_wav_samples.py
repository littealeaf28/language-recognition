from glob import glob
import os
import pandas as pd
import numpy as np
from pydub import AudioSegment


def get_wav_samples(_df, label):
    mp3_files = glob(f'cv-corpus-6.1-2020-12-11\\{label}\\clips\\*.mp3')

    if ~np.isnan(_df.loc[_df['Label'] == label, 'Sample Size'].values[0]):
        return

    try:
        pos_num_samples = int(_df.loc[df['Label'] == label, 'Num Samples'].values[0])
    except ValueError:
        print(f'Process number of samples for {label} first!')
        return

    print(f'Generating WAV samples for {label}...')

    sample_sel = int(len(mp3_files)/pos_num_samples)

    sample_size_mb = 0
    for idx, mp3_file in enumerate(mp3_files):
        # Set random idx out of sample selection every time reach new sample selection
        if idx % sample_sel == 0:
            random_idx = np.random.randint(0, sample_sel)

        if idx % sample_sel == random_idx and sample_size_mb <= max_lang_wav_size:
            mp3_audio = AudioSegment.from_mp3(mp3_file)
            wav_file = f'{mp3_file[:-3]}wav'
            mp3_audio.export(wav_file, format='wav')
            sample_size_mb += os.path.getsize(wav_file) / b_in_mb

    _df.loc[_df['Label'] == label, 'Sample Size'] = sample_size_mb


lang_dirs = glob('cv-corpus-6.1-2020-12-11\\*')
lang_dirs = lang_dirs[:7]

b_in_mb = 2**20
max_lang_wav_size = 216

df = pd.read_csv('data_links.csv')

[get_wav_samples(df, lang_dir[25:]) for lang_dir in lang_dirs]

df.to_csv('data_links.csv', index=False)
