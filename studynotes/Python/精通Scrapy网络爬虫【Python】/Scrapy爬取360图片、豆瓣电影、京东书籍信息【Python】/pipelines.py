# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ExamplePipeline(object):
    def process_item(self, item, spider):
        return item

class PriceConvertPipeline(object):
	exchange_rate = 8.5309
	def process_item(self,item,spider):
		price = float(item['price'][1:])*self.exchange_rate
		item['price'] = '¥%.2f' % price 
		return item

from scrapy.exceptions import DropItem
class DuplicatesPipeline(object):
	def __init__(self):
		self.book_set = set() #定义一个空集合,用于放置爬取的数据进而判断是否有重复
	def process_item(self,item,spider):
		name = item['name']
		if name in self.book_set:
			raise DropItem('Duplicate book found:%s' % item) #有重复数据就删除,并抛出异常
		self.book_set.add(name)
		return item

class RankToNumber(object):
	rank_map = {
	'One' : 1,
	'Two': 2,
	'Three': 3,
	'Four': 4,
	'Five': 5 
	}
	def process_item(self,item,spider):
		rank_key = item['rank']
		if rank_key:
			item['rank'] = self.rank_map[rank_key]
		return item

from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename,dirname,join
class MyFilesPipeline(FilesPipeline):
	def file_path(self,request,response=None,info=None):
		path = urlparse(request.url).path
		return join(basename(dirname(path)),basename(path))


		
# -----------------------MongoDB--------------------
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
# 		#分别读取配置文件settings.py中的MONGO_DB_URI和MONGO_DB_NAME,并赋给cls的属性,即MongoDB类的属性
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


#------------------SQLite-----------------------
# import sqlite3
# class SQLitePipeline(object):
		
# 	def open_spider(self,spider):
# 		db_name = spider.settings.get('SQLITE_DB_NAME','scrapy_default.db')
# 		self.db_conn = sqlite3.connect(db_name)
# 		self.db_cur = self.db_conn.cursor()

# 	def close_spider(self,spider):
# 		self.db_conn.commit()
# 		self.db_conn.close()
		
# 	def process_item(self,item,spider):
# 		self.insert_db(item)
# 		return item

# 	def insert_db(self,item):
# 		values=(
# 			item['upc'],
# 			item['name'],
# 			item['price'],
# 			item['review_rating'],
# 			item['review_num'],
# 			item['stock']
# 			)
# 		sql = 'INSERT INTO books VALUES (?,?,?,?,?,?)'
# 		self.db_cur.execute(sql,values)

#---------------------MySQL-----------------------
'''Scrapy框架自身是使用Twisted框架编写的程序,Twisted是一个
事件驱动型异步网络框架,提供了异步方式多线程访问数据库的模块adbapi,
使用该模块可以显著提高程序访问数据库的效率'''
# from twisted.enterprise import adbapi

# class MySQLPipeline(object):
# 	def open_spider(self,spider):
# 		db = spider.settings.get('MYSQL_DB_NAME','scrapy_default')
# 		host = spider.settings.get('MYSQL_HOST','localhost')
# 		port = spider.settings.get('MYSQL_PORT',3306)
# 		user = spider.settings.get('MYSQL_USER','root')
# 		passwd = spider.settings.get('MYSQL_PASSWORD','root')

# 		self.dbpool = adbapi.ConnectionPool('MySQLdb',host=host,db=db,port=port,
# 											user=user,passwd=passwd,charset='utf8')
# 		#adbapi只是提供了异步访问数据库的框架,内部依然使用MySQLdb等库访问数据库,
# 		#连接池的第一个参数指定使用哪个库来访问数据库,其他参数在创建连接对象时使用

# 	def close_spider(self,spider):
# 		self.dbpool.close()

# 	def process_item(self,item,spider):
# 		self.dbpool.runInteraction(self.insert_db,item)
# 		return item

# 	def insert_db(self,tx,item): 
#		#参数tx是一个Transaction对象,与Cursor类似,可以调用execute执行SQL语句,
#		#insert_db执行完后会自动调用commit方法
# 		values=(
# 			item['upc'],
# 			item['name'],
# 			item['price'],
# 			item['review_rating'],
# 			item['review_num'],
# 			item['stock']
# 			)	
# 		sql = 'INSERT INTO books VALUES (?,?,?,?,?,?)'
# 		tx.execute(sql,values)

#---------------------Redis-----------------------
# import redis
# from scrapy import Item

# class RedisPipeline(object):
# 	def open_spider(self,spider):
# 		db_host = spider.settings.get('REDIS_HOST','localhost')
# 		db_port = spider.settings.get('REDIS_PORT',6379)
# 		db_index = spider.settings.get('REDIS_DB_INDEX',0)

# 		self.db_conn = redis.StrictRedis(host=db_host,port=db_port,db=db_index)
# 		self.item_i = 0
	
# 	def close_spider(self,spider):
# 		self.db_conn.connection_pool.disconnect()

# 	def process_item(self,item,spider):
# 		self.insert_db(item)

# 		return item

# 	def insert_db(self,item):
# 		if isinstance(item,Item):
# 			item = dict(item)

# 		self.item_i += 1
# 		self.db_conn.hmset('book:%s' % self.item_i,item)

