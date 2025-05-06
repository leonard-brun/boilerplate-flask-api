import boto3
import logging
from botocore.exceptions import ClientError
from flask import current_app

logger = logging.getLogger(__name__)

BUCKET_NAME = "boilerplate"


def get_client(name):
    return boto3.client(
        name,
        aws_access_key_id=current_app.config.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=current_app.config.get("AWS_SECRET_ACCESS_KEY"))


def upload_fileobj(data, path, options=None, public=False):
    client = get_client("s3")

    l_options = options or {}
    if public:
        l_options.update({"ACL": "public-read"})

    try:
        client.upload_fileobj(data, BUCKET_NAME, path, ExtraArgs=l_options)
    except ClientError as e:
        logger.exception(e)
        return False
    return True


def get_public_url(key):
    region = current_app.config.get("AWS_DEFAULT_REGION")
    return "https://s3-{0}.amazonaws.com/{1}/{2}".format(region, BUCKET_NAME, key)
