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


class wireSpider(CrawlSpider):
	name = "thewire"
	urls ="https://thewire.in/wp-json/thewire/v2/posts/home/recent-stories?per_page=20&page={}"
	page_number = 1
	start_urls = [urls.format(page_number)]
	
	def url_gen(self, d):
		base_url="https://thewire.in/"
		post_name = d.get("post_name")
		category = d.get("prime_category")[0].get("slug")

		if category in ["goverment","law","rights","communalism"]:
			return base_url+category+"/"+post_name

	def parse(self, response):
		data = json.loads(response.body_as_unicode())
		all_links = [self.url_gen(d) for d in data if self.url_gen(d) is not None]
		
		for link in all_links:
			yield scrapy.Request(url=link, callback=self.extract_data)

		if self.page_number < 10:
			self.page_number += 1
			yield scrapy.Request(self.urls.format(self.page_number), callback = self.parse)
			
	@error_handler
	def get_publish_date(self,response):
		x = (response.xpath("/html/body/script[1]/text()").extract())[0]
		data =x[0:-1]
		data = data.replace('window.__data=','')
		data = json.loads(data)
		date = data['postDetails']['postDetails'][0]['post_date']
		date = parse(date)
		return date


	def extract_data(self,response):
		url = get_base_url(response)
		title = get_title(response,path='.//h1[@class="title"]/span/text()')
		content = get_content(response, path ='.//*[@class="col s12 m10 postComplete__description"]/p/text()')
		content += get_content(response, path ='.//*[@class="col s12 m10 postComplete__description"]/p/span/text()')
		author = get_author(response,path='.//*[@class="author__name"]/a/text()')
		date = self.get_publish_date(response)
		tag = get_tag(response,path='.//span[@class="data-tag"]/a/@title')
		
		tab = CorpusItem()

		tab['content'] = content
		tab['title'] = title
		tab['author'] = author
		tab['tag'] = tag
		tab['date'] = date
		tab['url'] = url
		yield tab