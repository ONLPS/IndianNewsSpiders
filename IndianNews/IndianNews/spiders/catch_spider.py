import scrapy
import time
from dateutil.parser import parse
from scrapy.spiders import CrawlSpider
from ..items import CorpusItem
from ..utils import *


class CatchSpider(CrawlSpider):
    name = "catch"
    urls = "http://www.catchnews.com/politics-news/"
    start_page = 1
    start_urls = [urls.format(str(start_page))]

    def parse(self, response):

        all_links = response.xpath(
            './/*[@class="category_div"]/ul/li/div/a/@href').extract()
        all_links += response.xpath(
            './/*[@class="cate_div2"]/ul/li/div/div/a[1]/@href').extract()

        for link in all_links:
            yield scrapy.Request(url=link, callback=self.extract_data)
        time.sleep(2)

        next_page = response.xpath(
            './/*[@class="nextAbled"]/a/@href').extract_first()

        if next_page is not None and self.start_page < 220:
            self.start_page += 1
            yield scrapy.Request(next_page, callback=self.parse)
            time.sleep(2)

    def get_date(self, response):

        date = response.xpath(
            './/div[1]/div[2]/div[1]/div[2]/span[2]/text()').extract_first()

        date = date.replace('| Updated on: ', '')
        date = parse(date.strip())

        return date

    def extract_data(self, response):
        url = response._url
        date = self.get_date(response)
        content = get_content(
            response, path='.//*[@class="quick_pill_news_description"]/p/text()')
        content += get_content(response,
                               path='.//*[@class="start-text dropCap fontAdelle"]/p/text()')
        content += get_content(response,
                               path='.//*[@class="start-text dropCap fontAdelle"]/p/span/text()')
        title = get_title(response, path='/html/head/title/text()')
        author = get_author(
            response, path='.//*[@class="artical_news_name textuc"]/a/text()')
        tag = get_tag(
            response, './/*[@class="ins_keyword margin_top40"]/a/text()')
        tag = [_ for _ in [t.replace('\n', '').strip()
                           for t in tag] if _ not in ['', ' ']]

        tab = CorpusItem()
        tab['content'] = content
        tab['title'] = title
        tab['author'] = author
        tab['tag'] = tag
        tab['date'] = date
        tab['url'] = url
        yield tab
