import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:S3SecurityAlerts'
    
    buckets = s3.list_buckets()['Buckets']
    public_buckets = []
    
    for bucket in buckets:
        name = bucket['Name']
        try:
            acl = s3.get_bucket_acl(Bucket=name)
            for grant in acl['Grants']:
                grantee = grant['Grantee']
                if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                    public_buckets.append(name)
        except Exception as e:
            continue

    if public_buckets:
        message = "Public S3 Buckets Detected: " + ', '.join(public_buckets)
        sns.publish(TopicArn=topic_arn, Message=message, Subject="AWS S3 Security Alert")
