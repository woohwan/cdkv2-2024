#!/usr/bin/env python3
import os

import aws_cdk as cdk
from my_first_cdk_app.my_first_cdk_app_stack import MyFirstCdkAppStack

# https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html#bootstrapping-synthesizers
app = cdk.App()
MyFirstCdkAppStack(app, "MyFirstCdkAppStack",
        synthesizer=cdk.DefaultStackSynthesizer(
            generate_bootstrap_version_rule=False,)
            )

app.synth()
