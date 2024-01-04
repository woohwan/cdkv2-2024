from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct

class MySampleAppStackL2(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1.vpc 생성
        my_vpc = ec2.Vpc(self, 'MyVPC',
                         nat_gateways=0)