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
from aws_solutions_constructs.aws_lambda_dynamodb import LambdaToDynamoDB

class ServerlessAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        products_backend = LambdaToDynamoDB(self, 'ProductsBackend',
                                            lambda_function_props=lambda_.FunctionProps(
                                                code=lambda_.Code.from_asset('lambda_src'),
                                                handler='product_list_function.lambda_handler',
                                                runtime=lambda_.Runtime.PYTHON_3_11,
                                            ),
                                            table_environment_variable_name='TABLE_NAME',
                                            table_permissions='Read')
        
        products_table = products_backend.dynamo_table

        product_list_function = products_backend.lambda_function

        # Delete the table on stack deletion
        products_table.apply_removal_policy(RemovalPolicy.DESTROY)

        # L2 Level Construct --------------------------------------------------------------------

        # products_table = dynamodb.Table(self, 'ProductsTable',
        #                                partition_key=dynamodb.Attribute(
        #                                    name='id',
        #                                    type=dynamodb.AttributeType.STRING
        #                                ),
        #                                billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        #                                removal_policy=RemovalPolicy.DESTROY)
        
        # product_list_function = lambda_.Function(self, 'ProductListFunction',
        #                                          code=lambda_.Code.from_asset('lambda_src'),
        #                                          handler='product_list_function.lambda_handler',
        #                                          runtime=lambda_.Runtime.PYTHON_3_11,
        #                                          environment={
        #                                              'TABLE_NAME': products_table.table_name
        #                                          })
        
        # Granting permissions to the Lambda function to read data from the DynamoDB table
        # products_table.grant_read_data(product_list_function.role)

        # L2 Level Construct --------------------------------------------------------------------
        
        # Adding a Lambda URL the lambda function to execute it from the Internet
        product_list_url = product_list_function.add_function_url(auth_type=lambda_.FunctionUrlAuthType.NONE)

        # Adding a stack output for the function URL to access it easily
        CfnOutput(self, 'ProductListUrl',
                  value=product_list_url.url)

        # Configuring an alarm for the Lambda function's errors metric
        # metric 정의
        errors_metric = product_list_function.metric_errors(
            label='ProductionListFunction Errors',
            period=Duration.minutes(5),
            statistic=cloudwatch.Stats.SUM
        )

        # metric에 대한 alarm
        errors_metric.create_alarm(self, 'ProductListErrorsAlarm',
                                   evaluation_periods=1,
                                   threshold=1,
                                   comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                                   treat_missing_data=cloudwatch.TreatMissingData.IGNORE)