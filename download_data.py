import requests
import pandas as pd

df = pd.read_csv('data_links.csv')

# Iterate through df rows to find languages that haven't yet been downloaded and ensure a reasonable
df = df[~df['Downloaded']]
# print(df.loc[1, 'Data Link'])
data_link = df.loc[0, 'Data Link']

r = requests.get(data_link, allow_redirects=True)

open('a.tar', 'wb').write(r.content)

# print(df)
