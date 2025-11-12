import boto3
import json
import time

# ---------- CONFIG ----------
REGION = "us-east-1"
USERS = ["developer_user", "analyst_user"]
ROLE_NAME = "S3DynamoReadRole"
POLICY_NAME = "CustomReadAccessPolicy"
# ----------------------------

iam = boto3.client("iam", region_name=REGION)

# 1️⃣ Create IAM Users
print("\n👤 Creating IAM Users...")
for user in USERS:
    try:
        iam.create_user(UserName=user)
        print(f"✅ Created user: {user}")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"ℹ️ User already exists: {user}")

# 2️⃣ Create IAM Role (for assumed access)
print(f"\n🧩 Creating IAM Role: {ROLE_NAME}...")
assume_role_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": "*"},  # you can restrict this to specific users/accounts
            "Action": "sts:AssumeRole"
        }
    ]
}

try:
    role = iam.create_role(
        RoleName=ROLE_NAME,
        AssumeRolePolicyDocument=json.dumps(assume_role_policy),
        Description="Role allowing S3 and DynamoDB read access"
    )
    role_arn = role["Role"]["Arn"]
    print(f"✅ Created role: {ROLE_NAME} ({role_arn})")
except iam.exceptions.EntityAlreadyExistsException:
    print(f"ℹ️ Role already exists: {ROLE_NAME}")
    role_arn = iam.get_role(RoleName=ROLE_NAME)["Role"]["Arn"]

# Wait briefly for role to propagate
time.sleep(10)

# 3️⃣ Create a Custom Policy (S3 + DynamoDB read)
print(f"\n📝 Creating custom policy: {POLICY_NAME}...")
custom_policy_doc = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:Query"
            ],
            "Resource": "*"
        }
    ]
}

try:
    policy = iam.create_policy(
        PolicyName=POLICY_NAME,
        PolicyDocument=json.dumps(custom_policy_doc),
        Description="Allows read access to S3 and DynamoDB"
    )
    policy_arn = policy["Policy"]["Arn"]
    print(f"✅ Created custom policy: {policy_arn}")
except iam.exceptions.EntityAlreadyExistsException:
    print("ℹ️ Policy already exists, fetching ARN...")
    policy_arn = iam.list_policies(Scope='Local')['Policies'][0]['Arn']

# 4️⃣ Attach Policy to Role
print(f"\n🔗 Attaching policy to role {ROLE_NAME}...")
iam.attach_role_policy(RoleName=ROLE_NAME, PolicyArn=policy_arn)
print("✅ Policy attached to role.")

# 5️⃣ Attach AWS Managed Policy to Role (optional)
aws_managed_policy = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
iam.attach_role_policy(RoleName=ROLE_NAME, PolicyArn=aws_managed_policy)
print("✅ Attached AWS managed S3ReadOnlyAccess policy to role.")

# 6️⃣ Attach Policy to Users
print(f"\n👥 Assigning policies to users...")
for user in USERS:
    try:
        iam.attach_user_policy(UserName=user, PolicyArn=policy_arn)
        print(f"✅ Attached custom policy to user: {user}")
        iam.attach_user_policy(UserName=user, PolicyArn=aws_managed_policy)
        print(f"✅ Attached AWS managed policy to user: {user}")
    except Exception as e:
        print(f"⚠️ Error attaching policy to {user}: {e}")

print("\n🎉 Setup complete!")
print(f"Users: {USERS}")
print(f"Role: {ROLE_NAME}")
print(f"Policy: {POLICY_NAME}")
