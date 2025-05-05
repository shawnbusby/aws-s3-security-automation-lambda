# AWS S3 Security Automation using Lambda

This project detects publicly accessible S3 buckets and sends security alerts via SNS email notifications. It's designed to demonstrate security automation skills using AWS Lambda, EventBridge, and IAM.

## Architecture

- AWS Lambda (Python)
- AWS SNS (for email notifications)
- IAM Role (Lambda execution + SNS publish)
- EventBridge (Scheduled daily trigger)

## Setup

1. Create SNS Topic and confirm email subscription.
2. Create IAM role: attach `AmazonS3ReadOnlyAccess` and `AmazonSNSFullAccess`.
3. Deploy Lambda using `lambda_function.py` and assign the role.
4. Create an EventBridge trigger with `rate(1 day)`.

## Lambda Function

See `lambda_function.py` for full source code.

## IAM Policy

See `iam-policy.json` for an example policy.

## Author

Shawn Busby | Security+ | AWS Solutions Architect Associate
