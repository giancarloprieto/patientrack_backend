from storages.backends.s3boto3 import S3Boto3Storage as OriginalS3Boto3Storage

from patientrack.settings import AWS_STORAGE_BUCKET_NAME


class S3Boto3Storage(OriginalS3Boto3Storage):
    location = 'media'


class S3Boto3StoragePublic(OriginalS3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
    bucket_name = AWS_STORAGE_BUCKET_NAME
    custom_domain = '%s.s3.amazonaws.com' % bucket_name