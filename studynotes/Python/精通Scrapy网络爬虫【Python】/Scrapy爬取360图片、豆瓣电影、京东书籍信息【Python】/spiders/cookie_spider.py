# -*- coding: utf-8 -*-

import scrapy 

class CookieSpider(scrapy.Spider):
	name = 'cookie'
	url = 'https://passport.etest.net.cn/Manage/Index?see=1'

	def start_requests(self):
		yield scrapy.Request(self.url,meta={'cookiejar':'chrome'})
	def parse(self,response):
		myname = response.css('div.input_sub1::text').extract()
		yield myname 

#。。。。。。。。。实践失败。。。。。。。。。。。
