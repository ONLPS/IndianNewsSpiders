# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
	# define the fields for your item here like:
	content = scrapy.Field()
	title = scrapy.Field()
	author = scrapy.Field()
	comment = scrapy.Field()
	tag = scrapy.Field()
	date = scrapy.Field()
	url = scrapy.Field()
	polarity = scrapy.Field()
	share = scrapy.Field()



