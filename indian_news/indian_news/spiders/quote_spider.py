import scrapy
import json
import re
import datetime
from ast import literal_eval

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import get_base_url

from indian_news.items import TutorialItem
from indian_news.utils import *

class QuotesSpider(CrawlSpider):
	name = "the_wire"

	start_urls = [
		"https://thewire.in/category/politics/all",
	]

	def parse(self, response):
		hxs = scrapy.Selector(response)
		# extract all links from page
		all_links = hxs.xpath('//*[@id="category-container"]/div[2]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/a/@href').extract()
		for link in all_links:
			link= 'https://thewire.in'+ link
			yield scrapy.Request(url=link, callback=self.extract_data)

	'''def error_handling(func):
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
		return share'''

	@error_handling
	def get_publish_date(self,response):
		x = (response.xpath("/html/body/script[1]/text()").extract())[0]
		data =x[0:-1]
		data = data.replace('window.__data=','')
		data = json.loads(data)
		date = data['postDetails']['postDetails'][0]['post_date']
		return date


	def extract_data(self,response):
		url = get_base_url(response)
		title = get_title(response,path=".//div[1]/div/h1/span/text()")
		content = get_content(response, path =".//div[3]/div[2]/div[2]/p/text()")
		author = get_author(response,path="//div[3]/div[1]/div[1]/div/div[2]/a/text()")
		date = get_publish_date(response,path="/html/body/script[1]/text()")
		comment = get_comment(response,path=".//nav/ul/li[1]/a/span[1]/text()")
		tag = get_tag(response,path=".//div[3]/div[2]/div[1]/div/span[1]/a/div/text()")
		share = get_share(response,path ='.//*[@id="social_count_box"]')

		tab = TutorialItem()

		tab['content'] = content
		tab['title'] = title
		tab['author'] = author
		tab['comment'] = comment
		tab['tag'] = tag
		tab['date'] = date
		tab['url'] = url
		tab['share'] = share
		yield tab

		







		