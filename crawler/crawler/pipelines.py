from datetime import datetime
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from huwai.apps.event import EventScrapyAPI
from huwai.config import SITE_ID
from settings import TIME_FORMAT


class StorePipeline(object):
    def process_item(self, item, spider):
        #api = EventScrapyAPI()
        #r = api.save(SITE_ID, item['club'], item['eid'], item['logo'], item['title'], tags=item['tags'], date=item['date'], day=item['day'], place=item['place'], href=item['href'], deadline=item['deadline'], created=item['created'], nick=item['nick'])
        return item
