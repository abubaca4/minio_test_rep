from minio import Minio

client = Minio(
    "83.149.198.179",
    access_key="FAO5WMCSNYII9GNHMEVV6KX4",
    secret_key="rU7dkiJh4XN3dEoXeI9E2wdnIIUdZS9JuyFhG3F7r2UicIVU",
    secure=False,
)

if not client.bucket_exists("ecg.storage"):
    client.make_bucket("ecg.storage")
