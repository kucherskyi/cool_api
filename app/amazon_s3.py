import boto3
from datetime import datetime

from const import FORMATS

BUCKETS = {'json': 'reports-json',
           'csv': 'report-csv',
           'pdf': 'reports-pdf'}

s3 = boto3.client('s3')


def send_to_s3(data, data_format):
    file_type = [x for x, v in FORMATS.items()if v == data_format][0]
    bucket_name = BUCKETS[file_type]
    file_name = '{}.{}'.format(datetime.now().strftime('%Y%m%d%H%M%S'),
                               file_type)
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=data)
    return {'bucket_name': bucket_name,
            'file_name': file_name}


def generate_link_to_attach(bucket_name, attach_key):
    link = s3.generate_presigned_url(
        'get_object', Params={'Bucket': bucket_name, 'Key': attach_key})
    return link
