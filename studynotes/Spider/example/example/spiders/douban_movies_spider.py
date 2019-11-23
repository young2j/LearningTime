#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-30 19:07:59
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import scrapy,json,re
from scrapy import Request

class MoviesSpider(scrapy.Spider):
	BASE_URL = 'http://movie.douban.com/j/search_subjects\
				?type=movie$tag=%s&sort=recommend&page_limit=%s&page_start=%s'
	MOVIE_TAG = '豆瓣高分'
	PAGE_LIMIT = 20
	page_start = 0

	name = 'douban_movies'
	start_urls = [BASE_URL % (MOVIE_TAG,PAGE_LIMIT,page_start)]

	def parse(self,response):
		infos = json.loads(response.body.decode('utf8'))
		for movie_info in infos['subjects']:
			movie_item = {}
			movie_item['片名'] = movie_info['title']
			movie_item['评分'] = movie_info['rate']

			yield Request(movie_info['url'],callback=self.parse_movie,meta={'_movie_item':movie_item})

		if len(infos['subjects']) == self.PAGE_LIMIT:
			self.page_start += self.PAGE_LIMIT
			url = self.BASE_URL % (self.MOVIE_TAG,self.PAGE_LIMIT,self.page_start)
			yield Request(url)
	
	def parse_movie(self,response):
		movie_item = response.meta['_movie_item']
		info = response.css('div.subject div#info').xpath('string(.)').extract_first()
		fields = [s.strip().replace(':','') for s in \
					response.css('div#info span.pl::text').extract()]
		values = [re.sub('\s+','',s.strip()) for s in \
					re.split('\s*(?:%s):\s*' % '|'.join(fields),info)][1:]
		movie_item.update(dict(zip(fields,values)))

		yield movie_item




