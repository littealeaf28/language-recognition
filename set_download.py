# Script to fix my mistake when playing around with data_links.csv, so need to reset Downloaded field for data frame

from glob import glob
import pandas as pd

audio_dirs = glob("cv-corpus-6.1-2020-12-11/*")
df = pd.read_csv("data_links.csv")

for audio_dir in audio_dirs:
    label = audio_dir[25:]
    df.loc[df['Label'] == label, 'Downloaded'] = True

df.to_csv("data_links.csv", index=False)
