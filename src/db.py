
import csv

import os
from config import DATA_FP
import logging
from airtable import Airtable


AIRTABLE_TOKEN = os.environ["AIRTABLE_TOKEN"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]


def list_debiteur_numbers() -> list:
    """Returns list of debiteur numbers"""
    with open(DATA_FP) as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for i, row in enumerate(reader)
                if i > 0]


def debiteur_nummer_exist(debiteur_id: str) -> bool:
    """Checks if user_ID exist in the DB"""
    with open(DATA_FP) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == debiteur_id:
                return True
    return False


def insert_record(customer_id: str,
                  comment: str,
                  dc_client_id: str ='ras_admin') -> bool:
    """Inserts record into Airtable for tracking purposes"""
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d %H:%M')
    data =      {'customer_id': customer_id,
                 'dc_client_id': dc_client_id,
                 'date_upload': today,
                 'comment': comment
                 }
    try:
        AT = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TOKEN)
        AT.create('uploads_new', data)
        return True
    except AttributeError:
        print('Airtable is not available')
        return False
    except Exception as exception:
        exception_name = type(exception).__name__
        logging.exception(exception_name)
    return False


if __name__ == '__main__':
    # print(debiteur_nummer_exist('000000000'))
    # print(debiteur_nummer_exist('000000001'))
    print(insert_record(customer_id='000000000', comment='test'))