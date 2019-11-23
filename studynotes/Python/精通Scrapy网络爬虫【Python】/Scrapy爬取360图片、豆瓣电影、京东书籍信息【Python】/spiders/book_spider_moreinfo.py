# from scrapy import Item,Field
from scrapy.linkextractors import LinkExtractor
import scrapy
from ..items import book_info

#---字段定义放在了items.py中---
# class book_info(Item):
# 	name = Field()
# 	price = Field()
# 	rank = Field()
# 	ISBN = Field()
# 	stockamount = Field()
# 	reviewamount = Field() 

class bookspider_moreinfo(scrapy.Spider):
	name = 'books_moreinfo'
	def start_requests(self):
		yield scrapy.Request(url='http://books.toscrape.com/',
								callback=self.parse_book,
								dont_filter = True)
	def parse_book(self,response):
		#提取页面所有书籍链接
		links = LinkExtractor(restrict_css='div.image_container',tags='a',attrs='href').extract_links(response)
		for link in links :
			next_url = link.url 
			yield scrapy.Request(next_url,callback=self.parse_book_moreinfo)
		#提取下一页链接
		links = LinkExtractor(restrict_css='ul.pager li.next').extract_links(response)
		if links:
			next_url = links[0].url
			yield scrapy.Request(next_url,callback=self.parse_book)
	def parse_book_moreinfo(self,response):
		books = book_info()
		books['name'] =  response.css('div.product_main>h1::text').extract_first()
		books['price'] = response.css('div.product_main p.price_color::text').extract_first()
		books['stockamount'] = response.xpath('//p[@class="instock availability"]/text()')[1].re_first('In stock \((\d+) available\)')
		books['rank'] = response.css('div.product_main p.star-rating::attr(class)').re_first('star-rating ([A-Za-z]+)')
		books['ISBN'] = response.css('table tr:first_child>td::text').extract_first()
		books['reviewamount'] = response.css('table>tr:last_child td::text').extract_first()
		yield books 

		