import scrapy
import json
import re
import time
from ast import literal_eval
from dateutil.parser import parse

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import get_base_url

from ..items import CorpusItem
from ..utils import *


class FirstpostSpider(CrawlSpider):
    name = "firstpost"
    allow_domain = ['firstpost.in']

    urls = "https://www.firstpost.com/category/politics/page/{}"
    start_page = 1
    start_urls = [urls.format(str(start_page))]

    def parse(self, response):
        all_links = response.xpath('.//*[@class="articles-list"]/li/a/@href').extract()
        for link in all_links:
            yield scrapy.Request(url=link, callback=self.extract_data)

        if len(all_links) > 0 and self.start_page < 780:
            self.start_page += 1
            yield scrapy.Request(self.urls.format(str(self.start_page)), callback=self.parse)
            time.sleep(2)

    @error_handler
    def get_date(self, response):
        date = response.xpath('.//*[@class="article-date"]/text()').extract_first()
            #'//*[@id="middle_container"]/div[2]/div[1]/span[2]/a/text()').extract()[0]
        date = parse(date)
        return date

    def extract_data(self, response):
        url = response._url
        date = self.get_date(response)
        content = get_content(
            response, path='.//*[@class="article-full-content"]/p/text()')
        title = get_title(
            response, path='.//*[@class="page-title article-title"]/text()')
        author = get_author(
            response, path='.//*[@class="article-by"]/text()')

        tag = get_tag(response, './/*[@class="article-tags hidden-xs hidden-sm"]/a/text()')

        tab = CorpusItem()
        tab['content'] = content
        tab['title'] = title
        tab['author'] = author
        tab['tag'] = tag
        tab['date'] = date
        tab['url'] = url
        yield tab
