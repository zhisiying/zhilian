# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
from zhilian.items import ZhilianItem
from scrapy.loader import ItemLoader


class ZhilianzhaopingSpider(scrapy.Spider):
    name = 'zhilianzhaoping'
    allowed_domains = ['sou.zhaopin.com']
    start_urls = [
        'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC&kw=%E7%88%AC%E8%99%AB%E5%B7%A5%E7%A8%8B%E5%B8%88&isadv=0&sg=f5bcbd571f734bfc85a7d6f9014088a0&p=1']

    def parse(self, response):
        href = response.xpath('//*[@id="newlist_list_content_table"]//div/a/@href').extract()
        for i in href:
            yield Request(url=i, callback=self.filter_Career, dont_filter=True)
        page = response.xpath('//li[@class="pagesDown-pos"]/a/@href').extract_first()
        # print(page)
        url = response.urljoin(page)
        yield Request(url=url, callback=self.parse)

    def filter_Career(self, response):
        url = response.url
        print(url)
        company_url = response.xpath('//div[@class="inner-left fl"]/h2/a/@href').extract_first()
        name = response.xpath('//div[@class="inner-left fl"]/h1/text()').extract_first()
        company = response.xpath('//div[@class="inner-left fl"]/h2/a/text()').extract_first()
        welfare = ','.join(response.xpath('//div[@class="welfare-tab-box"]/span/text()').extract())
        ul_xpath = '//ul[@class="terminal-ul clearfix"]/li'
        salary = response.xpath(ul_xpath + '/strong/text()').extract_first()
        location = response.xpath(ul_xpath + '/strong/a/text()').extract_first()
        job = response.xpath(ul_xpath + '/strong/a/text()').extract()[1]
        job_kind = response.xpath(ul_xpath + '[4]/strong/text()').extract_first()
        job_time = response.xpath(ul_xpath + '[5]/strong/text()').extract_first()
        xueli = response.xpath(ul_xpath + '[6]/strong/text()').extract_first()
        push_time = response.xpath('//*[@id="span4freshdate"]/text()').extract_first()
        people_num = response.xpath(ul_xpath + '[7]/strong/text()').extract_first()
        bs4 = BeautifulSoup(response.text, 'lxml')
        for terminalpage in bs4.find_all('div', class_='terminalpage-main clearfix'):
            for box in terminalpage.find_all('div', class_='tab-cont-box'):
                cont = box.find_all('div', class_='tab-inner-cont')[0]
                ms = cont.contents
                list = []
                for i in ms:
                    try:
                        if i.text.split() == []:
                            pass
                        else:
                            job_ms = ''.join(i.text.split())
                            list.append(job_ms)
                    except:
                        pass
                jog_location = ''.join(list).split('工作地址：').pop()
                job_mss = ''.join(list).split('工作地址：')[0]
                if job_mss == '':
                    job_ms = bs4.find('div', class_="tab-inner-cont")
                    job_mss = ''.join(job_ms.text.split()).split('工作地址')[0]
                loader = ItemLoader(item=ZhilianItem(), response=response)
                loader.add_value('url', url)
                loader.add_value('name', name)
                loader.add_value('company', company)
                loader.add_value('company_url', company_url)
                loader.add_value('welfare', welfare)
                loader.add_value('salary', salary)
                loader.add_value('location', location)
                loader.add_value('job', job)
                loader.add_value('job_kind', job_kind)
                loader.add_value('job_time', job_time)
                loader.add_value('xueli', xueli)
                loader.add_value('push_time', push_time)
                loader.add_value('people_num', people_num)
                loader.add_value('jog_location', jog_location)
                loader.add_value('job_mss', job_mss)
                print(loader.load_item())
                yield loader.load_item()
