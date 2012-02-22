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

import uimethods

SITE_ID = u'917d450c728b4f62b6ac9bac1beb01ba'

#config settings
settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "htmls"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        login_url="/account/login",
        autoescape="xhtml_escape",
#        ui_modules=uimodules,
        ui_methods=uimethods,
#        xsrf_cookies=True,
        debug=True,
        cache_engine=redis.Redis(host='localhost', port=6379, db=1),
)

#mongodb settings
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

#thirdpart key list
SINA_CONSUME_KEY = '2798557074'
SINA_CONSUME_SECRET = '1540c762507cae70b0d81abdc2ad4d59'

DOUBAN_CONSUME_KEY = '697a5613626dfdc0'
DOUBAN_CONSUME_SECRET = '0d210d05553709372763270fffa51ba5'

KAIXIN_APP_ID = '100019696'
KAIXIN_CONSUME_KEY = '7052833246653cb4b04368a76c42789b'
KAIXIN_CONSUME_SECRET = '9ddbc8ed5cdef1d8a641653cc62414a5'

RENREN_APP_ID = '171267'
RENREN_CONSUME_KEY = 'd985117bff384fff909736978af0da63'
RENREN_CONSUME_SECRET = 'bab6147970dd49ab99b81fe105017123'

TX_CONSUME_KEY = '801072901'
TX_CONSUME_SECRET = 'd8721f9490268e6edf4ddb3687a6ffda'

QQ_CONSUME_KEY = '100243230'
QQ_CONSUME_SECRET = '93113512b242bfc9a08a8a99d3b5e25c'

TAOBAO_APP_KEY = '12484169'
TAOBAO_APP_SECRET = '8520cdb2c1ef7ff1c287944c4adfc4ac'

TAOBAO_TEST_KEY = '12484169'
TAOBAO_TEST_SECRET = 'sandbox2c1ef7ff1c287944c4adfc4ac'
