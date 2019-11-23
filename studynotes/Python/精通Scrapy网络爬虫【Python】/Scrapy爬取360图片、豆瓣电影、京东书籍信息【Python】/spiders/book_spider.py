
import scrapy 
from scrapy import Item,Field
from scrapy.linkextractors import LinkExtractor

class BookItem(Item): #可将此自定义Item子类放于项目中自带的items.py里,然后import
	name = Field()
	price = Field()

class book_spider(scrapy.Spider):
	name = "books"
	# start_urls = ['http://books.toscrape.com/'] #使用基类Spider默认的start_requests方法
	def start_requests(self): #自定义请求,覆盖基类的start_requests方法
		yield scrapy.Request('http://books.toscrape.com/',
								callback=self.parse_book,
								headers={'User_Agent':'Mozilla/5.0'},
								dont_filter=True)
	# def parse(self,response):
	def parse_book(self,response):
		for sel in response.css('article.product_pod'):
			# name = sel.xpath('./h3/a/@title').extract_first()
			# price = sel.css('p.price_color::text').extract_first()
			# yield {
			# 	'name' : name,
			# 	'price': price,
			# }
			book = BookItem()
			book['name'] = sel.xpath('./h3/a/@title').extract_first()
			book['price'] = sel.css('p.price_color::text').extract_first()
			yield book 

		# next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
		# if next_url:
		#	 next_url = response.urljoin(next_url)
		links = LinkExtractor(restrict_css='ul.pager li.next').extract_links(response)
		if links:
			next_url = links[0].url #链接的第一个参数url,是一个绝对路径
			yield scrapy.Request(next_url,callback=self.parse_book)

#---------下面的代码放在settings.py中------
# ITEM_PIPELINES = {
# 	'example.pipelines.PriceConvertPipeline':300,
#	'example.pipelines.DuplicatesPipeline':350,
#	'example.pipelines.MongoDBPipeline':400
# }

#下面的代码放在pipelines.py中
#---------------汇率转换-----------------
# class PriceConvertPipeline(object):
# 	exchange_rate = 8.5309
# 	def process_item(self,item,spider):
# 		price = float(item['price'][1:])*self.exchange_rate
# 		item['price'] = '¥%.2f' % price 
# 		return item
#---------------数据去重-----------------
# from scrapy.exceptions import DropItem
# class DuplicatesPipeline(object):
# 	def _init_(self):
# 		self.book_set = set()
# 	def process_item(self,item,spider):
# 		name = item['name']
# 		if name in self.book_set:
# 			raise DropItem('Duplicate book found:%s' % item)
# 		self.book_set.add(name)
# 		return item
# ------------将数据存入MongoDB---------
# from scrapy.item import Item
# import pymongo

# class MongoDBPipeline(object):
# 	# DB_URI = 'mongodb://localhost:27017/' #数据库的URI地址
# 	# DB_NAME = 'scrapy_data' 				#数据库的名字
	
# 	@classmethod 
# 	'''
# 	@classmethod 修饰符对应的函数 类不需要实例化,不需要 self 参数,
# 	但第一个参数需要是表示自身类的 cls 参数,可以来调用类的属性,类的方法,实例化对象等
# 	'''
# 	def from_crawler(cls,crawler): 
# 		'''
# 		1.如果Item Pipeline中定义了from_crawler方法,Scrapy会调用该方法来创建类对象(即此处的MongDBPipeline)
# 		2.此处仅仅是改变了类属性的定义方法,还要在settings.py中进行设置:
# 		   MONGO_DB_URI = 'mongodb://192.168.1.105:27017/'
# 		   MONGO_DB_NAME = 'scrapy_data'
# 		'''
# 		cls.DB_URI = crawler.settings.get('MONGO_DB_URI','mongodb://localhost:27017/') 
# 		cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME','scrapy_data')
# 		#分别读取配置文件settings.py中的MONGO_DB_URI和MONGO_DB_NAME,并赋予cls的属性,即MongoDB类的属性
# 		return cls()

# 	def open_spider(self,spider): #spider打开时被调用---连接数据库
# 		self.client = pymongo.MongoClient(self.DB_URI) #通过URI地址连接数据库端
# 		self.db = self.client[self.DB_NAME] #创建一个名为scrapy_data的数据库

# 	def close_spider(self,spider): #spider关闭时被调用---关闭数据库
# 		self.client.close()

# 	def process_item(self,item,spider): #此步处理数据,实现数据在数据库中的写入操作
# 		collection = self.db[spider.name] #在scrapy_data数据库中创建一份名为爬虫名字books的数据集
# 		post = dict(item) if isinstance(item,Item) else item #生成字典对象
# 		collection.insert_one(post) #集合对象的insert_one方法需要传入字典对象,不能传入Item对象
# 		return item


