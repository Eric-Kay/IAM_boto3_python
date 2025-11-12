

---

# 🛠️ AWS IAM Setup Script — S3 & DynamoDB Read Access

This Python script automates the creation and configuration of **AWS IAM users**, **roles**, and **policies** to grant **read-only access** to **Amazon S3** and **Amazon DynamoDB** resources.

It uses the **boto3** library (AWS SDK for Python) to interact with IAM and set up the following:

* IAM Users
* IAM Role (for assumed access)
* Custom IAM Policy (S3 + DynamoDB read)
* Attachments of Policies to Users and Role
* Optional attachment of AWS Managed Policy for S3 read access

---

## 📋 Features

✅ Creates multiple IAM users automatically
✅ Creates an IAM role with an assume-role trust policy
✅ Creates a custom policy that allows read-only access to S3 and DynamoDB
✅ Attaches the policy to both the role and users
✅ Optionally attaches AWS managed `AmazonS3ReadOnlyAccess` policy
✅ Handles existing users, roles, and policies gracefully

---

## 🧩 Prerequisites

Before running this script, ensure you have:

* **Python 3.7+**
* **boto3** library installed

  ```bash
  pip install boto3
  ```
* **AWS CLI configured** with credentials that have permission to create IAM users, roles, and policies:

  ```bash
  aws configure
  ```
* IAM permissions required for the executing identity (AdministratorAccess or equivalent)

---

## ⚙️ Configuration

Update the configuration section at the top of the script:

```python
# ---------- CONFIG ----------
REGION = "us-east-1"  # AWS region
USERS = ["developer_user", "analyst_user"]  # List of IAM users to create
ROLE_NAME = "S3DynamoReadRole"  # Name of IAM role to create
POLICY_NAME = "CustomReadAccessPolicy"  # Name of custom policy
# ----------------------------
```

You can modify the user list, role name, or policy name to suit your environment.

---

## 🚀 How to Run

1. **Clone this repository**

   ```bash
   git clone https://github.com/Eric-Kay/IAM_boto3_python.git
   cd IAM
   ```

2. **Run the script**

   ```bash
   python 
   ```

3. The script will:

   * Create IAM users if they don’t exist
   * Create a role with a trust relationship
   * Create a custom policy for read access
   * Attach the policies to users and role

---

## 📄 Example Output

```
👤 Creating IAM Users...
✅ Created user: developer_user
✅ Created user: analyst_user

🧩 Creating IAM Role: S3DynamoReadRole...
✅ Created role: S3DynamoReadRole (arn:aws:iam::123456789012:role/S3DynamoReadRole)

📝 Creating custom policy: CustomReadAccessPolicy...
✅ Created custom policy: arn:aws:iam::123456789012:policy/CustomReadAccessPolicy

🔗 Attaching policy to role S3DynamoReadRole...
✅ Policy attached to role.
✅ Attached AWS managed S3ReadOnlyAccess policy to role.

👥 Assigning policies to users...
✅ Attached custom policy to user: developer_user
✅ Attached AWS managed policy to user: developer_user
✅ Attached custom policy to user: analyst_user
✅ Attached AWS managed policy to user: analyst_user

🎉 Setup complete!
```

---

## 🧠 Notes

* The trust relationship in the assume-role policy is currently **open to all AWS principals (`"AWS": "*"`)**.
  You should **restrict it** to specific AWS accounts or IAM entities for security:

  ```json
  "Principal": { "AWS": "arn:aws:iam::123456789012:user/developer_user" }
  ```

* Use IAM **least privilege** principles — customize policies as needed.

* To delete the created resources, you can manually remove users, roles, and policies via the **AWS Management Console** or using the script cleanup_iam.py.

---

## 📚 AWS Docs Reference

* [boto3 IAM documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html)
* [AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/)
* [AWS Policy Reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)

---

## 🧑‍💻 Author

**ERIC AVWORHO**
📧 [avworho.eric@gmail.com]


---

