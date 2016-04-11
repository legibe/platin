import os
import smtplib
from ..core.basic import make_list
from ..core.config import Config
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.Utils import COMMASPACE

class GMail(object):

    def __init__(self,email_to,email_from,email_subject,email_bcc=[]):
        self._msg = MIMEMultipart()
        self._msg['Subject'] = email_subject
        self._msg['From'] = email_from
        self._recipients = make_list(email_to)
        self._msg['To'] = COMMASPACE.join(self._recipients)
        self._bcc = make_list(email_bcc)

    def addContents(self,contents):
        self._msg.attach(MIMEText(contents))

    def addFileAttachment(self,filename):
        extension = os.path.splitext(filename)[1]
        if extension in set(['.csv','.txt','pdf']):
            self.addTextFileAttachment(filename)
        elif extension in set(['.png','.jpeg','.jpg']):
            self.addImageFileAttachment(filename)
        else:
            raise ValueError('unknow extension: %s' % extension)

    def addTextAttachment(self,text,name=''):
        text = MIMEText(text)
        text.add_header('Content-Disposition', 'attachment',filename=name)
        self._msg.attach(text)

    def addTextFileAttachment(self,filename):
        with open(filename) as f:
            text = f.read()
            self.addTextAttachment(text,os.path.basename(filename))

    def addImageAttachment(self,img,name=''):
        img = MIMEImage(img)
        img.add_header('Content-Disposition', 'attachment',filename=name)
        self._msg.attach(img)

    def addImageFileAttachment(self,filename):
        with open(filename) as f:
            img = f.read()
            self.addImageAttachment(img,os.path.basename(filename))

    def send(self):
        filename = os.path.join(os.path.join(os.path.expanduser("~"),'.dbs'),'.gmail.yaml')
        config = Config.read(filename)
        gmail_user = self._msg['From']
        gmail_pwd = config['credentials'][gmail_user]
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(self._msg['From'], self._recipients, self._msg.as_string())
        if len(self._bcc) > 0:
            server.sendmail(self._msg['From'], self._bcc, self._msg.as_string())
        server.close()
