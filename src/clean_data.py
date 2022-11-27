""" 
Script runs locally to prepare data.
"""
import pandas as pd
from config import DATA_FP


def clean_input_data():
    """ 
    Run this only when new input is delivered by Enrique.
    
    See file in /home/david/code/data-champs/docudeel
    and `make_airtable_base.py`
    """
    df = pd.read_csv('data/update_relaties.csv')
    df['Code'] = df['Code'].str.replace('-', '').str.replace(' ', '')
    df = df.drop_duplicates()
    df.to_csv(DATA_FP, index=False)