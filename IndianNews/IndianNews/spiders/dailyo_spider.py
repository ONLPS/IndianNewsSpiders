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


class DailyOSpider(CrawlSpider):
    name = "dailyo"
    allow_domain = ['dailyo.in']

    urls = "https://www.dailyo.in/politics/?page={}"
    start_page = 1
    start_urls = [urls.format(str(start_page))]

    def parse(self, response):
        all_links = response.xpath('.//div/div[2]/div[2]/h2/a/@href').extract()
        for link in all_links:
            link = "https://www.dailyo.in"+link
            yield scrapy.Request(url=link, callback=self.extract_data)
        time.sleep(2)

        if len(all_links) > 0 and self.start_page < 5:
            self.start_page += 1
            yield scrapy.Request(self.urls.format(str(self.start_page)), callback=self.parse)
            time.sleep(2)

    @error_handler
    def get_date(self, response):
        date = response.xpath('/html/body/div[1]/meta[6]/@content').extract_first()
            #'//*[@id="middle_container"]/div[2]/div[1]/span[2]/a/text()').extract()[0]
        date = parse(date)
        return date

    def extract_data(self, response):
        url = get_base_url(response)
        date = self.get_date(response)
        content = get_content(
            response, path='//*[@id="forElectionID"]/p/text()')
        title = get_title(
            response, path='//*[@id="header-story"]/div[2]/h1/text()')
        author = get_author(
            response, path='//*[@id="middle_container"]/div[2]/div[2]/a/div/text()')
        tag = get_tag(response, '//*[@id="taglist"]/a/text()')
        tag = [t.replace('\n', '').replace("#", "") for t in tag]

        tab = CorpusItem()
        tab['content'] = content
        tab['title'] = title
        tab['author'] = author
        tab['tag'] = tag
        tab['date'] = date
        tab['url'] = url
        yield tab
