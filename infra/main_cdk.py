#!/usr/bin/env python3

from aws_cdk import App, Stack

from report_stack import ReportStack

app = App()

ReportStack(app, "report-stack")
app.synth()
