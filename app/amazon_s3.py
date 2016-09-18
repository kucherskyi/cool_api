import boto3


s3 = None


def send_to_s3(bucket, key, data):
    if not s3:
        global s3
        s3 = boto3.client('s3')
    s3.upload_fileobj(data, bucket, key)


def generate_link_to_attach(bucket, key):
    if not s3:
        global s3
        s3 = boto3.client('s3')
    link = s3.generate_presigned_url(
        'get_object', Params={'Bucket': bucket, 'Key': key})
    return link
