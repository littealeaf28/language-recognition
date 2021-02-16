import tarfile
import requests
import pandas as pd
import os


def download_data_link(_df, lang_data, idx, _curr_size_mb):
    if lang_data.loc['Downloaded']:
        return

    if lang_data.loc['Size (MB)'] + _curr_size_mb > download_lim_mb:
        print(f"Skipping {lang_data.loc['Language']}")
        return

    print(f"Retrieving {lang_data.loc['Language']}")
    r = requests.get(lang_data.loc['Data Link'], allow_redirects=True)

    # Download links expired, so must re-download
    if r.status_code != 200:
        print(f"Must re-download {lang_data.loc['Language']}")
        return

    print(f"Writing {lang_data.loc['Language']}")
    download_archive = f"{lang_data.loc['Label']}.tar"
    open(download_archive, 'wb').write(r.content)

    t = tarfile.open(download_archive, 'r')
    t.extractall()
    t.close()

    os.remove(download_archive)

    _df.loc[idx, 'Downloaded'] = True
    _curr_size_mb += lang_data.loc['Size (MB)']


df = pd.read_csv('data_links.csv')

# Set limit because only want to download a certain amount so don't overload computer storage
download_lim_mb = 400
curr_size_mb = 0

[download_data_link(df, lang_data, idx, curr_size_mb) for idx, lang_data in df.iterrows()]

df.to_csv('data_links.csv', index=False)
