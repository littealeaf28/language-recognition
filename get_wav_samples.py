from glob import glob
import os
import pandas as pd
import numpy as np
from pydub import AudioSegment

label = 'ab'
mp3_files = glob(f'cv-corpus-6.1-2020-12-11\\{label}\\clips\\*.mp3')

# load
df = pd.read_csv('data_links.csv')
pos_num_samples = int(df.loc[df['Label'] == label, 'Num Samples'].values[0])

# If pos_num_samples is nan cancel

sample_sel = int(len(mp3_files)/pos_num_samples)

total_size_mb = 0
for idx, mp3_file in enumerate(mp3_files):
    # Set random idx out of sample selection every time reach new sample selection
    if idx % sample_sel == 0:
        random_idx = np.random.randint(0, sample_sel)

    if idx % sample_sel == random_idx and total_size_mb <= 18:
        mp3_audio = AudioSegment.from_mp3(mp3_file)

        wav_file = mp3_file
        wav_file = f'{wav_file[:-3]}wav'

        mp3_audio.export(wav_file, format='wav')

        total_size_mb += os.path.getsize(mp3_file) / 2 ** 20

print(total_size_mb)

# TODO: Generalize to all row entries and mark it as complete
