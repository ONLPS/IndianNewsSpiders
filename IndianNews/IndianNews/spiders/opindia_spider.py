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

class OpindiaSpider(CrawlSpider):
	name = "opindia"
	#allow_domain=['catchnews.com']
	urls = "https://www.opindia.com/category/politics/"
	pages = 0
	start_urls = [urls]

	def parse(self,response):
		all_links = response.xpath('.//div[3]/div/div/div[1]/div/div/div[2]/h3/a/@href').extract()
		for link in all_links:
			yield scrapy.Request(link, callback= self.extract_data)

		next_page_link = response.xpath('.//*[@class="page-nav td-pb-padding-side"]/a/@href')[-1].extract()
		if next_page_link is not None and self.pages < 10:
			self.pages+=1
			yield scrapy.Request(next_page_link, callback =self.parse)
	


	def get_date(self, response):
		date = response.xpath('.//*[@class="entry-date updated td-module-date"]/@datetime')[0].extract()
		date = parse(date)
		return date

	def get_content(self,response):
		content = response.xpath('.//*[@class="tdb-block-inner td-fix-index"]/p')
		content_list = []
		for tp in content:
			content = tp.xpath("text()").extract()
			a_tag = tp.xpath("a/text()").extract()
			if len(a_tag) > 0:
				a_tag.append('')
				content = [ c+a for c,a in zip(content,a_tag)]
				content = [' '.join(content)]
			if len(content) > 0:
				content_list.append(content[0])
		return ' '.join(content_list)


	
	def extract_data(self, response):
		url = "https://www.opindia.com/"
		date = self.get_date(response)
		content = self.get_content(response)
		title = get_title(response, path ='.//div/div/div/div[2]/div/h1/text()')
		author = get_author(response, path= './/*[@class="tdb-author-name"]/text()')
		tag = get_tag(response,path = './/*[@class="tdb-tags"]/li/a/text()')

		tab = CorpusItem()
		tab['content'] = content
		tab['title'] = title
		tab['author'] = author
		tab['tag'] = tag
		tab['date'] = date
		tab['url'] = url
		yield tab



