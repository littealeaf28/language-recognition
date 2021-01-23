from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from glob import glob
import pandas as pd


def get_nonsilence_audio(_df, label):
    mp3_files = glob(f'cv-corpus-6.1-2020-12-11\\{label}\\clips\\*.mp3')

    if _df.loc[_df['Label'] == label, 'Removed Silence'].values[0]:
        return

    print(f'Processing {label}...')

    # Removes all silence before and after speak
    for idx, mp3_file in enumerate(mp3_files):
        if idx % notif_iter == 0:
            print(f'Reached iteration {idx} of {label}...')

        mp3_audio = AudioSegment.from_mp3(mp3_file)

        nonsilent_audio_idcs = detect_nonsilent(mp3_audio, min_silence_len=int(0.05 * len(mp3_audio)),
                                                silence_thresh=-60)

        if len(nonsilent_audio_idcs) == 0:
            print(f'Check {mp3_file}...')
            continue

        last_idc = len(nonsilent_audio_idcs) - 1
        nonsilent_slice = [nonsilent_audio_idcs[0][0], nonsilent_audio_idcs[last_idc][1]]

        nonsilent_audio = mp3_audio[nonsilent_slice[0]:nonsilent_slice[1]]
        nonsilent_file = f'{mp3_file[:-3]}wav'
        nonsilent_audio.export(nonsilent_file, format='wav')

    _df.loc[_df['Label'] == label, 'Removed Silence'] = True

    _df.to_csv('data_links.csv', index=False)


notif_iter = 200

lang_dirs = glob('cv-corpus-6.1-2020-12-11\\*')
lang_dirs = lang_dirs[:2]

df = pd.read_csv('data_links.csv')

# df['Removed Silence'] = False

[get_nonsilence_audio(df, lang_dir[25:]) for lang_dir in lang_dirs]

# df.to_csv('data_links.csv', index=False)
