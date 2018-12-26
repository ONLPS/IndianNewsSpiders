import scrapy
import json
import re
import datetime
from ast import literal_eval

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import get_base_url

from tutorial.items import TutorialItem


class QuotesSpider(CrawlSpider):
    name = "the_wire"

    def start_requests(self):
        urls = [
            'https://thewire.in/politics/nda-seat-sharing-bihar-bjp-jdu-ljp'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def error_handling(func):
        def func_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                print(ex)
                return 'null'
        return func_wrapper

    @error_handling
    def get_title(self,response):
        title = response.xpath(".//div[1]/div/h1/span/text()").extract()
        return title[0]

    @error_handling
    def get_content(self,response):
        content = response.xpath(".//div[3]/div[2]/div[2]/p/text()").extract()
        content = " ".join(content)
        return content

    @error_handling
    def get_author(self, response):
        author = response.xpath("//div[3]/div[1]/div[1]/div/div[2]/a/text()").extract()
        author = ' '.join(author)
        return author

    @error_handling
    def get_publish_date(self,response):
        x = (response.xpath("/html/body/script[1]/text()").extract())[0]
        data =x[0:-1]
        data = data.replace('window.__data=','')
        data = json.loads(data)
        date = data['postDetails']['postDetails'][0]['post_date']

        return date

    @error_handling
    def get_comment(self,response):
        comment = response.xpath(".//nav/ul/li[1]/a/span[1]/text()").extract()
        return comment

    @error_handling
    def get_tag(self,response):
        tag = response.xpath(".//div[3]/div[2]/div[1]/div/span[1]/a/div/text()").extract()
        return tag

    @error_handling
    def get_share(self,response):
        share = response.xpath('.//*[@id="social_count_box"]').extract()
        return share



    def parse(self,response):
        print(get_base_url(response))
        url = get_base_url(response)
        polarity = "left"
        title = self.get_title(response)
        content = self.get_content(response)
        author = self.get_author(response)
        date = self.get_publish_date(response)
        comment = self.get_comment(response)
        tag = self.get_tag(response)
        share = self.get_share(response)

        tab = TutorialItem()

        tab['content'] = content
        tab['title'] = title
        tab['author'] = author
        tab['comment'] = comment
        tab['tag'] = tag
        tab['date'] = date
        tab['url'] = url
        tab['polarity'] = polarity
        tab['share'] = share
        yield tab

        







        