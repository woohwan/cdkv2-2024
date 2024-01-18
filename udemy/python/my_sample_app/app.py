#!/usr/bin/env python3
import os

import aws_cdk as cdk

from my_sample_app.my_sample_app_stackL2 import MySampleAppStackL2
from my_sample_app.network_stack import NetworkStack
from my_sample_app.aspects import ( EC2InstanceTypeChecker, SSHAnywhereChecker)

app = cdk.App()

root_stack = cdk.Stack(app, 'RootStack')
newtwork_stack = NetworkStack(root_stack, "NetworkStack")
application_stack = MySampleAppStackL2(root_stack, "MySampleAppStackL2", 
                   my_vpc=newtwork_stack.vpc)

# Aspect attachement
cdk.Aspects.of(root_stack).add(EC2InstanceTypeChecker())
cdk.Aspects.of(root_stack).add(SSHAnywhereChecker())

# Stack-level tagging
cdk.Tags.of(newtwork_stack).add('category', 'network')
cdk.Tags.of(application_stack).add('category', 'application',
                                   priority=200)

app.synth()
