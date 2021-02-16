from minio import Minio
from minio.error import S3Error
from datetime import timedelta


def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "user-virtualbox.lan:32768",
        access_key="FAO5WMCSNYII9GNHMEVV6KX4",
        secret_key="rU7dkiJh4XN3dEoXeI9E2wdnIIUdZS9JuyFhG3F7r2UicIVU",
        secure=False,
    )
    """
    # Make 'asiatrip' bucket if not exist.
    found = client.bucket_exists("test")
    if not found:
        client.make_bucket("test")
    else:
        print("Bucket 'test' already exists")

    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
    client.fput_object(
        "test", "example.txt", "/home/user/my_minio_project/example.txt",
    )
    print(
        "'/home/user/my_minio_project/example.txt' is successfully uploaded as "
        "object 'example.txt' to bucket 'test'."
    )
    url = client.presigned_get_object(
        "test",
        "example.txt",
        expires=timedelta(hours=2),
    )
    print("link to file: " + url) """
    url = client.presigned_put_object("test", "jar.7z")
    print(url)


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
