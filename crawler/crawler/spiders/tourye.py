#!/usr/bin/env python
# encoding: utf-8
"""
tourye.py

Created by 刘 智勇 on 2011-11-08.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import json
import os
import uuid

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawler.items import TouryeItem

class TouryeSpider(BaseSpider):
	name = "tourye"
	domain = 'u.tourye.com/'
	allowed_domains = ['u.tourye.com']
	start_urls=['http://u.tourye.com/space.php?uid=0&do=event&view=all&type=signing&classid=1&page=1']
	def parse(self, response):
#		obj= dboperator.Dboperator()
		hxs = HtmlXPathSelector(response)
		ff = '//ol/li'
		sites = hxs.select(ff)
		filters = {'title':'div[2]/h4/a/text()','link':'div[2]/h4/a/@href','organizername':'div[2]/ul/li[3]/a/text()','activityclass':'div[2]/h4/span/text()','place':'div[2]/ul/li[2]','time':'div[2]/ul/li[1]','hotnumber':'div[2]/ul/li[4]/text()'}
		preurl= self.domain
		for site in sites:
			item = TouryeItem()
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

