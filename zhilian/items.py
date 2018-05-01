# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import Join, MapCompose, TakeFirst
import scrapy


class ZhilianItem(scrapy.Item):
    out_put  = scrapy.Field( output_processor=TakeFirst(),)
    url =  out_put
    name = out_put
    company_url =out_put
    company =out_put
    welfare = out_put
    salary = out_put
    location = out_put
    job = out_put
    job_kind = out_put
    job_time = out_put
    xueli = out_put
    push_time = out_put
    people_num = out_put
    jog_location = out_put
    job_mss = out_put

