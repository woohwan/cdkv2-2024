import aws_cdk as core
import aws_cdk.assertions as assertions

# from my_sample_app.my_sample_app_stack import MySampleAppStack
from my_sample_app.my_sample_app_stackL2 import MySampleAppStackL2
from my_sample_app.network_stack import NetworkStack


def test_network_stack_resource_counts():
    app = core.App()
    root_stack = core.Stack(app, 'RootStack')
    newtwork_stack = NetworkStack(root_stack, "NetworkStack")
    application_stack = MySampleAppStackL2(root_stack, "MySampleAppStackL2", 
                    my_vpc=newtwork_stack.vpc)
    
    template = assertions.Template.from_stack(newtwork_stack)
    template.resource_count_is('AWS::EC2::VPC', 1)
    template.resource_count_is('AWS::EC2::NatGateway', 0)

def test_application_stack_web_server():
    app = core.App()
    root_stack = core.Stack(app, 'RootStack')
    newtwork_stack = NetworkStack(root_stack, "NetworkStack")
    application_stack = MySampleAppStackL2(root_stack, "MySampleAppStackL2", 
                    my_vpc=newtwork_stack.vpc)
    
    template = assertions.Template.from_stack(application_stack)
    # for only resource propertiest
    template.has_resource_properties('AWS::EC2::Instance', {
        'InstanceType': assertions.Match.string_like_regexp('(t2|t3).micro'),
        'ImageId': assertions.Match.any_value(),
        'KeyName': assertions.Match.absent()
    })

    # template.has_resource('AWS::EC2::INSTANCE', {
    #     'Properties': {},
    #     'DependsOn': '',
    #     'DeletionPolicy': ''
    # })

# for complex data type: ex: array
def test_web_server_security_group():
    app = core.App()
    root_stack = core.Stack(app, 'RootStack')
    newtwork_stack = NetworkStack(root_stack, "NetworkStack")
    application_stack = MySampleAppStackL2(root_stack, "MySampleAppStackL2", 
                    my_vpc=newtwork_stack.vpc)
    
    template = assertions.Template.from_stack(application_stack)
    # for only resource propertiest
    template.has_resource_properties('AWS::EC2::SecurityGroup', {
        # array_with와 array_eqauls의 차이. equals는 only 하나만 허용
        # 여기 같은 경우 SecurityGroupIngress 하나만 허용하고 싶을 때
        # !!     Too many elements in array (expecting 1, got 2)
        # object_like와 object_equals과 동일한 의미
        # equals일 경우, resource정의와 property와 완전히 동일해야 함.

        'SecurityGroupIngress': assertions.Match.array_with([
            assertions.Match.object_equals({
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'CidrIp': '0.0.0.0/0',
                'Description': assertions.Match.any_value()
            })
        ])
    })
