#!/usr/bin/env python
# encoding: utf-8
"""
517huwai.py

Created by 刘 智勇 on 2011-11-08.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import json
import os
import uuid

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawler.items import Huwai517Item

class hw517Spider(BaseSpider):
	name = "517huwai"
	domain = 'www.517huwai.com'
	allowed_domains = ['www.517huwai.com']
	start_urls=['http://www.517huwai.com/Activity/index/p/1/']
	def parse(self, response):
#		obj= dboperator.Dboperator()
		hxs = HtmlXPathSelector(response)
		ff = '//dl'
		sites = hxs.select(ff)
		filters = {'title':'dd/h1/a/text()','link':'dd/h1/a/@href','organizername':'dd/p[1]/span[1]/font/a/text()','activityclass':'dd/p[1]/span[2]/font/a/text()','place':'dd/p[2]/span/text()','time':'dd/p[3]/span/text()','hotnumber':'dd/p[4]/span[2]'}
		preurl= self.domain
		for site in sites:
			item = Huwai517Item()
			add = True
			haha={}
			for name in item.innerItem:
				exdata  = site.select(filters[name]).extract()
				print exdata
				if len(exdata) == 0:
					add = False
					break
				else:
					if cmp("link", name) == 0 and exdata[0].find("http://") == -1:
						haha[name] = "http://"+preurl+exdata[0]
					elif cmp("place", name) == 0 and exdata[0].find("<") != -1:
						place = exdata[0].split(">")	
						place.remove(place[0])
						place.remove(place[0])
						place2=""
						while 1 < len(place):
							place2 += place[0].split("<")[0]
							place.remove(place[0])
						haha[name] = place2
					elif cmp("time", name) ==0 and exdata[0].find("<") !=-1:
						timestr = exdata[0].split(">")	
						timestr.remove(timestr[0])
						timestr.remove(timestr[0])
						timestr2=""
						while 1 < len(timestr):
							timestr2 += timestr[0].split("<")[0]
							timestr.remove(timestr[0])
						haha[name] = timestr2
					elif cmp("hotnumber", name) == 0 and exdata[0].find("<") != -1:	
						hotstr = exdata[0].split(">")	
						hotstr.remove(hotstr[0])
						hotstr.remove(hotstr[0])
						hotstr2=""
						while 1 < len(hotstr):
							hotstr2 += hotstr[0].split("<")[0]
							hotstr.remove(hotstr[0])
						haha[name] = hotstr2
					else:
						haha[name] = exdata[0]
			if add:
				haha["uuid"] = unicode(uuid.uuid4().hex)
				print haha
#				obj.putDatatoBase(haha)	

