
import csv
import pandas as pd

from config import DATA_FP


def debiteur_nummer_exist(debiteur_id: str) -> bool:
    """Checks if user_ID exist in the DB"""
    with open(DATA_FP) as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if row[0] == debiteur_id:
                return True
    return False
