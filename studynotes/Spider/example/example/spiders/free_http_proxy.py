#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-30 10:48:45
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import scrapy,json
from scrapy import Request

class FreeProxy(scrapy.Spider):
	name = 'freeproxy'
	allowed_domains = ['www.xicidaili.com']

	def start_requests(self):
		#爬取前三页内容
		for i in range(0,4):
			yield Request('http://www.xicidaili.com/nn/%s' % i)

	def parse(self,response):
		for sel in response.xpath("//table[@id='ip_list']/tr[positon()>1]"):
			ip = sel.css('td:nth-child(2)::text').extract_first()
			port = sel.css('td:nth-child(3)::text').extract_first()
			scheme = sel.css('td:nth-child(6)::text').extract_first().lower()

			#使用爬取的代理发送请求
			url = '%s://httpbin.org/ip' % scheme
			proxy = '%s://%s:%s' % (scheme,ip,port)

			meta = {
			'proxy':proxy,
			'dont_retry': True,
			'download_timeout':10,
			'_proxy_scheme':scheme,
			'_proxy_ip':ip
			}
			yield Request(url,callback=self.check_available,meta= meta,dont_filter=True)

	def check_available(self,response):
		proxy_ip = response.meta['_proxy_ip_']

		#判断代理是否具有隐藏IP的功能
		if proxy_ip == json.loads(response.text)['origin']:
			yield {
			'proxy_scheme':response.meta['_proxy_scheme'],
			'proxy':response.meta['proxy']
			}







