

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
print(sys.path)
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
