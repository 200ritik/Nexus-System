import boto3

from configuration.config import (
    access_key,
    secret_access_key,
    bucket_name,
    region
)


def get_s3_client():

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
        region_name=region
    )

    return s3_client

    