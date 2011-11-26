#!/usr/bin/env python
# encoding: utf-8
"""
mail.py

Created by 刘 智勇 on 2011-11-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""


import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


MAIL_SMTP = 'smtp.exmail.qq.com'
MAIL_FROM = 'no-reply@yimiqisan.com'
MAIL_SUBJECT = 'no reply'
MAIL_TEMPLATE='''
    Hello,<br/>welcome to use magicBox,Here is you password,please remember:<br/>

'''

def send_mail(to_list):
    try:
        smtp = smtplib.SMTP()    
        smtp.connect("smtp.exmail.qq.com")
        smtp.login(MAIL_FROM, 'yimiqisan')
        
        msg = MIMEMultipart() 
        msg['To'] = ";".join(to_list) 
        msg['From']= MAIL_FROM
        msg['Subject']= MAIL_SUBJECT
        body= MIMEText("%s" % MAIL_TEMPLATE,_subtype='html',_charset='gb2312')
        msg.attach(body)
        smtp.sendmail( msg['From'], to_list, msg.as_string())
        smtp.quit()
        return 'ok'
    except Exception, e:
        return e

if __name__=='__main__':
    EMAILTO = ['mark-warlike@qq.com']
    print send_mail(EMAILTO)