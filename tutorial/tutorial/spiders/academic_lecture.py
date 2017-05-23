import scrapy
from tutorial.items import Lecture
from scrapy.loader import ItemLoader
import json
import hashlib

class SustcLecturesSpider(scrapy.Spider):
    name = 'sustc_lectures'
    start_urls = [
        'http://sustc.edu.cn/news_events_jiangzuo'
    ]

    def parse(self, response):
        for lecture in response.css('div.clearfix.block'):
            lecture_info = Lecture()
            lecture_info['lecturer'] = lecture.css('div.t2::text').extract_first()
            lecture_info['time'] = lecture.css('div.t3::text').extract_first()
            lecture_info['location'] = lecture.css('div.t4::text').extract_first()
            lecture_info['weekday'] = lecture.css('div.week::text').extract_first()
            lecture_info['type'] = lecture.css('div.t0::text').extract_first()
            lecture_info['title'] = lecture.css('h2 a::attr(title)').extract_first()
            lecture_info['url'] = 'http://sustc.edu.cn' + lecture.css('h2 a::attr(href)').extract_first()
            yield response.follow(lecture_info['url'], meta={'lecture_info': lecture_info}, callback=self.second_parse)

        # check whether have next page
        for item in response.css('div.page_bar.block18 a'):
            if '下一页' in item.get():
                yield response.follow(item.css("::attr(href)").extract_first(), callback=self.parse)

    def second_parse(self, response):
        lecture_info = response.meta['lecture_info']
        lecture_info['date'] = response.css('div.txt .t0::text').extract_first()[:10]
        lecture_info['poster_url'] = 'http://sustc.edu.cn' + response.css('div.txt .t6 img::attr(src)').extract_first()
        lecture_info['hash_code'] = get_md5(json.dumps(dict(lecture_info), ensure_ascii=False, indent=2, sort_keys=True))
        return lecture_info

def get_md5(string):
    hash_md5 = hashlib.md5(string.encode('utf-8'))
    return hash_md5.hexdigest()