# -*- coding: utf-8 -*-

# Scrapy settings for example project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'example'

SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'example (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'example.middlewares.ExampleSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'example.middlewares.ExampleDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'example.pipelines.ExamplePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

ITEM_PIPELINES = {
	# 'scrapy.pipelines.files.FilesPipeline': 1 ,
	'example.pipelines.MyFilesPipeline': 1 ,
	'scrapy.pipelines.images.ImagesPipeline': 2 ,
	'example.pipelines.PriceConvertPipeline':300,
	'example.pipelines.DuplicatesPipeline':350,
	'example.pipelines.RankToNumber':400
	# 'example.pipelines.MongoDBPipeline':450
	# 'example.pipelines.SQLitePipeline':450
	# 'example.pipelines.MySQLPipeline':450
	# 'example.pipelines.RedisPipeline':450
}

FEED_EXPORTERS = {'excel':'example.my_exporter.ExcelItemExporter'}
FILES_STORE = "E:\\Sublime Text 3\\Files\\Spider\\example\\example\\spiders\\export_data"
IMAGES_STORE = "E:\\Sublime Text 3\\Files\\Spider\\example\\example\\spiders\\export_data"

# IMAGES_THUMBS = { #为图片生成缩略图
# 	'small': (50,50),
# 	'big': (270,270)
# }
# IMAGES_MIN_WIDTH = 110 #尺寸过滤
# IMAGES_MIN_HEIGHT = 110

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/65.0.3315.4 Safari/537.36'
DOWNLOADER_MIDDLEWARES = {
	'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
	'example.middlewares.BrowserCookiesMiddleware': 701,
	'scrapy_splash.SplashCookiesMiddleware': 723,
	'scrapy_splash.SplashMiddleware' :725,
	'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware':810,
	'example.middlewares.RandomHttpProxyMiddleware':745
	}

SPLASH_URL = 'http://localhost:8050' 
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
SPIDER_MIDDLEWARES = {
	'scrapy_splash.SplashDeduplicateArgsMiddleware':100
	}

HTTPPROXY_PROXY_LIST_FILE = 'proxy_list.json'

# DOWNLOAD_DELAY = 0.5 


# MONGO_DB_URI = 'mongodb://192.168.1.105:27017/'
# MONGO_DB_NAME = 'scrapy_data'

# SQLITE_DB_NAME = 'scrapy.db'

# MYSQL_DB_NAME = 'scrapy_db'
# MYSQL_HOST = 'localhost'
# MYSQL_USER = 'username'
# MYSQL_PASSWORD = 'passwd'

# REDIS_DB_INDEX = 0
# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379
