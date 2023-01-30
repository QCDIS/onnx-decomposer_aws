import boto3
import json

import sfn_constants
import utils

sfn_client = boto3.client('stepfunctions')
lambda_client = boto3.client('lambda')
iam_client = boto3.client('iam')

with open(sfn_constants.EVENT0) as event0_file:
    event0_data = json.load(event0_file)

function = lambda_client.get_function(
    FunctionName=sfn_constants.FUNCTION_NAME
)
role = iam_client.get_role(RoleName='StepFunctionLambdaBasicExecution')
function_arn = function['Configuration']['FunctionArn']
asl_definition = {
  "Comment": sfn_constants.STATE_MACHINE_NAME,
  "StartAt": "Init",
  "States": {
    "Init": {
      "Type": "Pass",
      "Result": event0_data,
      "Next": sfn_constants.FUNCTION_NAME
    },
    sfn_constants.FUNCTION_NAME: {
      "Type": "Task",
      "Resource": function_arn,
      "Next": "IsExecutionCompleted"
    },
    "IsExecutionCompleted": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.body.keep_going",
          "BooleanEquals": True,
          "Next": sfn_constants.FUNCTION_NAME
        }
      ],
      "Default": "Done",
      "OutputPath": "$.body"
    },
    "Done": {
      "Type": "Pass",
      "End": True,
      "ResultPath": None,
      "InputPath": "$.result"
    }
  }
}
response = sfn_client.create_state_machine(
    name=sfn_constants.STATE_MACHINE_NAME,
    definition=json.dumps(asl_definition),
    roleArn=role['Role']['Arn']
)

utils.save_to_file(response, sfn_constants.DEPLOYMENT_OUTPUT)

print(response)