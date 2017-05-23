# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Lecture(scrapy.Item):
    info = [
        'lecturer',
        'weekday', # 星期
        'time', # 日期+时间
        'location',
        'type',
        'url',
        'title',
        'date',
        'poster_url',
        'hash_code',
    ]

    lecturer = scrapy.Field()
    weekday = scrapy.Field()
    time = scrapy.Field()
    location = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    poster_url = scrapy.Field()
    hash_code = scrapy.Field()
    image_urls = scrapy.Field()