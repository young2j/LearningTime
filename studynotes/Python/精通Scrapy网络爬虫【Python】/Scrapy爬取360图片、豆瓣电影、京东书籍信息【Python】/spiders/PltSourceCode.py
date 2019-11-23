# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import pltItem

class PltsourcecodeSpider(scrapy.Spider):
	name = 'PltSourceCode'
	allowed_domains = ['matplotlib.org']
	start_urls = ['http://matplotlib.org/examples/index.html']

	def parse(self, response):
		links = LinkExtractor(restrict_css='div.toctree-wrapper.compound li.toctree-l2',\
								deny='/index.html$').extract_links(response)
		for link in links:
			yield scrapy.Request(link.url,callback = self.parse_plt)
	def parse_plt(self,response):
		pltitem = pltItem()
		href = response.css('a.reference.external::attr(href)').extract_first()
		url = response.urljoin(href)
		pltitem['file_urls'] = [url] #注意此处必须转为list
		return pltitem 
