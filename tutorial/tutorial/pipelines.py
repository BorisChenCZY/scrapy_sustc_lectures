# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import json
import mysql.connector
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
# from lxml.html.soupparser import unescape

class TutorialPipeline(object):
    def __init__(self):
        self.file = open('item.json', 'w')

    def process_item(self, item, spider):
        line =json.dumps(dict(item), ensure_ascii=False, indent=2) + '\n'
        self.file.write(line)
        inser_data(self.db, self.cursor, 'lectures_', **dict(item))
        return item

    def open_spider(self, spider):
        #here you should modify for your own database.
        self.db = mysql.connector.connect(user='username', password='password', database='lectures',
                                     use_unicode=True, host = 'borischen.me')
        self.cursor = self.db.cursor()

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # for image_url in item['poster_url']:
            # self.log(image_url)
        yield scrapy.Request(item['poster_url'], meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['poster_url'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = request.url.split('/')[-1]
        suffix = image_guid.split('.')[-1]
        name = '{title} {location} {time} {lecturer}'.format(
                                                      title = item['title'],
                                                      location = item['location'],
                                                      time = item['time'],
                                                      lecturer = item['lecturer'],)
        # print(name + '.' + suffix)
        # print(image_guid)
        return 'full/{date}/{name}'.format(date = item['date'], name =(name + '.' + suffix))

def inser_data(db, cursor, table_name, **kwargs):
    s = 'INSERT INTO {table_name} {columnNames} VALUES {values}'.format(table_name = table_name, columnNames = str(tuple(kwargs.keys())).replace("'", ""), values=tuple(kwargs.values() ))
    cursor.execute(s)
    db.commit()

