
import csv

import os
from config import DATA_FP
import logging
from airtable import Airtable

try:
    AIRTABLE_TOKEN = os.environ["AIRTABLE_TOKEN"]
    AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]

except ImportError:
    # local dev
    from config import AIRTABLE_TOKEN, AIRTABLE_BASE_ID




def debiteur_nummer_exist(debiteur_id: str) -> bool:
    """Checks if user_ID exist in the DB"""
    with open(DATA_FP) as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if row[0] == debiteur_id:
                return True
    return False


def insert_record(customer_id: str,
                  comment: str,
                  dc_client_id: str ='ras_admin') -> bool:
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    data =      {'customer_id': customer_id,
                 'dc_client_id': dc_client_id,
                 'date_upload': today,
                 'comment': comment
                 }
    try:
        AT = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TOKEN)
        AT.create('uploads_new', data)
        return True
    except Exception as exception:
        exception_name = type(exception).__name__
        logging.exception(exception_name)
    return False


if __name__ == '__main__':
    # print(debiteur_nummer_exist('000000000'))
    # print(debiteur_nummer_exist('000000001'))
    print(insert_record(customer_id='000000000', comment='test'))