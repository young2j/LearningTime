#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-30 10:01:05
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest

lua_script = ''' 
function main(splash)
	splash:go(splash.args.url)
	splash:wait(2)
	splash:runjs("document.getElementsByClassName('page')[0].scrollIntoView(true)")
	splash:wait(2)
	return splash:html()
end
'''
#打开页面->等待渲染->执行js触发加载->等待渲染->返回html

class JDbookSpider(scrapy.Spider):
	name = 'jd_book'
	allowed_domains = ['search.jd.com']
	base_url = 'https://search.jd.com/Search?keyword=python&enc=utf-8&book=y&wq=python'

	def start_requests(self): #第一页无需渲染
		yield Request(self.base_url,callback=self.parse_urls,dont_filter=True)
	
	def parse_urls(self,response):
		#获取商品总数,计算出总页数
		total = int(response.css('span#J_resCount::text').extract_first())
		pageNum = total//60 +(1 if total % 60 else 0)
		#构造每页的url,向Splash的execute端点发送请求
		for i in range(pageNum):
			url = '%s&page=%s'%(self.base_url,2*i+1)
			yield SplashRequest(url,
							endpoint='execute',
							args={'lua_source':lua_script},
							cache_args=['lua_source'])
	
	def parse(self,response):
		for sel in response.css('url.gl-warp.clearfix>li.gl-item'):
			yield {
				'name':sel.css('div.p-name').xpath('string(.//em)').extract_first(),
				'price':sel.css('div.p-price i::text').extract_first()
			}
