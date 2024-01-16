#!/usr/bin/env python3
import os

import aws_cdk as cdk

from my_sample_app.my_sample_app_stackL2 import MySampleAppStackL2
from my_sample_app.network_stack import NetworkStack

app = cdk.App()

root_stack = cdk.Stack(app, 'RootStack')
newtwork_stack = NetworkStack(root_stack, "NetworkStack")
MySampleAppStackL2(root_stack, "MySampleAppStackL2", my_vpc=newtwork_stack.vpc)


app.synth()
