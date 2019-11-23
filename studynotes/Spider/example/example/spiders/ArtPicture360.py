# -*- coding: utf-8 -*-
# scrapy shell http://image.so.com/zj?ch=art&sn=30&listtype=new&temp=1 
# 	#找type=xhr的链接XmlHttpRequest
# 	#ch 表示分类,此处为art; sn 从第几张图片加载,即显示的第一张图片在服务器端的序号
# res = json.loads(response.body.encode('utf8'))



import scrapy
import json

class Artpicture360Spider(scrapy.Spider):
	name = 'ArtPicture360'
	allowed_domains = ['image.so.com']
	base_url = 'http://image.so.com/zj?ch=art&sn=%s&listtype=new&temp=1'
	start_urls = [base_url % 0] 
	start_index = 0 #计数器,从第一张图片开始请求
	max_download = 200 #设置最大下载量

	def parse(self, response):
		info = json.loads(response.body.decode('utf8'))
		yield {'image_urls':[url['qhimg_url'] for url in info['list']]} #image_urls关键字,此外可在items.py中定义字段

		self.start_index += info['count']
		if info['count']>0 and self.start_index<self.max_download:
			yield scrapy.Request(self.base_url % self.start_index)

