#!/usr/bin/env python3


import os
import sys

from pprint import pprint as pp
pp(sys.path)
from aws_cdk import App, Stack

from infra.report_stack import ReportStack

app = core.App()

ReportStack(app, "report-stack")
app.synth()