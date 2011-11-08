# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Huwai517Item(Item):
    # define the fields for your item here like:
    # name = Field()
    innerItem={}
    namelist = {'title':'dd/h1/a/text()','link':'dd/h1/a/@href','organizername':'dd/p[1]/span[1]/font/a/text()','activityclass':'dd/p[1]/span[2]/font/a/text()','place':'dd/p[2]/span/text()','time':'dd/p[3]/span/text()','hotnumber':'dd/p[4]/span[2]'}
    for item in namelist:
        innerItem[item] = Field()


class TouryeItem(Item):
    # define the fields for your item here like:
    # name = Field()
    innerItem={}
    namelist = {'title':'div[2]/h4/a/text()','link':'div[2]/h4/a/@href','organizername':'div[2]/ul/li[3]/a/text()','activityclass':'div[2]/h4/span/text()','place':'div[2]/ul/li[2]','time':'div[2]/ul/li[1]','hotnumber':'div[2]/ul/li[4]/text()',}
    for item in namelist:
        innerItem[item] = Field()