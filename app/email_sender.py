import boto3
from datetime import datetime
import flask_mail

from const import FORMATS

BUCKETS = {'json': 'reports-json',
           'csv': 'report-csv',
           'pdf': 'reports-pdf'}


def send_mail(app, data, format,
              mail_title='Report',
              file_name='Report',
              sender='testmicoac@gmail.com'):

    s3 = boto3.client('s3')
    file_type = [x for x, v in FORMATS.items()if v == format][0]
    file_name = '{}{}.{}'.format(app.user.name,
                                 datetime.now().strftime('%Y%m%d%H%M%S'),
                                 file_type)
    bucket_name = BUCKETS[file_type]
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=data)
    link = s3.generate_presigned_url(
        'get_object', Params={'Bucket': bucket_name, 'Key': file_name})
    mail = flask_mail.Mail(app)
    msg = flask_mail.Message(mail_title, sender=sender,
                             recipients=[app.user.email])
    msg.body = ('Here is a link (expire in 1 hour): \n {}').format(link)
    mail.send(msg)
    return True
