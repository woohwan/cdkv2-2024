#!/usr/bin/env python3
import os

import aws_cdk as cdk

# from my_sample_app.my_sample_app_stack import MySampleAppStack
from my_sample_app.my_sample_app_stackL2 import MySampleAppStackL2

app = cdk.App()
# MySampleAppStack(app, "MySampleAppStack")
MySampleAppStackL2(app, "MySampleAppStackL2")

app.synth()
