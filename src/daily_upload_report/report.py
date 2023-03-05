#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Send a report of airtable uploads
"""

import datetime as dt
import pandas as pd

from email import send_plain_email
# for local dev go to src/daily_upload_report
from fancy_html import build_table, get_greeting
from airtable import Airtable
import os
AIRTABLE_TOKEN = os.environ["AIRTABLE_TOKEN"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]



AT = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TOKEN)

def _get_date_str(n_days_ago: int) -> str:
    date = (dt.datetime.today() - dt.timedelta(days=n_days_ago))
    return date.strftime('%Y-%m-%d')


def _keep_days(df: pd.DataFrame, n_days_ago: int = 1) -> pd.DataFrame:
    dates_report = [_get_date_str(x) for x in range(0, n_days_ago+1)]
    needs_report = df['date_upload'].str.split(' ', expand=True).isin(dates_report)
    out = df.loc[needs_report, :]
    return out
    
# ex = pd.DataFrame(dict(date_upload=['2023-03-05 16:22']))    
# out['date_upload'].str.split(' ',expand=True).isin(today_or_yesterday)

def get_data(n_days: int) -> pd.DataFrame:
    # https://support.airtable.com/hc/en-us/articles/4405741487383-Understanding-Airtable-IDs
    res = AT.get('uploads_new')
    df = pd.DataFrame(res['records'])
    out = pd.DataFrame.from_records(df['fields']).dropna(how='all')
    out = _keep_days(df=out, n_days_ago=n_days)
    return out


def run_report(n_days: int=1):
    df = get_data(n_days=n_days)
    # select last 24 hours * n_days
    no_new_records = df.empty
    if no_new_records:
        bericht = get_greeting(empty=True)
    else:
        bericht = get_greeting(empty=False)
        out = out.rename(columns={'date_upload': 'Tijd geüpload',
                                  'customer_id': 'Bedrijfsnaam',
                                  'description': 'Omschrijving'})
        bericht += build_table(out, color='blue_light')
        today_str = dt.datetime.today().strftime("%Y-%m-%d")
    send_plain_email(bericht, subject=f'Docudeel Uploads {today_str}')


if __name__ == '__main__':
    run_report(n_days=1)