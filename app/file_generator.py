import csv
from flask import render_template
import json
import tempfile
from xhtml2pdf import pisa


def generate_json(data, **kwargs):
    temp = tempfile.TemporaryFile()
    temp.write(json.dumps(data,
                          indent=kwargs.get('indent')))
    temp.seek(0)
    return temp


def generate_csv(data, **kwargs):
    temp = tempfile.TemporaryFile()
    if not data:
        return temp
    headers = data[0].keys()
    writer = csv.DictWriter(temp, delimiter=kwargs.get('delimiter'),
                            quoting=csv.QUOTE_NONE,
                            fieldnames=headers)
    writer.writeheader()
    for item in data:
        writer.writerow(item)
    temp.seek(0)
    return temp


def generate_pdf(data, **kwargs):
    temp = tempfile.TemporaryFile()
    template = render_template(kwargs.get('template'),
                               items=data,
                               report_title=kwargs.get('title'))
    pisa.CreatePDF(template, dest=temp)
    temp.seek(0)
    return temp
