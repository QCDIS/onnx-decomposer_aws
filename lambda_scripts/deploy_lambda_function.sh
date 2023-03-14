#!/bin/bash

source project.config
source constants.sh

echo "FUNCTION:" ${FUNCTION_NAME}
echo "EXECUTION_TIMEOUT:" ${EXECUTION_TIMEOUT}"s"
echo "FUNCTION_MEMORY:" ${FUNCTION_MEMORY}"MB"

aws lambda delete-function --function-name ${FUNCTION_NAME}

aws s3 cp ${ZIP_PACKAGE_PATH} s3://${S3_BUCKET}

aws lambda create-function --function-name ${FUNCTION_NAME} \
--code S3Bucket=${S3_BUCKET},S3Key=${ZIP_PACKAGE} --handler ${LAMBDA_HANDLER}.lambda_handler --runtime python3.8 \
--role arn:aws:iam::426543810977:role/lambda-ex --timeout ${EXECUTION_TIMEOUT} --memory-size ${FUNCTION_MEMORY}
