import pandas as pd 

df = pd.read_csv('data/clean_relaties.csv')
df.to_excel('data/clean_relaties.xlsx', index=False)