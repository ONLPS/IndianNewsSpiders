from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import get_base_url

'''class someSpider(CrawlSpider):
  name = 'crawltest'
  start_urls = ['https://thewire.in/category/politics/all']

  rules = (Rule(LinkExtractor(allow=('category/politics/') ), callback='parse_obj', follow=True),)


  def parse_obj(self,response):
	for link in LinkExtractor(allow=('politics/'),).extract_links(response):
		print('print here ',link.url)


from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

class MySpider(CrawlSpider):
	name = "crawltest"
	#allowed_domains = ["sfbay.craigslist.org"]
	start_urls = ["https://thewire.in/category/politics/all"]

	rules = (
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@href="/#"]',)), callback="parse_items", follow= True),
	)

	def parse_items(self, response):
		print(get_base_url(response))'''


import scrapy
 
class MyntraSpider(scrapy.Spider):
	name = "crawltest"
	start_urls = [
		"https://thewire.in/category/politics/all",
	]
 
	def parse(self, response):
		x = get_base_url(response)
		hxs = scrapy.Selector(response)
		# extract all links from page
		all_links = hxs.xpath('//*[@id="category-container"]/div[2]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/a/@href').extract()
		for link in all_links:
			link= x+ link
			print('--------------------------------\n')
			print('link  is  ', link)
			yield scrapy.Request(url=link, callback=self.print_this_link)
 
	def print_this_link(self, response):
		pass