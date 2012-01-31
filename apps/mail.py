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
import logging
import uuid

from huwai.config import DB_CON, DB_NAME, SITE_ID
from modules import TmpTableDoc
from api import API

class TmpTable(object):
    def __init__(self, id=None, api=None):
        self._api = api if api else TmpTableAPI()
        if id:
            ret = self._api.one(_id=id)
            self.info, self.eid = (ret[1], ret[1]['_id']) if ret[0] else (None, None)
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None
    
class TmpTableAPI(API):
    def __init__(self):
        DB_CON.register([TmpTableDoc])
        datastore = DB_CON[DB_NAME]
        col_name = TmpTableDoc.__collection__
        collection = datastore[col_name]
        doc = collection.TmpTableDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def set(self, email):
        return super(TmpTableAPI, self).create(email=email)
    
    def unset(self, id):
        return super(TmpTableAPI, self).remove(id)
    
    def check(self, id):
        r = self.one(_id=id)
        self.unset(id)
        return r[1]['email']

class Mail(object):
    def __init__(self, to):
        self.smtp = self._p_smtp(to)
        self.fr = 'no-reply@yimiqisan.com'
        self.to = to
    
    def _p_smtp(self, to):
        a, b = to.split('@')
        c = b.split('.')[0]
        if c == 'qq':
            return 'smtp.exmail.qq.com'
        else:
            return 'smtp.'+b
    
    def get_template(self, no, code):
        if (no=='invite'):
            return '''Hello,<br/>click this url for register http://127.0.0.1:8000/account/register/?icode=%s<br/>'''%code
        else:
            return ''' no thing '''
    
    def send(self, subject, tno, code, to_l=None):
        try:
            smtp = smtplib.SMTP()    
            smtp.connect(self.smtp)
            smtp.login(self.fr, 'yimiqisan')
            msg = MIMEMultipart() 
            to = ";".join(to_l) if to_l else self.to
            msg['To'] = to
            msg['From']= self.fr
            msg['Subject']= subject
            body= MIMEText("%s" % self.get_template(tno, code), _subtype='html', _charset='gb2312')
            msg.attach(body)
            smtp.sendmail( msg['From'], to, msg.as_string())
            smtp.quit()
            return (True, 'ok')
        except Exception, e:
            print e
            return (False, e)

if __name__=='__main__':
    m = Mail('mark-warlike@qq.com')
    print m.send('hello this is yuanhang', 'invite')
    
    
    