import pandas as pd 

excel_enrique_sent = "data/Kopie van clean_relaties(1) updated.xlsx" # see whatsapp

current_used_file = "data/clean_relaties.csv" #used in prod

df = pd.read_csv(current_used_file)

new = pd.read_excel(excel_enrique_sent)

# new prod output
new.to_csv(current_used_file, index=False)
new.to_excel('data/clean_relaties.xlsx', index=False)

n_row = len(new)
print(f'succesful. Total number contacts is: {n_row}')