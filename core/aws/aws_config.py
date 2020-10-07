import os

from app.core.base_config import BaseConfig


class AWSConfig(BaseConfig):
    S3_DEFAULT_BUCKET = os.getenv("AWS_S3_DEFAULT_BUCKET")
    S3_IMAGE_BUCKET = os.getenv("AWS_S3_IMAGE_BUCKET")
    SNS_DEFAULT_REGION = os.getenv("AWS_SNS_DEFAULT_REGION")
    AWS_LAMBDA_TRIGGER_HLS = os.getenv("AWS_LAMBDA_TRIGGER_HLS")
