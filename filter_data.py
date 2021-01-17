import tarfile
import os
from glob import glob

raw_data_files = glob('*.tar')

for raw_data_file in raw_data_files:
    print(f'Extracting {raw_data_file}...')

    t = tarfile.open(raw_data_file, 'r')
    t.extractall()
    t.close()

    os.remove(raw_data_file)
