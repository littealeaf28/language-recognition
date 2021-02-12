from glob import glob
import os
import pandas as pd
import numpy as np
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

# Takes in an input MP3 file, removes any silence before and after the audio, and saves it to specified output path
def extract_nonsilence(input_file, output_file):
    mp3_audio = AudioSegment.from_mp3(input_file)
    nonsilent_audio_idcs = detect_nonsilent(mp3_audio, min_silence_len=int(0.05 * len(mp3_audio)),
                                            silence_thresh=-60)

    if len(nonsilent_audio_idcs) == 0:
        os.remove(input_file)
        raise Exception(f'No audio in {input_file}')

    last_idc = len(nonsilent_audio_idcs) - 1
    nonsilent_slice = [nonsilent_audio_idcs[0][0], nonsilent_audio_idcs[last_idc][1]]

    nonsilent_audio = mp3_audio[nonsilent_slice[0]:nonsilent_slice[1]]
    nonsilent_audio.export(output_file, format='wav')


def get_wav_samples(_df, label):
    try:
        pos_num_samples = int(_df.loc[df['Label'] == label, 'Num Possible Samples'].values[0])
    except ValueError:
        print(f'Process number of samples for {label} first!')
        return

    mp3_files = glob(f'cv-corpus-6.1-2020-12-11\\{label}\\clips\\*.mp3')

    sample_size_mb = _df.loc[_df['Label'] == label, 'Sample Size'].values[0]

    if ~np.isnan(sample_size_mb) and sample_size_mb > max_lang_wav_size:
        return
    elif np.isnan(sample_size_mb):
        sample_size_mb = 0

    print(f'Generating WAV samples for {label}...')

    sample_sel = round(len(mp3_files)/pos_num_samples)
    if sample_sel == 0:
        sample_sel = 1

    for idx, mp3_file in enumerate(mp3_files):
        if sample_size_mb > max_lang_wav_size:
            break

        # Set random idx out of sample selection every time reach new sample selection
        if idx % sample_sel == 0:
            random_idx = np.random.randint(0, sample_sel)

        if idx % sample_sel == random_idx:
            sample_num = int(idx / sample_sel)
            if sample_num % notif_iter == 0:
                print(f'Reached sample {sample_num} of {label}...')

            wav_file = f'{mp3_file[:-3]}wav'
            if not os.path.exists(wav_file):
                try:
                    extract_nonsilence(mp3_file, wav_file)
                    sample_size_mb += os.path.getsize(wav_file) / b_in_mb
                except Exception as e:
                    print(e)
                    continue

    _df.loc[_df['Label'] == label, 'Sample Size'] = sample_size_mb


b_in_mb = 2**20
max_lang_wav_size = 216
notif_iter = 100

lang_dirs = glob('cv-corpus-6.1-2020-12-11\\*')
# lang_dirs = lang_dirs[:14]

df = pd.read_csv('data_links.csv')

[get_wav_samples(df, lang_dir[25:]) for lang_dir in lang_dirs]

df.to_csv('data_links.csv', index=False)
