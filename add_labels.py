import pandas as pd
import re


def get_label(row):
    matches = re.findall("\/(.*?)\.", row.loc['Data Link'])
    return matches[2]


df = pd.read_csv('data_links.csv')

df['Label'] = df.apply(lambda row: get_label(row), axis=1)

df.to_csv('data_links.csv', index=False)
