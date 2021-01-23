import tarfile
import requests
import pandas as pd
import os

df = pd.read_csv('data_links.csv')

# df = df[~df['Downloaded']]

download_lim_mb = 70

curr_size_mb = 0

# Iterate through df rows to find languages that haven't yet been downloaded and ensure a reasonable
for idx, row in df.iterrows():
    if row.loc['Downloaded']:
        continue

    # Only want to download a certain amount so don't overload computer storage
    if row.loc['Size (MB)'] + curr_size_mb > download_lim_mb:
        print(f"Skipping {row.loc['Language']}")
        continue

    print(f"Retrieving {row.loc['Language']}")
    r = requests.get(row.loc['Data Link'], allow_redirects=True)

    # Download links expired, so must re-download
    if r.status_code != 200:
        print(f"Must re-download {row.loc['Language']}")
        continue

    print(f"Writing {row.loc['Language']}")

    download_file_name = f"{row.loc['Label']}.tar"

    open(download_file_name, 'wb').write(r.content)

    t = tarfile.open(download_file_name, 'r')
    t.extractall()
    t.close()

    os.remove(download_file_name)

    df.loc[idx, 'Downloaded'] = True
    curr_size_mb += row.loc['Size (MB)']

df.to_csv('data_links.csv', index=False)
