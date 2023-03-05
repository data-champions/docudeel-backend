

# v2
from aws_cdk import (
    App,
    Stack,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_events as events,
    aws_events_targets as targets
)
import json
import urllib.request
from typing import List

from src.config import AIRTABLE_TOKEN, AIRTABLE_BASE_ID


def _get_layer_arn(lib: str = 'pandas') -> str:
    url = f'https://api.klayers.cloud/api/v2/p3.9/layers/eu-central-1/{lib}'
    contents = urllib.request.urlopen(url).read()
    return json.loads(contents)[0]['arn']


def create_klayer(stack: core.Stack,
                  lib: str) -> lambda_.LayerVersion:
    layer_arn = _get_layer_arn(lib=lib)
    layer = lambda_.LayerVersion.from_layer_version_arn(
        stack,
        id=f'layer-{lib}',
        layer_version_arn=layer_arn)
    return layer


def create_daily_rule(stack: core.Stack,
                      rule_targets: List[lambda_.Function]) -> None:
    rule_targets = [targets.LambdaFunction(x) for x in rule_targets]
    # time is right before the current notification email!
    events.Rule(
        stack,
        id="every_morning",
        rule_name="every_morning",
        description="daily trigger for daily reports",
        schedule=events.Schedule.cron(
            hour='9',
            minute='30',
            week_day='*',
            month='*',
            year='*'),
        targets=rule_targets
    )


class ReportStack(core.Stack):
    # scope is type construct
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        layer_pandas = create_klayer(stack=self, lib='pandas')
        layer_req = create_klayer(stack=self, lib='requests')

        env = dict(AIRTABLE_TOKEN=AIRTABLE_TOKEN,
                   AIRTABLE_BASE_ID=AIRTABLE_BASE_ID
        )
        fn_name = 'daily_upload_report'
        scheduler_fn = lambda_.Function(self, id=fn_name,
        function_name=fn_name,
        code=lambda_.Code.from_asset(f'lambdas/{fn_name}'),
        runtime=lambda_.Runtime.PYTHON_3_9,
        handler=f"lambda_function.lambda_handler",
        environment=env,
        memory_size=576,
        layers=[layer_pandas, layer_req],
        retry_attempts=0
        )
        schedule = create_daily_rule(self, rule_targets=[scheduler_fn])
