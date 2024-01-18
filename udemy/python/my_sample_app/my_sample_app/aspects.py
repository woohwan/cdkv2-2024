import jsii
from aws_cdk import (
    IAspect,
    Annotations,
    aws_ec2 as ec2,
    Stack
)

# for ec2 instance validation check
@jsii.implements(IAspect)
class EC2InstanceTypeChecker:
    
    def visit(self, node):
        if isinstance(node, ec2.CfnInstance ):
            if node.instance_type not in ['t2.micro', 't3.micro']:
                # Annotations.of(node).add_error(f'{node.instance_type} instance type is invalid')
                Annotations.of(node).add_warning(f'{node.instance_type} instance type is invalid. It will be set to t2.micro.')
                node.instance_type = 't2.micro'

@jsii.implements(IAspect)
class SSHAnywhereChecker:
    # synth 단계 전에는 정해져 있기 않기 때문에, resolve method를 호출함.
    def visit(self, node):
        if isinstance(node, ec2.CfnSecurityGroup):
            rules = Stack.of(node).resolve(node.security_group_ingress)
            # print(rules)
            for rule in rules:
                if rule['ipProtocol'] == 'tcp' and rule['fromPort'] <=22 and rule['toPort'] >= 22:
                    if rule['cidrIp'] == '0.0.0.0/0':
                        Annotations.of(node).add_error('SSH from anywhere is not allowed')