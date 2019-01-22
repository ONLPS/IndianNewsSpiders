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


class ScrollSpider(CrawlSpider):
    name = "scroll"
    allow_domain = ['scroll.in']

    urls = "https://scroll.in/category/76/politics/page/{}"
    start_page = 1
    start_urls = [urls.format(str(start_page))]

    def parse(self, response):
        all_links = response.xpath(
            './/li[@class="row-story"]/link/@href').extract()

        for link in all_links:
            if 'video' not in link:
                yield scrapy.Request(url=link, callback=self.extract_data)

        if len(all_links) > 0 and self.start_page < 15:
            self.start_page += 1
            yield scrapy.Request(self.urls.format(str(self.start_page)), callback=self.parse)

    def get_date(self, response):
        date = response.xpath('.//meta[@name="dcterms.created"]/@content').extract()[0]
        date = parse(date)
        return date

    def extract_data(self, response):
        url = response._url
        date = self.get_date(response)
        content = get_content(response, path='.//div[@id="article-contents"]/p/text()')
        content += get_content(response, path='.//div[@id="article-contents"]/ol/li/text()')
        content += get_content(response, path = './/div[@itemprop="articleBody"]/p/text()')
        title = get_title(response, path='.//header/h1/text()')
        author = get_author(response, path='.//div/address/a/text()')
        tag = get_tag(response, './/a[@class="tag-menu"]/text()')
        tag = [t.replace('\n', '').strip() for t in tag]

        tab = CorpusItem()
        tab['content'] = content
        tab['title'] = title
        tab['author'] = author
        tab['tag'] = tag
        tab['date'] = date
        tab['url'] = url
        yield tab
