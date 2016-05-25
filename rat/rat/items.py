# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RatItem(scrapy.Item):	
    lineName = scrapy.Field()
    lineNr = scrapy.Field()
    station = scrapy.Field()
    mon_fri = scrapy.Field()
    saturday = scrapy.Field()
    sunday = scrapy.Field()
    hasExtraStations = scrapy.Field()
    hasHandicapRide = scrapy.Field()