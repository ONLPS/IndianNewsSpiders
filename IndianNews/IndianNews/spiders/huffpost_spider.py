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


class HuffpostSpider(CrawlSpider):
    name = "huffpost"
    allow_domain = ['huffpost.in']

    urls = "https://www.huffingtonpost.in/politics/{}/"
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64)"
    start_page = 1
    start_urls = [urls.format(str(start_page))]

    def parse(self, response):
        print( "\n\n\n-----------------------------------\n\n\n")
        center_link = response.xpath('.//*[@class="col col--body-center bnp__card-list yr-col-body-center"]')

        all_links = center_link.xpath('.//*[@class="apage-rail-cards"]/div/div/a/@href').extract()
        print(len(all_links))
        for link in all_links:
            
            link = "https://www.huffingtonpost.in"+link
            yield scrapy.Request(url=link, callback=self.extract_data)
        time.sleep(2)

        """if len(all_links) > 0 and self.start_page < 5:
            self.start_page += 1
            yield scrapy.Request(self.urls.format(str(self.start_page)), callback=self.parse)
            time.sleep(2)
"""
    @error_handler
    def get_date(self, response):
        date = response.xpath('.//*[@class="article-date"]/text()').extract_first()
            #'//*[@id="middle_container"]/div[2]/div[1]/span[2]/a/text()').extract()[0]
        date = parse(date)
        return date

    def extract_data(self, response):
        
        title = get_title(
            response, path='.//*[@class="headline__title"]/text()')
        print("\n----------------\n{}\n----------------\n".format(title))

        """url = get_base_url(response)
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
        yield tab"""
