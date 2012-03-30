#!/usr/bin/env python
# encoding: utf-8

import sys
import string
from datetime import datetime
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from bs4 import BeautifulSoup, re
from urllib2 import urlopen
from crawler.items import Huwai8264Item

from huwai.config import CLUB_WEBSITE

class E8264Spider(BaseSpider):
    name = "c_8264"
    domain = 'bbs.8264.com'
    allowed_domains = ["8264.com"]
    start_urls = [
        "http://bbs.8264.com/forum-forumdisplay-fid-101-filter-specialtype-specialtype-activity.html",
    ]
    
    def _flt_eid(self, h):
        m = re.match(r'.*thread-(\d+)-1-1\.html.*', h)
        return m.group(1)
    
    def _mkflt(self, s):
        r = ''
        k = string.digits + '- :'
        for i in xrange(0, len(s)):
            if s[i] in k: r+=s[i]
        return r
    
    def _flt_date(self, d):
        l = d.split(u'至')
        start = datetime.strptime(l[0].strip(), '%Y-%m-%d %H:%M')
        if len(l) > 1:
            ll = self._mkflt(l[1])
            end = datetime.strptime(ll.strip(), '%Y-%m-%d %H:%M')
            result = end - start
            day = result.days if result.days>0 else 1
        else:
            day = 1
        return start, day
    
    def parse(self, response):
        soup = BeautifulSoup(response.body)
        el = soup.find_all('table', {'summary':'forum_101'})[0]
        es = el.find_all('tbody')
        items = []
        for e in es[:2]:
            item = Huwai8264Item()
            th = e.th.find_all('a')
            td = e.find_all('td')
            if len(th) < 2:continue
            address = th[1].get('href').strip()
            print address
            nick = e.cite.find_all('a')[0].get_text().strip()
            child_soup = BeautifulSoup(urlopen(address))
            act = child_soup.find_all('div', {'class':'act'})[0]
            try:
                item['eid'] = unicode(self._flt_eid(address))
                item['club'] = CLUB_WEBSITE[self.name]
                item['title'] = th[1].get_text().strip()
                item['created'] = datetime.strptime(td[1].em.get_text().strip(), '%Y-%m-%d')
                item['logo'] = logo
                item['tags'] = dd[0].get_text().strip()
                item['date'], item['day'] = self._flt_date(dd[1].get_text().strip())
                item['place'] = dd[2].get_text().strip()
                item['nick'] = nick
                item['deadline'] = datetime.strptime(dd[-2].get_text().strip(), '%Y-%m-%d %H:%M')
                item['href'] = unicode(address)
                items.append(item)
            except Exception, e:
                print e
                continue
        return items

