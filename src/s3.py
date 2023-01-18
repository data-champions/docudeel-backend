import boto3
import logging
from botocore.exceptions import ClientError


def upload_file_to_s3(local_file_name, bucket, s3_object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param s3_object_name: If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if s3_object_name is None:
        s3_object_name = local_file_name

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(local_file_name, bucket, s3_object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True