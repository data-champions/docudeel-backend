import os


AIRTABLE_TOKEN = os.environ["AIRTABLE_TOKEN"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]

environment = {
    "AWS_ACCESS_KEY_ID": os.environ['AWS_ACCESS_KEY_ID'],
    "AWS_SECRET_ACCESS_KEY": os.environ['AWS_SECRET_ACCESS_KEY'],
    "AIRTABLE_BASE_ID": AIRTABLE_BASE_ID,
    "AIRTABLE_TOKEN": AIRTABLE_TOKEN,
}

print(f'{environment=}')