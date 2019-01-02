import scrapy
import json
import re
import datetime
import time
from ast import literal_eval

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import get_base_url

from ..items import CorpusItem
from ..utils import *

class ScrollSpider(CrawlSpider):
	name = "scroll"
	allow_domain=['scroll.in']

	urls = "https://scroll.in/category/76/politics/page/{}"
	start_page = 1
	start_urls = [urls.format(str(start_page))]
	
	def parse(self,response):
		all_links = response.xpath('//*[@id="feed"]/div/div[1]/ul/li/link/@href').extract()

		for link in all_links:
			if 'video' not in link:
				yield scrapy.Request(url=link, callback=self.extract_data)
				time.sleep(2)

		if len(all_links) > 0:
			self.start_page += 1
			yield scrapy.Request(self.urls.format(str(self.start_page)), callback =self.parse)
		

	def get_date(self, response):
		date = response.xpath('/html/head/meta[33]').extract()[0]
		start_index = date.find('t=')
		end_index = date.find('>')
		date = date[start_index+3:end_index-1]
		return date
	
	def extract_data(self, response):
		url = get_base_url(response)
		date = self.get_date(response)
		content = get_content(response, path = './/p/text()')
		content += get_content(response, path ='//*[@id="article-contents"]/ol/li/text()' )
		title = get_title(response, path ='.//header/h1/text()')
		author = get_author(response, path= './/div/aside[1]/address/a/text()')
		tag = get_tag(response, './/div/section/ul/li/a/text()')
		tag = [t.replace('\n','').strip() for t in tag]



		tab = CorpusItem()
		tab['content'] = content
		tab['title'] = title
		tab['author'] = author
		tab['tag'] = tag
		tab['date'] = date
		tab['url'] = url
		yield tab



		