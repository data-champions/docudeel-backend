import os

try:
    from src.config import AIRTABLE_BASE_ID, AIRTABLE_TOKEN
except:
    print('ImportError')
    import sys
    from pprint import pprint as pp
    pp(sys.path)

environment = {
    "AWS_ACCESS_KEY_ID": os.environ['AWS_ACCESS_KEY_ID'],
    "AWS_SECRET_ACCESS_KEY": os.environ['AWS_SECRET_ACCESS_KEY'],
    "AIRTABLE_BASE_ID": AIRTABLE_BASE_ID,
    "AIRTABLE_TOKEN": AIRTABLE_TOKEN,
}

print(f'{environment=}')