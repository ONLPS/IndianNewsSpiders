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

class QuintSpider(CrawlSpider):
	name = "quint"
	urls = "https://www.thequint.com/news/politics/{}"
	start_page = 1
	start_urls = [urls.format(str(start_page))]

	def parse(self,response):

		all_links= response.xpath('.//div[@class="card-elements"]/a/@href').extract()
		for link in all_links:
			if "sunday" not in link:
				link = response.urljoin(link)
				yield scrapy.Request(link, callback=self.extract_data)

		if len(all_links) > 0 and self.start_page< 5:
			self.start_page += 1
			yield scrapy.Request(self.urls.format(str(self.start_page)), callback =self.parse)
			time.sleep(2)


	def get_date(self, response):
		date = response.xpath('.//meta[@itemprop="datePublished"]/@content').extract()
		date = parse(date[0])
		return date

	
	def extract_data(self, response):
		url = get_base_url(response)
		date = self.get_date(response)
		content = get_content(response, path = './/div[@class="story-article__content__element--text"]/p/text()')
		title = get_title(response, path ='/html/head/title/text()')
		author = get_author(response, path= './/span[@itemprop="author"]/a/text()')
		author += get_author(response, path = './/div[@class="story-article__author"]/a/text()')
		tag = get_tag(response, path='.//meta[@name="keywords"]/@content')
		tag = tag[0].split(',')

		tab = CorpusItem()
		tab['content'] = content
		tab['title'] = title
		tab['author'] = author
		tab['tag'] = tag
		tab['date'] = date
		tab['url'] = url
		yield tab
