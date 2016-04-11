import os
import sys
from platin.gmail.gmail import GMail

if len(sys.argv) < 3:
    raise ValueError('Expectes 2 arguments: subject and body')

allowed_file_types = set(['png','csv','txt','pdf','.jpg','.jpeg'])

subject = sys.argv[1]
body = sys.argv[2]
files = sys.argv[3:]
print subject
print body
efrom = os.getenv('SCHEDULER_EMAIL')
eto = [ x.strip() for x in os.getenv('SCHEDULER_ADMIN').split(',') ]
mail = GMail(eto,efrom,subject)
mail.addContents(body)
for filepath in files:
    l = filepath.split('.')
    extension = l[-1]
    if extension in allowed_file_types:
        mail.addFileAttachment(filepath)
mail.send()
