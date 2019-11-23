# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class ExampleItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class book_info(Item):
	name = Field()
	price = Field()
	rank = Field()
	ISBN = Field()
	stockamount = Field()
	reviewamount = Field()

class pltItem(Item):
	file_urls = Field()
	files = Field()
	