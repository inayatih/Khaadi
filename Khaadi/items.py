# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KhaadiItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    special_price = scrapy.Field()
    regular_price = scrapy.Field()
    description = scrapy.Field()
    detail = scrapy.Field()
    size = scrapy.Field()
    category = scrapy.Field()
    product_url = scrapy.Field()
    image_url = scrapy.Field()
