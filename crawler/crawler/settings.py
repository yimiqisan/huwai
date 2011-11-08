# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

from mongokit import Connection

BOT_NAME = 'crawler'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
DEFAULT_ITEM_CLASS = 'crawler.items.CrawlerItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

#mongodb settings
DB_NAME = 'crawler'
DB_HOST = 'localhost'
DB_PORT = 27027
#DB_CON = Connection(host=DB_HOST, port=DB_PORT)

WEB_SITE = [
            {'allowd_domains':'www.517huwai.com','start_urls':'http://www.517huwai.com/Activity/index/p/1/','filter':'//dl','title':'dd/h1/a/text()','link':'dd/h1/a/@href','organizername':'dd/p[1]/span[1]/font/a/text()','activityclass':'dd/p[1]/span[2]/font/a/text()','place':'dd/p[2]/span/text()','time':'dd/p[3]/span/text()','hotnumber':'dd/p[4]/span[2]'},
            {'allowd_domains':'u.tourye.com/','start_urls':'http://u.tourye.com/space.php?uid=0&do=event&view=all&type=signing&classid=1&page=1','filter':'//ol/li','title':'div[2]/h4/a/text()','link':'div[2]/h4/a/@href','organizername':'div[2]/ul/li[3]/a/text()','activityclass':'div[2]/h4/span/text()','place':'div[2]/ul/li[2]','time':'div[2]/ul/li[1]','hotnumber':'div[2]/ul/li[4]/text()',},
        ]
