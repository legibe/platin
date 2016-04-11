import os
import sys
import subprocess
from platin.core.basic import substitute_env_variables
from platin.core.config import Config
from platin.gmail.gmail import GMail

if len(sys.argv) < 3:
    raise ValueError('emailreports requires 1 argument, the product name and the template filename')

allowed_file_types = set(['png','csv','txt','pdf','.jpg','.jpeg'])

product_name = sys.argv[1]
template_name = sys.argv[2]
files = sys.argv[2:]
status = os.getenv('EMAIL_STATUS','1')
# no emails to send stop here
if status == '1':
    exit(0)

configdir = os.getenv('CONFIG_DIR','./')
config = Config.read('%s/email.yaml' % configdir)
templates = Config.read('%s/%s' % (configdir,template_name))

if not product_name in templates:
    raise IndexError('cannot find product %s in the template file' % product_name)

product = templates[product_name]
sender = product['sender']
recipients = config['admin']
bcc = []
if status == '3':
    recipients = [ y for x in product['recipients'] for y in config[x] ]
    bcc = config['admin'] + product['bcc']

subject = substitute_env_variables(product['subject'])
body = substitute_env_variables(product['body'])

print
print 'sender:',sender
print 'recipients:',', '.join(recipients)
print 'subject:',subject
print 'bcc:',', '.join(bcc)
print 'product name:',product_name
print 'attachments:',', '.join(files)
print 'body:',body
print

mail = GMail(email_from=sender,email_to=recipients,email_subject=subject,email_bcc=bcc)
mail.addContents(body)
for filepath in files:
    l = filepath.split('.')
    extension = l[-1]
    if extension in allowed_file_types:
        mail.addFileAttachment(filepath)

print 'sending report(s) by email'
mail.send()
