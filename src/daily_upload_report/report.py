#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Send a report based on s3 raw files.
"""
import boto3
import datetime as dt
import os
from typing import List

import pandas as pd

# for local dev go to src/daily_upload_report
from fancy_html import build_table, get_greeting
from report_email import send_plain_email, send_email_make
from s3_files import get_data


def run_report(receiver: str, backup_receiver: str, n_days: int=1,
               receiver_name: str = 'RAS administrative') -> str:
    df = get_data(n_days_ago=n_days)
    # select last 24 hours * n_days
    no_new_records = df.empty

    if no_new_records:
        bericht = get_greeting(empty=True, receiver=receiver_name)
    else:
        bericht = get_greeting(empty=False, receiver=receiver_name)
        bericht += build_table(df, color='blue_light')
    send_email_make(message=bericht,
                    receiver=receiver,
                    backup_receiver='infodatachampions@gmail.com')
    return bericht


if __name__ == '__main__':
    html = run_report(
        receiver='fortini.david@gmail.com',
        backup_receiver='infodatachampions@gmail.com',
        n_days=22)