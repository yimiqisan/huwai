#!/usr/bin/env python
# encoding: utf-8
"""
config.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import os
import redis
from mongokit import Connection
from logging import basicConfig, DEBUG

import uimethods, uimodules

SITE_ID = u'917d450c728b4f62b6ac9bac1beb01ba'
DEFAULT_CUR_UID = '948a55d68e1b4317804e4650a9505641'

PERM_CLASS = {
    'FOUNDER':      0x01,
    'VERIFIER':     0x02,
    
    'cFOUNDER':     0x10,
    'cMANAGER':     0x11,
    'cMEMBER':      0x12,
    
    'eSPONSOR':     0x20,
    'eASSISTANT':   0x21,
    'ePARICIPANT':  0x22,
    
    'nFOUNDER':     0x30,
    
    'aFOUNDER':     0x50,
    'aEDITER':      0x51,
    
    'wFOUNDER':     0x70,
    
    'NORMAL':       0X90,
}

FOUNDER_LIST = [
    u'2d40119715674d82a38216009efe528e',
    u'c18db1940a5e4c00a4b29f7206bc953f',
]


#config settings
settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "htmls"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        login_url="/account/login",
        autoescape="xhtml_escape",
        ui_modules=uimodules,
        ui_methods=uimethods,
#        xsrf_cookies=True,
        debug=True,
        cache_engine=redis.Redis(host='localhost', port=6379, db=1),
)

#mongodb settings
DB_SCRAPY_NAME = 'crawler'
DB_NAME = 'huwai'
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DB_CON = Connection(host=MONGO_HOST, port=MONGO_PORT)

#session initialize settings
SESSION_SET = {
    "SESSION_EXPIRE_TIME": 86400,    # sessions are valid for 86400 seconds (24 hours)
    "REDIS_URL": {'ip': 'localhost', 'port': 6379, 'db': 0, },
}

#loggging config
basicConfig(filename = 'app.log',
            format = '%(asctime)s %(module)s %(lineno)s %(message)s',
            level = DEBUG
)
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

CLUB_WEBSITE = {
    "c_8264":       u"b096ba6ee2d34a649be11d3d45eddc60",
    "c_517":        u"608fb0bcf528477ab2cd166a17738b28",
    "c_tourye":     u"23b22295c6de483481242fdcdf1afbff",
    "c_lvye":       u"ac061d953c564bb5ba987df50fc6baf8",
    "c_doyouhike":  u"ddb2d797c1424cb298edcf4bf20bb70d",
    "c_lvzhou":     u"461a993f6ba448b7a13a4335f3ff6a83"
}

#thirdpart key list
SINA_CONSUME_KEY = '2729924436'
SINA_CONSUME_SECRET = '74ad4b5f9fe4c391d618ec447f834e1c'

DOUBAN_CONSUME_KEY = ''
DOUBAN_CONSUME_SECRET = ''

KAIXIN_APP_ID = ''
KAIXIN_CONSUME_KEY = ''
KAIXIN_CONSUME_SECRET = ''

RENREN_APP_ID = ''
RENREN_CONSUME_KEY = ''
RENREN_CONSUME_SECRET = ''

TX_CONSUME_KEY = ''
TX_CONSUME_SECRET = ''

QQ_CONSUME_KEY = '100267721'
QQ_CONSUME_SECRET = 'afb6055be0c0cf1596b3c0ab6061f39d'

TAOBAO_APP_KEY = ''
TAOBAO_APP_SECRET = ''

TAOBAO_TEST_KEY = ''
TAOBAO_TEST_SECRET = ''
