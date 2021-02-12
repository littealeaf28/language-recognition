from ffmpeg_normalize import FFmpegNormalize
from glob import glob
import os


def add_norm_file(_norm, input_file):
    file_dir_index = input_file.rindex('\\') + 1
    file_dir = input_file[:file_dir_index]
    file_name = input_file[file_dir_index:]

    file_dir += 'norm-clips\\'
    output_file = file_dir + file_name
    print(output_file)

    # norm.add_media_file(input_file, output_file)


def add_norm_dir(_norm, lang_dir):
    if not os.path.exists(f'{lang_dir}\\norm-clips'):
        os.mkdir(f'{lang_dir}\\norm-clips')

    wav_files = glob(f'{lang_dir}\\clips\\*.wav')

    [add_norm_file(_norm, wav_file) for wav_file in wav_files]


norm = FFmpegNormalize()

lang_dirs = glob('cv-corpus-6.1-2020-12-11\\*')
lang_dirs = lang_dirs[:1]

[add_norm_dir(norm, lang_dir) for lang_dir in lang_dirs]

# norm.run_normalization()
