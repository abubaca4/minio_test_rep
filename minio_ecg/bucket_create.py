from minio import Minio

client = Minio(
    "s3:9000",
    access_key="FAO5WMCSNYII9GNHMEVV6KX4",
    secret_key="rU7dkiJh4XN3dEoXeI9E2wdnIIUdZS9JuyFhG3F7r2UicIVU",
    secure=False,
)

bucket_name = "ecg.storage"

if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)
