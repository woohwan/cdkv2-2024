from aws_cdk import (
    NestedStack,
    CfnOutput,
    aws_ec2 as ec2,
    # aws_rds as rds,
    # RemovalPolicy,
    aws_s3_assets as s3_assets
)
from constructs import Construct

class MySampleAppStackL2(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, my_vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
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
                                 'rm -rf /usr/share/nginx/html/*'
                                 )
        
        CfnOutput(self, 'WebServerDnsName',
                  value=web_server.instance_public_dns_name)
        
        # Allowing connectins to the web server
        web_server.connections.allow_from_any_ipv4(ec2.Port.tcp(80), 'Allow HTTP Access from the Internet')

        # for ssh access를 통해서 db 연결 테스트를 위해 사용
        web_server.connections.allow_from_any_ipv4(ec2.Port.tcp(22), 'Allow SSH Access from the Internet')

        # Deploying a web page to the web server
        web_page_asset = s3_assets.Asset(self, 'WebPageAsset',
                                         path='web_pages/index.html')
        
        web_server.user_data.add_s3_download_command(bucket=web_page_asset.bucket,
                                                     bucket_key=web_page_asset.s3_object_key,
                                                     local_file='/usr/share/nginx/html/index.html')

        web_page_asset.grant_read(web_server.role)

        web_server.add_user_data('service nginx start')

        
        # # DB Instance configuration
        # db_instance = rds.DatabaseInstance(self, 'DbInstance',
        #                                     engine=rds.DatabaseInstanceEngine.MARIADB,
        #                                     vpc=my_vpc,
        #                                     vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
        #                                     instance_type=ec2.InstanceType.of(instance_class=ec2.InstanceClass.T2,
        #                                                                         instance_size=ec2.InstanceSize.MICRO),
        #                                     removal_policy=RemovalPolicy.DESTROY)
        
        # # Allowing connections to the DB instance
        # # db 관점에서: inbound rule 생성
        # db_instance.connections.allow_default_port_from(web_server, 'Allow MySQL access from the web server')

        # # web server 관점에서. same as the above
        # # web_server.connections.allow_to_default_port(db_instance, "db instance로 연결 허용")

        # # web server에서 db 연결 테스트
        # # Installing MySQL client on the web server
        # web_server.add_user_data('yum install -y mysql')


        # # DB endpoint 
        # CfnOutput(self, 'DbEndpoint',
        #           value=db_instance.db_instance_endpoint_address)