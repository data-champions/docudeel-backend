
try:
    from report import run_report
except ImportError:
    # local dev
    from lambdas.daily_upload_report.report import run_report


def lambda_handler(event, context):
    run_report(n_days=1.3)
    print('lambda finished')
    return None
