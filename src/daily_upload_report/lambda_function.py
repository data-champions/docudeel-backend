

from report import run_report


def lambda_handler(event, context):
    run_report(n_days=1, receivers=[''])
    print('lambda finished')
    return None
