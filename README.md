 🛡️ AWS S3 Security Automation using Lambda

This project automatically scans all S3 buckets in your AWS account for public access and sends an alert via email using Amazon SNS. It demonstrates real-world cloud security automation using Lambda, IAM, and EventBridge.

---

## 📐 Architecture Overview

- **AWS Lambda (Python)**: Executes daily scans
- **Amazon SNS**: Sends security alerts via email
- **IAM Role**: Grants permissions to Lambda
- **Amazon EventBridge**: Schedules daily triggers

---

## 🔧 Prerequisites

- AWS Free Tier account
- Email address for alerts (confirmed via SNS)
- Python & AWS Console familiarity

---

## 🛠️ Setup Instructions

### 1️⃣ Create SNS Topic

1. Go to **Amazon SNS** → Topics → Create topic
2. Type: **Standard**
3. Name: `S3SecurityAlerts`
4. Click **Create topic**
5. Under Subscriptions, click **Create subscription**
   - Protocol: **Email**
   - Endpoint: *your email address*
6. Go to your inbox and **confirm the subscription**
7. Copy the **Topic ARN** for later (e.g., `arn:aws:sns:us-east-1:123456789012:S3SecurityAlerts`)

---

### 2️⃣ Create IAM Role

1. Go to **IAM > Roles > Create role**
2. Choose **Lambda** as the use case
3. Attach policies:
   - `AmazonS3ReadOnlyAccess`
   - `AmazonSNSFullAccess`
4. Name it `LambdaS3SecurityRole`
5. Click **Create Role**

---

### 3️⃣ Create Lambda Function

1. Go to **AWS Lambda > Create Function**
2. Name: `DetectPublicS3`
3. Runtime: `Python 3.12`
4. Permissions: Use existing role → `LambdaS3SecurityRole`
5. Click **Create Function**

---

### 4️⃣ Add This Python Code

Replace the default function code with:

```python
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-east-1:123456789012:S3SecurityAlerts'  # replace with your real ARN

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
            print(f"Error checking bucket {name}: {e}")
            continue

    print("Buckets found:", [b['Name'] for b in buckets])
    print("Public buckets:", public_buckets)

    if public_buckets:
        message = "Public S3 Buckets Detected: " + ', '.join(public_buckets)
        sns.publish(TopicArn=topic_arn, Message=message, Subject="AWS S3 Security Alert")
```

✅ Replace the `topic_arn` value with your actual SNS ARN from Step 1.

Click **Deploy**

---

### 5️⃣ Test It

1. Click **Test > Configure test event**
2. Use `{}` as the event body
3. Click **Test**
4. If a public bucket is detected, you’ll get an email alert

---

### 6️⃣ Schedule Daily Scans

1. In the Lambda console, click **Add Trigger**
2. Choose **EventBridge (CloudWatch Events)**
3. Create a new rule
   - Name: `DailyS3Scan`
   - Schedule expression: `rate(1 day)`
4. Click **Add**

---

### 7️⃣ Test with a Public Bucket

1. Go to **S3 → Create bucket**
2. Name: `test-public-bucket-XYZ`
3. Uncheck **Block all public access**
4. Create the bucket
5. Go to **Permissions > Edit ACL**
6. Grant **Read** access to **Everyone (public)**
7. Save and run the Lambda again

✅ You should see:
```python
Public buckets: ['test-public-bucket-XYZ']
```
📬 And receive an alert email.

---

## 📁 Repo Contents

- `lambda_function.py` — Scanning + alert logic
- `iam-policy.json` — IAM permissions (optional)
- `README.md` — Full walkthrough

---

## 👤 Author

Shawn Busby  
Security+ | AWS Solutions Architect Associate  
[GitHub](https://github.com/shawnbusby)
