

import os
import sys
import pandas as pd
from pprint import pprint as print

current_path = sys.path[0]
parent_path = os.path.dirname(current_path)
src_path = os.path.join(os.path.dirname(current_path), 'src')
sys.path.append(parent_path)
sys.path.append(src_path)
print(sys.path)
to_remove = '/home/david/code/o-nexus/assembly-line'
if to_remove in sys.path:
    sys.path.remove(to_remove)
from src.app import app
from src.clean import clean_debiteur_nummer


def test_clean_debiteur_nummer():
    inp_and_expected = [
        ('13004-ss', '13004SS'),
        (' 13004-ss', '13004SS'),
        ('13004 -ss', '13004SS'),
        (' 13004-ss', '13004SS'),
        ('13004- ss', '13004SS'),
        ('13004-Ss ', '13004SS'),
        ('13004SS', '13004SS'),
    ]
    
    for inp, exp in inp_and_expected:
        err_msg = f'Expected {exp} for {inp}'
        assert exp == clean_debiteur_nummer(user_id=inp), err_msg


def test_debiteur_nummer_unique():
    df = pd.read_csv('data/clean_relaties.csv')
    assert len(df) == df['Code'].nunique()
    
    
def test_latest_contacts_included():
    ## TODO add flask testing on /info endpoint
    response = app.test_client().get('/list_users')
    out = response.data.decode('utf-8')
    latest_contacts = ['13025BS']
    for contact in latest_contacts:
        err = f'{contact} not in {out}'
        assert contact in out, err

def test_index_route():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert "Hello" in response.data.decode('utf-8')
    