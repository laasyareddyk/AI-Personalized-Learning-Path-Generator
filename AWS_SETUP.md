# AWS Setup

This project includes optional AWS integration modules. It runs without AWS credentials.

## Bedrock

Set `AWS_BEDROCK_ENABLED=true`, `AWS_REGION`, and `BEDROCK_MODEL_ID`. Configure AWS credentials through the standard AWS credential provider chain. Enable access to the selected model in your AWS account. This can incur usage charges.

The application explicitly separates demo output from Bedrock output. Bedrock generation is not invoked automatically by dashboard loads.

## S3

Set `S3_BUCKET` and configure write permissions if using `backend/aws/s3_service.py`. Create the bucket separately; this application does not deploy it.

## Lambda and API Gateway

`lambda_handlers.py` provides reusable handler entry points. Deploying Lambda or API Gateway is optional and is not performed by this project.
