#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 13:59:57 2023

@author: david
"""

import datetime
import json
from datetime import datetime, timezone

from typing import Dict, Tuple, Union, List, Optional

import boto3, botocore
import pandas as pd
from collections import Counter
bucket = 'docudeel-temp-storage'

def is_recent_file(item: dict, n_days_ago: Optional[int] = None) -> bool:
    if n_days_ago is None:
        return True
    n_days_last_modified = (item['LastModified'] - datetime.now(timezone.utc)).days
    is_recent = abs(n_days_last_modified) < n_days_ago
    return is_recent



def get_s3_files(bucket_name: str,
                 s3_client: botocore.client = boto3.client("s3"),
                 n_days_ago: Optional[int] = None
                 ) -> List[str]:
    """
    get all the names of the files inside an s3 directory
    """
    kwargs = dict(Bucket=bucket_name,
                  # Prefix=s3_directory,
                  MaxKeys=1000)
    all_file_names = []
    # a response with a continuation token implies there are more files
    # to be retrieved
    while True:
        response = s3_client.list_objects_v2(**kwargs)
        all_items = response['Contents']
        continuation_token = response.get('NextContinuationToken', None)
        kwargs['ContinuationToken'] = continuation_token
        if len(all_items) > 0:
            # apply transformations here!
            for item in all_items:
                is_recent = is_recent_file(item=item, n_days_ago=n_days_ago)
                if is_recent:
                    all_file_names.append(item['Key'])
        if continuation_token is None:
            break

    print(f'found {len(all_file_names)} files')
    return all_file_names


def get_data(n_days_ago: int) -> pd.DataFrame:


    files = get_s3_files(bucket_name=bucket, n_days_ago=n_days_ago)
    if files != []:
        data = dict(Counter([x.split('_')[0] for x in files ]))
    
        df = pd.DataFrame.from_dict(data, orient='index').reset_index()
        df = df.rename(columns={'index':'debiteurnummer', 0 : 'aantal bestanden'})
    else:
        df = pd.DataFrame()
    return df


if __name__ == "__main__":
    data = get_data(1)
    data = get_data(8)
