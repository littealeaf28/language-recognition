import tarfile

import requests
import pandas as pd
import os

df = pd.read_csv('data_links.csv')

df = df[~df['Downloaded']]

download_file_name = 'download.tar'
download_lim_mb = 5000

curr_size_mb = 0

# Iterate through df rows to find languages that haven't yet been downloaded and ensure a reasonable
for idx, row in df.iterrows():
    # Only want to download a certain amount
    if row.loc['Size (MB)'] + curr_size_mb > download_lim_mb:
        continue

    r = requests.get(row.loc['Data Link'], allow_redirects=True)
    print(r)

    if r.status_code != 200:
        print(f"Must re-download {row.loc['Language']}")
        continue

    print(f"Downloading {row.loc['Language']}")
    open(download_file_name, 'wb').write(r.content)

    t = tarfile.open(download_file_name, 'r')
    t.extractall()

    df.loc[0, 'Downloaded'] = True
    os.remove(download_file_name)
    curr_size_mb += row.loc['Size (MB)']
