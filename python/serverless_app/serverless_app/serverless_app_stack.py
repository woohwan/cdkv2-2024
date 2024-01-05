from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    CfnOutput,
    Duration,
    aws_cloudwatch as cloudwatch
)
from constructs import Construct

class ServerlessAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        products_table = dynamodb.Table(self, 'ProductsTable',
                                       partition_key=dynamodb.Attribute(
                                           name='id',
                                           type=dynamodb.AttributeType.STRING
                                       ),
                                       billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                                       removal_policy=RemovalPolicy.DESTROY)
        
        product_list_function = lambda_.Function(self, 'ProductListFunction',
                                                 code=lambda_.Code.from_asset('lambda_src'),
                                                 handler='product_list_function.lambda_handler',
                                                 runtime=lambda_.Runtime.PYTHON_3_11,
                                                 environment={
                                                     'TABLE_NAME': products_table.table_name
                                                 })
        
        # Granting permissions to the Lambda function to read data from the DynamoDB table
        products_table.grant_read_data(product_list_function.role)
        
        # Adding a Lambda URL the lambda function to execute it from the Internet
        product_list_url = product_list_function.add_function_url(auth_type=lambda_.FunctionUrlAuthType.NONE)

        # Adding a stack output for the function URL to access it easily
        CfnOutput(self, 'ProductListUrl',
                  value=product_list_url.url)