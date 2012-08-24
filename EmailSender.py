# -*- coding: utf-8 -*-
import __main__
import smtplib,mimetypes
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

class EmailSender(object):
    def __init__(self):
        self.email = 'nhmltq@163.com'
        self.password = 'fs452879'
        self.recv_list = 'flaresky@gmail.com'
        #self.recv_list = 'flaresky@qq.com'
        self.s = smtplib.SMTP('smtp.163.com')
        self.s.login(self.email, self.password)
    
    def send_mail(self, title, content):
        msg = MIMEMultipart()
        msg['Subject'] = title
        msg['From'] = self.email
        msg['To'] = self.recv_list        
        txt = MIMEText(content,_charset='utf-8')
        msg.attach(txt)
        self.s.sendmail(self.email, self.recv_list, msg.as_string())
    
    def close(self):
        self.s.close()

if __name__ == '__main__':
    es = EmailSender()
    es.send_mail('EmailSender Test', 'test')
    es.close()
