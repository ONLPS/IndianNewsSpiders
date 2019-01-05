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
	#allow_domain=['catchnews.com']
	urls = "https://www.thequint.com/news/politics/{}"
	start_page = 1
	start_urls = [urls.format(str(start_page))]

	def parse(self,response):

		all_links= response.xpath(".//div/div[3]/section/div/div/div/div/a/@href").extract()
		for link in all_links:
			if "sunday" not in link:
				link = response.urljoin(link)
				yield scrapy.Request(link, callback=self.extract_data)

		if len(all_links) > 0 and self.start_page< 200:
			self.start_page += 1
			yield scrapy.Request(self.urls.format(str(self.start_page)), callback =self.parse)
			time.sleep(2)


	def get_date(self, response):
		date = response.xpath('.//div/div[1]/div[2]/div[1]/meta[1]').extract()
		date += response.xpath('//*[@id="container"]/div/div[3]/div/section/section[2]/article[1]/meta[2]').extract()
		date = date[0]
		date = date.replace('<meta itemprop="datePublished" content="',"")
		date = date[:date.find('" data-reactid')].strip()
		date = parse(date.strip())
		return date

	def find_tag(self,response):
		tag = response.xpath('/html/head/meta[21]').extract()[0]
		tag = tag.replace('<meta content="','')
		tag = tag[:tag.find('name')-2].strip()
		tag = tag.split(',')
		return tag
	
	def extract_data(self, response):
		url = get_base_url(response)
		date = self.get_date(response)
		content = get_content(response, path = './/div/div/div/div/p/text()')
		title = get_title(response, path ='/html/head/title/text()')
		author = get_author(response, path= './/div/div[3]/div/div/section[2]/article[1]/div[4]/div[1]/div[2]/div[1]/div[2]/a/text()')
		author += get_author(response,path='.//div/div[3]/div/section/section[2]/article[1]/div[3]/div[1]/div[1]/div[2]/div[1]/span/a/text()')
		tag = self.find_tag(response)
	

						
		tab = CorpusItem()
		tab['content'] = content
		tab['title'] = title
		tab['author'] = author
		tab['tag'] = tag
		tab['date'] = date
		tab['url'] = url
		yield tab
