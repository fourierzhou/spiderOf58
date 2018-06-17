# -*- coding: utf-8 -*-
import re,requests

import scrapy
from dianyingtiantang.items import DianyingtiantangItem
from lxml import etree


class DyttSpider(scrapy.Spider):
    name = 'dytt'
    allowed_domains = ['www.ygdy8.net']
    start_urls = ['http://www.ygdy8.net/html/gndy/dyzz/index.html']
    # 下载程序
    def newParse(self, response):
        download_url = response.xpath('//tbody/tr/td/a/@href').extract_first()
        print('下载地址为',download_url)


    def parse(self, response):
        table_list = response.xpath('//table[contains(@class,"tbspan")]')
        words = response.xpath('//div[@class="x"]//option[last()]/text()').extract_first()
        pattern = r'(\d+)'
        reg = re.compile(pattern)
        max_page = reg.findall(words)[0]
        max_page = int(max_page)
        url_list = []
        for table in table_list:
            name = table.xpath('.//tr[2]//a/text()').extract_first()
            href = 'http://www.ygdy8.net' + table.xpath('./tr[2]//a/@href').extract_first()
            item = DianyingtiantangItem()
            item["name"] = name
            item["link"] = href
            url_list.append(href)
            yield item

        for page in range(2,max_page):
            url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_{}.html'.format(page)
            yield scrapy.Request(url, callback=self.parse)

        for url in url_list:
            print('页面地址为',url)
            yield scrapy.Request(url, callback=self.newParse)



