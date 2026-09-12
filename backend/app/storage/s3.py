import boto3

from boto3.s3.transfer import TransferConfig

from app.config import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key = settings.aws_secret_access_key,
    region_name=settings.aws_region
)

transfer_config = TransferConfig(
    multipart_threshold=5 * 1024 * 1024,
    multipart_chunksize=5* 1024 *1024,
    max_concurrency=4,
)

def generate_presigned_url(
    object_key: str,
    expiration: int = 900
):
    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.aws_s3_bucket_name,
            "Key": object_key
        },
        ExpiresIn=expiration
    )

def upload_file_to_s3(
        file,
        object_key: str,
        content_type: str
):
    s3_client.upload_fileobj(
        file,
        settings.aws_s3_bucket_name,
        object_key,
        ExtraArgs={
            "ContentType": content_type
        },
        Config=transfer_config

    )