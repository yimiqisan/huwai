#!/usr/bin/env python
# encoding: utf-8
"""
517huwai.py

Created by 刘 智勇 on 2011-11-08.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import string
from datetime import datetime
from scrapy.spider import BaseSpider
from bs4 import BeautifulSoup, re
from urllib2 import urlopen
from crawler.items import Huwai517Item

from huwai.config import CLUB_WEBSITE

class hw517Spider(BaseSpider):
    name = "c_517"
    domain = 'www.517huwai.com'
    allowed_domains = ['www.517huwai.com']
    start_urls=[
        'http://www.517huwai.com/Activity',
    ]
    
    def _flt_eid(self, h):
        return h.split('/')[-1]
    
    def _mkflt(self, s):
        r = ''
        k = string.digits + '- :,'
        for i in xrange(0, len(s)):
            if s[i] in k: r+=s[i]
        return r
    
    def _flt_date(self, d):
        prefix = str(datetime.now().year)+'-'
        l = d.split(u'至')
        start = datetime.strptime(prefix+self._mkflt(l[0]).strip(), '%Y-%m-%d')
        if len(l) > 1:
            ll = self._mkflt(l[1])
            end = datetime.strptime(prefix+ll.strip(), '%Y-%m-%d')
            result = end - start
            day = result.days if result.days>0 else 1
        else:
            day = 1
        return start, day
    
    def parse(self, response):
        prefix = 'http://'+self.domain
        soup = BeautifulSoup(response.body)
        el = soup.find_all(id='actlist')[0]
        es = el.find_all('dl')
        items = []
        for e in es[:5]:
            item = Huwai517Item()
            address = prefix + e.dt.find_all('a')[0].get('href').strip()
            print address
            child_soup = BeautifulSoup(urlopen(address))
            act = child_soup.find_all('div', {'class':'acv_showBox'})[0]
            comr = act.find_all('div', {'class':'comr'})[1]
            comt = act.find_all('p')
            try:
                item['eid'] = unicode(self._flt_eid(address))
                item['club'] = CLUB_WEBSITE[self.name]
                item['title'] = comr.find_all('div', {'class':'tit'})[0].get_text().strip()
                item['created'] = datetime.now()
                item['logo'] = unicode(prefix+act.find_all('img')[0].get('src').strip())
                item['tags'] = comt[4].get_text().strip()
                item['date'], item['day'] = self._flt_date(comt[8].get_text().strip())
                item['place'] = comt[9].get_text().strip()
                item['nick'] = unicode(comt[0].get_text().strip())
                deadline = str(datetime.now().year)+'-'+self._mkflt(comt[14].get_text()).strip()
                item['deadline'] = datetime.strptime(deadline, '%Y-%m-%d,%H:%M')
                item['href'] = unicode(address)
                items.append(item)
            except Exception, e:
                print e
                continue
        return items