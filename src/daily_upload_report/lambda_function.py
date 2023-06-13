

from report import run_report


def lambda_handler(event, context):
    run_report(receiver='info@rasadministrative.com',
               receiver_name='RAS administrative',
               backup_receiver='infodatachampions@gmail.com',
               n_days=1)
    
    print('lambda finished')
    return None
