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

class CatchSpider(CrawlSpider):
	name = "catch"
	#allow_domain=['catchnews.com']

	urls = "http://www.catchnews.com/politics-news/"
	start_page = 1
	start_urls = [urls.format(str(start_page))]
	
	def parse(self,response):
		all_links = response.xpath('.//div[1]/div/div[2]/div[1]/div[1]/ul/li/div/span[1]/a/@href').extract()
		all_links +=  response.xpath('.//div[1]/div/div[2]/div[1]/div[3]/ul/li/div/div[2]/span[1]/a/@href').extract()
		for link in all_links:
			yield scrapy.Request(url=link, callback=self.extract_data)
		time.sleep(2)
			
		
		next_page = response.xpath('.//div[1]/div/div[2]/div[2]/div/span[3]/a/@href').extract_first()
		if next_page is not None:
			print("\n-------------next page-----------\n",next_page)
			yield scrapy.Request(next_page, callback=self.parse)

	def get_date(self, response):
		date = response.xpath('.//div[1]/div[2]/div[1]/div[2]/span[2]/text()').extract_first()
		date = date.replace('| Updated on: ','')
		print(date.strip())
		date = parse(date.strip())
		return date
	
	def extract_data(self, response):
		url = get_base_url(response)
		date = self.get_date(response)
		content = get_content(response, path = './/div[1]/div[2]/div[1]/div[6]/span/div/p/text()')
		content +=get_content(response,path = './/div[1]/div[2]/div[1]/div[6]/span/p/text()')
		content += get_content(response,path = './/div[1]/div[2]/div[1]/div[6]/span/div[1]/p/span/text()')
		title = get_title(response, path ='/html/head/title/text()')
		author = get_author(response, path= './/div[1]/div[2]/div[1]/div[2]/span[1]/a/text()')
		tag = get_tag(response, './/div[1]/div[2]/div[3]/a/text()')
		tag =[_ for _ in [t.replace('\n','').strip() for t in tag] if _ not in ['',' ']]

						
		tab = CorpusItem()
		tab['content'] = content
		tab['title'] = title
		tab['author'] = author
		tab['tag'] = tag
		tab['date'] = date
		tab['url'] = url
		yield tab
