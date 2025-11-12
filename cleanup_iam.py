import boto3
import time

# ---------- CONFIG (must match creation script) ----------
REGION = "us-east-1"
USERS = ["developer_user", "analyst_user"]
ROLE_NAME = "S3DynamoReadRole"
POLICY_NAME = "CustomReadAccessPolicy"
# ---------------------------------------------------------

iam = boto3.client("iam", region_name=REGION)

print("\n🧹 Starting IAM cleanup...")

# 1️⃣ Detach and delete user policies, then delete users
for user in USERS:
    print(f"\n👤 Cleaning up user: {user}")
    try:
        # List and detach all attached policies
        attached_policies = iam.list_attached_user_policies(UserName=user)
        for policy in attached_policies["AttachedPolicies"]:
            iam.detach_user_policy(UserName=user, PolicyArn=policy["PolicyArn"])
            print(f"  🔗 Detached policy: {policy['PolicyArn']}")
        
        # Remove inline policies if any
        inline_policies = iam.list_user_policies(UserName=user)["PolicyNames"]
        for policy_name in inline_policies:
            iam.delete_user_policy(UserName=user, PolicyName=policy_name)
            print(f"  🗑️ Deleted inline policy: {policy_name}")
        
        # Delete access keys (if any)
        keys = iam.list_access_keys(UserName=user)["AccessKeyMetadata"]
        for key in keys:
            iam.delete_access_key(UserName=user, AccessKeyId=key["AccessKeyId"])
            print(f"  🔑 Deleted access key: {key['AccessKeyId']}")
        
        # Delete the user
        iam.delete_user(UserName=user)
        print(f"✅ Deleted user: {user}")
    except Exception as e:
        print(f"⚠️ Error cleaning up user {user}: {e}")

# 2️⃣ Detach policies from role and delete role
print(f"\n🧩 Cleaning up IAM role: {ROLE_NAME}")
try:
    attached_policies = iam.list_attached_role_policies(RoleName=ROLE_NAME)
    for policy in attached_policies["AttachedPolicies"]:
        iam.detach_role_policy(RoleName=ROLE_NAME, PolicyArn=policy["PolicyArn"])
        print(f"  🔗 Detached policy: {policy['PolicyArn']}")
    
    # Delete inline policies if any
    inline_policies = iam.list_role_policies(RoleName=ROLE_NAME)["PolicyNames"]
    for policy_name in inline_policies:
        iam.delete_role_policy(RoleName=ROLE_NAME, PolicyName=policy_name)
        print(f"  🗑️ Deleted inline policy: {policy_name}")
    
    # Delete role
    time.sleep(3)
    iam.delete_role(RoleName=ROLE_NAME)
    print(f"✅ Deleted IAM role: {ROLE_NAME}")
except Exception as e:
    print(f"⚠️ Error deleting role: {e}")

# 3️⃣ Delete custom policy
print(f"\n📝 Deleting custom policy: {POLICY_NAME}")
try:
    # Find custom policy by name
    policies = iam.list_policies(Scope='Local', OnlyAttached=False)["Policies"]
    policy_arn = next((p["Arn"] for p in policies if p["PolicyName"] == POLICY_NAME), None)
    
    if policy_arn:
        # Delete all versions except default
        versions = iam.list_policy_versions(PolicyArn=policy_arn)["Versions"]
        for v in versions:
            if not v["IsDefaultVersion"]:
                iam.delete_policy_version(PolicyArn=policy_arn, VersionId=v["VersionId"])
                print(f"  🗑️ Deleted non-default policy version: {v['VersionId']}")
        
        iam.delete_policy(PolicyArn=policy_arn)
        print(f"✅ Deleted custom policy: {POLICY_NAME}")
    else:
        print("ℹ️ Custom policy not found.")
except Exception as e:
    print(f"⚠️ Error deleting custom policy: {e}")

print("\n🎉 Cleanup complete! All IAM users, roles, and policies have been removed.")
