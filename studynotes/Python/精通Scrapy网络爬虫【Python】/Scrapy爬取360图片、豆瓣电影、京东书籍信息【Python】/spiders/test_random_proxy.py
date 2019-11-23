#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-30 18:51:37
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import scrapy,json
from scrapy import Request

class TestRandomProxySpider(scrapy.Spider):
	name = 'test_random_proxy'

	def start_requests(self):
		for _ in range(100): # 循环100次,但并不关心循环的变量,_代替
			yield Request('http://httpbin.org/ip',dont_filter=True)
			yield Request('https://httpbin.org/ip',dont_filter=True)

	def parse(self,response):
		print(json.loads(response.text))
		