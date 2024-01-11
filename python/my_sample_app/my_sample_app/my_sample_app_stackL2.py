from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2
)
from constructs import Construct

class MySampleAppStackL2(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1.vpc 생성
        my_vpc = ec2.Vpc(self, 'MyVPC',
                         nat_gateways=0)
        
        web_server = ec2.Instance(self, 'WebServer',
                                  machine_image=ec2.MachineImage.latest_amazon_linux2(),
                                  instance_type=ec2.InstanceType.of(instance_class=ec2.InstanceClass.T2,
                                                                    instance_size=ec2.InstanceSize.MICRO),
                                  vpc=my_vpc,
                                  vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                  user_data_causes_replacement=True,
                                  ssm_session_permissions=True
                                  )
        
        # Attaching an Elastic IP to keep the DNS name on updates
        ec2.CfnEIP(self, 'ElasticIP',
                   instance_id=web_server.instance_id)
        
        # Installing package at instance launch
        web_server.add_user_data('yum update -y',
                                 'amazon-linux-extras install nginx1',
                                 'service nginx start')
        
        CfnOutput(self, 'WebServerDnsName',
                  value=web_server.instance_public_dns_name)
        
        # Allowing connectins to the web server
        web_server.connections.allow_from_any_ipv4(ec2.Port.tcp(80), 'Allow HTTP Access from the Internet')
