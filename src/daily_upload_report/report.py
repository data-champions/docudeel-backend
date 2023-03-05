#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Send a report of airtable uploads
"""

import datetime as dt
import os
from typing import List

from airtable import Airtable
import pandas as pd

# for local dev go to src/daily_upload_report
from fancy_html import build_table, get_greeting
from report_email import send_plain_email


AIRTABLE_TOKEN = os.environ["AIRTABLE_TOKEN"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]
AT = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TOKEN)


def _get_date_str(n_days_ago: int) -> str:
    date = (dt.datetime.today() - dt.timedelta(days=n_days_ago))
    return date.strftime('%Y-%m-%d')


def _keep_days(df: pd.DataFrame, n_days_ago: int = 1) -> pd.DataFrame:
    dates_report = [_get_date_str(x) for x in range(0, n_days_ago+1)]
    needs_report = df['date_upload'].str.split(' ').str[0].isin(dates_report)
    out = df.loc[needs_report, :]
    return out
    

def get_data(n_days: int) -> pd.DataFrame:
    # https://support.airtable.com/hc/en-us/articles/4405741487383-Understanding-Airtable-IDs
    res = AT.get('uploads_new')
    df = pd.DataFrame(res['records'])
    if df.empty:
        return df
    df = pd.DataFrame.from_records(df['fields']).dropna(how='all')
    out = _keep_days(df=df, n_days_ago=n_days)
    return out


def run_report(n_days: int=1, receivers: List[str] = ['fortini.david@gmail.com']):
    df = get_data(n_days=n_days)
    # select last 24 hours * n_days
    no_new_records = df.empty
    receiver = 'RAS administrative'
    today_str = dt.datetime.today().strftime("%Y-%m-%d")
    if no_new_records:
        bericht = get_greeting(empty=True, receiver=receiver)
    else:
        bericht = get_greeting(empty=False, receiver=receiver)
        df = df.rename(columns={'date_upload': 'Tijd geüpload',
                                  'customer_id': 'Bedrijfsnaam',
                                  'description': 'Omschrijving'})
        df = df.drop(columns=['dc_client_id'])
        bericht += build_table(df, color='blue_light')
        
    try:
        send_plain_email(bericht, subject=f'Docudeel Uploads {today_str}',
                         )
    except boto3.client('ses').exceptions.MessageRejected:
        # stil in sanbox mode
        print('Email failed, are we out of the sanbox?')
        pass
    return bericht


if __name__ == '__main__':
    html = run_report(n_days=1)
    with open('report.html', 'w') as f:
        f.write(html)