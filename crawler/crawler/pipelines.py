import sqlite3
from os import path
 
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from settings import DB_CON, DB_NAME


class StorePipeline(object):
    def __init__(self):
        dispatcher.connect(self.start, signals.spider_opened)
        dispatcher.connect(self.stop, signals.spider_closed)
    
    def start(self, spider):
        pass
        #self._api = EventAPI(db_name=DB_NAME)
    
    def stop(self, spider):
        pass
        
    def process_item(self, item, spider):
        print '================ in ==================='
        print item
        #self._api.save_step_one(owner, logo, title, tags, is_merc, level, date, place, schedule_tl, nick=None, members=None, club=None, route=None, spend_tl=None, equip=None, declare_tl=None, attention_tl=None)
        print '================ out =================='
        return item
    
class Huwai8264Pipeline(StorePipeline):
    pass
    