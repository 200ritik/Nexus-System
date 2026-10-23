
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "nexus-medical-storage"

OBJECT_KEY = (
    "users/test-user-123/documents/"
    "0bebe8b7-7272-4ad0-9dd7-601b3f3008e0/"
    "blood_report.pdf"
)

s3 = boto3.client("s3", region_name="us-east-1")

try:
    response = s3.head_object(
        Bucket=BUCKET_NAME,
        Key=OBJECT_KEY,
    )

    print("SUCCESS: Python can access the S3 object.")
    print("File size:", response["ContentLength"], "bytes")

except ClientError as error:
    details = error.response.get("Error", {})

    print("S3 access failed.")
    print("Error code:", details.get("Code"))
    print("Message:", details.get("Message"))

    print(
        "\nCheck the IAM identity, s3:GetObject permission, "
        "bucket policy, and any applicable KMS permissions."
    )
        