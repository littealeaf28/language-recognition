from glob import glob
import os

label = 'ab'
wav_files = glob(f'cv-corpus-6.1-2020-12-11\\{label}\\clips\\*.wav')

total_size_mb = 0
for wav_file in wav_files:
    print(os.path.getsize(wav_file) / 2**20)
    total_size_mb += os.path.getsize(wav_file) / 2**20

print(total_size_mb)
