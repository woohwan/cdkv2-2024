from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct

class MySampleAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1.vpc 생성
        my_vpc = ec2.CfnVPC(self, 'MyVPC',
                        cidr_block="10.0.0.0/16",
                        enable_dns_hostnames=True,
                        enable_dns_support=True)
        
        # 2. Internet gateway 생성
        internet_gateway = ec2.CfnInternetGateway(self, 'InternetGateway')

        # VPC와 IG연결
        ec2.CfnVPCGatewayAttachment(self, 'IgwAttatchment',
                                    vpc_id=my_vpc.attr_vpc_id,
                                    internet_gateway_id=internet_gateway.attr_internet_gateway_id)
        
        # 3. subnet 생성
        my_subnet = [
            { 'cidr_block': '10.0.0.0/24', 'public': True},
            { 'cidr_block': '10.0.1.0/24', 'public': True},
            { 'cidr_block': '10.0.2.0/24', 'public': False},
            { 'cidr_block': '10.0.3.0/24', 'public': False},
        ]

        for i, subnet in enumerate(my_subnet):

            subnet_resource = ec2.CfnSubnet(self, f'Subnet{i}',
                                           vpc_id=my_vpc.attr_vpc_id,
                                           cidr_block=subnet['cidr_block'],
                                           map_public_ip_on_launch=subnet['public'],
                                           availability_zone=Stack.availability_zones.fget(self)[i%2] )  # 2개만 이용
            
            # Route table 생성
            route_table = ec2.CfnRouteTable(self, f'Subnet{i}RouteTable',
                                            vpc_id=my_vpc.attr_vpc_id)
            
            # Routable Asscociation 생성: subnet과 table 연결
            ec2.CfnSubnetRouteTableAssociation(self, f'Subnet{i}RouteTableAscn',
                                               route_table_id=route_table.attr_route_table_id,
                                                subnet_id=subnet_resource.attr_subnet_id )
            
            # public subnet internet 연결: 연결e된 route table에 route 추가
            if subnet['public']:

                ec2.CfnRoute(self, f'Subnet{i}InternetRoute',
                             route_table_id=route_table.attr_route_table_id,
                             destination_cidr_block='0.0.0.0/0',
                             gateway_id=internet_gateway.attr_internet_gateway_id)