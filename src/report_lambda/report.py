#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Send a report of airtable uploads
"""

import datetime as dt
import pandas as pd

try:
    from fancy_html import build_table, get_greeting
    from airtable import Airtable
    import os
    AIRTABLE_TOKEN = os.environ["AIRTABLE_TOKEN"]
    AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]

except ImportError:
    # local dev
    from lambdas.daily_upload_report.fancy_html import build_table, get_greeting
    from cdk_infra.config import AIRTABLE_TOKEN, AIRTABLE_BASE_ID
    from lambdas.daily_upload_report.airtable import Airtable


AT = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TOKEN)

def _extract_name(x) -> str:
    if isinstance(x, list):
        return x[0]
    return 'onbekend'


def get_data() -> pd.DataFrame:
    # https://support.airtable.com/hc/en-us/articles/4405741487383-Understanding-Airtable-IDs
    res = AT.get('Ras-Admin -> Uploads')
    df = pd.DataFrame(res['records'])
    out = pd.DataFrame.from_records(df['fields'])
    deb_name = out['Name (from DEBITEUREN_NUMMER)'].map(_extract_name)
    dt_created = pd.to_datetime(out['DateTimeCreated'], utc=True).dt.tz_convert('Europe/Amsterdam')
    description = out['Description']
    df = pd.DataFrame(dict(deb_name=deb_name,
                           dt_created=dt_created,
                           description=description))
    return df


def run_report(n_days:int=1):
    df = get_data()
    # select last 24 hours * n_days
    n_days = 1
    dt_yesterday = dt.datetime.now()-dt.timedelta(hours=24*n_days)
    out = df.set_index('dt_created').sort_index()[dt_yesterday:].reset_index()
    # formatting
    out['dt_created'] = out['dt_created'].astype(str).str[:19]
    out = out.rename(columns={'dt_created': 'Tijd geüpload',
                              'deb_name': 'Bedrijfsnaam',
                              'description': 'Omschrijving'})
    bericht = get_greeting(empty=out.empty)
    styled_html = bericht + build_table(out, color='blue_light')
    today_str = dt.datetime.today().strftime("%-d/%-m/%Y")
    data =      {'Date': today_str,
                 'HTML': styled_html,
                 'EMAIL': 'info@rasadministrative.com',
                 #TODO extract business from email or so
                 'Business': 'Ras-administrative'
                 }
    AT.create('Ras-Admin -> Reports', data)
    print('Finished inserting data')


if __name__ == '__main__':
    df = get_data()
    # select last 24 hours
    dt_yesterday = dt.datetime.now()-dt.timedelta(hours=16*30)
    out = df.set_index('dt_created').sort_index()[dt_yesterday:].reset_index()
    # formatting
    out['dt_created'] = out['dt_created'].astype(str).str[:19]
    out = out.rename(columns={'dt_created': 'Tijd geüpload',
                              'deb_name': 'Bedrijfsnaam',
                              'description': 'Omschrijving'})
    bericht = get_greeting(empty=out.empty)
    styled_html = bericht + build_table(out, color='blue_light')
    with open('styled2.html', 'w') as f:
        f.write(styled_html)
    # put to airtable
    data =      {'customer_id': '13004SS',
                 'dc_client_id': 'ras_admin',
                 'date_upload': 'today',
                 'n_doc': 1,
                 }

    AT.create('uploads_new', data)
