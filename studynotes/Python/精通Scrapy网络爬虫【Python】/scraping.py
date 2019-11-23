===============爬虫简介============
#了解目标站点: http://example.webscraping.com/
robots.txt:网站爬取限制
-------
section 1#禁止用户代理BadCrawler爬取网站 
User-agent:BadCrawler 
Disallow: /

section 2
User-agent: *
Crawl-delay: 5 #任和用户代理两次下载请求间5秒延迟
Disallow: /trap #封禁爬取了不允许链接的爬虫

section 3
Sitemap: http:/.../sitemap.xml #网站地图:提供了所有网页的链接,帮助爬虫定位网站最新内容
--------
#估算网站大小,利用Google搜索的site关键词过滤域名结果
site:example.webscraping.com
--------
#识别网站构建所使用的技术---builtwith模块
builtwith.parse("http://example.webscraping.com")
--------
#寻找网站所有者name_servers----python-whois模块
whois.whois("appspot.com")
--------
# 下载网页----urllib2模块

=========================scrapy=====================
# shell 命令：
scrapy startproject projectname
cd projectname #cd到爬虫项目文件夹下,快速生成一个爬虫标准模板:名为spidername,目标域名为domains
	->scrapy genspider spidername domains 
scrapy crawl -t excel -o 'path' --nolog
scrapy shell url -> view(response) ->fetch(url) ->view(response)

---scrapy.Request(url,...)
	callback='self.parse' #页面解析函数,默认Spider的parse方法
	dont_filter='False' #去重过滤器,避免重复下载,当页面内容随时间而变化时可设置为Ture
	method #请求方法,默认为'GET'
	headers #请求头,字典型
	body #请求的正文
	cookies #字典类型
	meta #字典类型,用于给其他组件传递信息
	encoding 
	priority=0 #请求的优先级

---Response基类:
 ->子类:	TextResponse
		HtmlResponse
		XmlResponse
# HtmlResponse的属性及方法：
	url/status/headers/encoding/request 
	body #响应正文,bytes类型
	text #响应正文,str类型
		 # response.text=response.body.decode(response.encoding)
	meta #response.request.meta
	selector #选择器
	xpath # response.selector.xpath的快捷方式
	css #response.selector.css的快捷方式
	urljoin(url) #用于构造绝对url

---Selector:
	from scrapy.selector import Selector
	from scrapy.http import HtmlResponse
	
	response = HtmlResponse(url='',body=body,encoding='utf-8') #此处body为一串html
	selector = Selector(response=response) #selector为选择器对象,代表选中了body这一串html
	->实际应用中不需要手动创建Selector对象,在第一次访问Response的selector属性时,
	  Response内部会自动创建Selector对象。即可直接写：
	  -response.selector

	--选中数据 #返回的是SelectorList对象,一堆html标签列表
	selector.xpath(query)
	selector.css(query)
	--提取数据
	selector.xpath.extract() #或者selector.css().extract(),下同
	selector.xpath.re()
	selector.xpath.extract_first() #SeletorList专有,即只提取选中数据的第一个
	selector.xpath.re_first() #SeletorList专有

---xpath:XML路径语言
	/  			#选中根节点
	.  			#当前节点
	..  		#上一个节点,即父节点
	element 	#子节点中的所有元素节点,如html、body、div、a
	//element   #后代节点中的所有元素节点
	*   		#元素的所有子节点
	text()  	#文本节点
	@attr  		#属性节点,如@class
	@*  		#所有属性节点
	[]  		#查找特定节点

	->结合常用函数示例
	response.xpath('//a[3]') #所有a标签中的第三个
	response.xpath('//a[last()]') #所有a标签中的最后一个
	response.xpath('//a[position()<=3]') #前三个a标签
	response.xpath('//div[@id]') #包含属性id的所有div标签
	response.xpath('//div[@id=images]') #包含属性id=images的所有div标签
	response.xpath('string(/body/a)') #选中a标签中的所有文本,连续的
		->response.xpath('/body/a//text()') #也能选中所有文本,但返回的是分开的文本
	response.xpath('//p[contains(@class,'small')]') #属性class包含small的p标签

---css:简单但功能不如xpath
	*					#所有元素
	E 					#E元素
	E1,E2 				#选中E1和E2元素
	E1 E2 				#选中E1的后代元素中的E2元素
	E1>E2 				#选中E1子元素中的E2元素
	E1+E2 				#选中E1和兄弟元素E2
	.CLASS 				#选中属性包含CLASS类的元素
	#ID 				#选中属性为ID的元素
	[attr] 				#选中包含attr属性的元素
	[attr='value'] 		#选中属性为value的元素
	[attr~='value'] 	#选中属性attr的值包含value的元素
	E:nth-child(n) 		#选中E元素,且该元素是其父元素的第n个子元素
	E:nth-last-child(n) #选中E元素,且该元素是其父元素的倒数第n个子元素
	E:first-child 		#选中E元素,且该元素是其父元素的第1个子元素
	E:last-child 		#选中E元素,且该元素是其父元素的倒数第1个子元素
	E:empty 			#选中没有子元素的E元素
	E::text 			#选中E元素的文本节点 
	E::attr()			#选中E元素的属性节点

	->示例
	response.css('[style]') 
	response.css('[id=images-1]') 
	response.css('div>a:nth-child(1)')
	response.css('div:nth-child(2)>a:nth-child(1)')
	response.css('div:first-child>a:last-child')

---使用 Item基类 和 Field类 封装数据：
	from scrapy import Item,Field
	#Field是Python字典的子类
	issubclass(Field,dict)
	
	#创建Item子类继承Item,并自定义字段
	class BookItem(Item):
		name = Field()
		price = Field(a=lambda x:x**2) #括号内为Field元数据,给其他组件传递一个处理信息的规则
	
	#对类进行实例化并给字段赋值
	book = BookItem(name='bookname',price=45)
	
	book.fields #可通过属性fields访问类的所有字段

		->对Item子类进行拓展:增加字段
		class ForeignBookItem(BookItem):
			translator = Field()

		->爬取到信息并不总是一个字符串,可能是字符串列表,此时可通过Field元数据
		  告诉CsvItemExporterd对字段进行'串行化:serializer',如:

		  author = Field(serializer=lambda x:'|'.join(x)) 
		  #元数据的键serializer是CsvItemExporter规定好的,用于获取串行化函数对象

---使用 Item Pipeline 处理数据：[示例见book_spider.py注释或pipelines.py]
# 创建一个Item Pipeline不需要继承特定基类,只需要定义处理方法：
	process_item(self,item,spider) #一个Item Pipeline 必须实现此方法,必不可少的
		->item #爬取的数据
		->spider #爬取此数据的Spider对象
		1.process_item处理后返回的数据会传递给下一级Item Pipeline继续处理
		2.如果process_item在处理数据时抛出DropItem异常,该item就会被抛弃,
		  通常在检测到无效数据或者主动想要过滤数据时,可以选择抛出DropItem异常

	open_spider(self,spider) #用于定义一个spider开启时需要做什么,比如连接数据库
	close_spidre(self,spider) #用于定义一个spider关闭时需要做什么,比如断开数据库
	from_crawler(cls,crawler) #用于在创建Item Pipeline时通过crawler.settings读取配置,即在settings.py中的配置信息
		->cls #Item Pipeline 的类对象,可以理解类本身self
		->crawler #Scrapy中的一个核心对象,用于访问配置

->注意：1.要启用定义的 Item Pipeline,需要在项目中的配置文件settings.py自行配置,例如

	ITEM_PIPELINES = {
	'example.pipelines.PriceConvertPipeline':300
	}
	#形式是 'projectname.pipelines.custom_item_pipeline':0~1000 ,数字决定处理的先后顺序,小的优先

	2.同时,自定义的Item Pipeline代码块需放在pipelines.py中

---使用LinkExtractor描述链接提取规则,再使用 extract_links(response)提取链接:
	LinkExtractor(...) #默认选中页面中所用链接
		allow = 're' #选中与re或者 re列表 匹配的绝对url
		deny = 're' #与allow相反,选中不与re或者 re列表 匹配的绝对url
		allow_domains=['baidu.com','github.com'] #选中指定域名或 域名列表里的链接
		deny_domains = [] #与allow_domains相反,选中指定域名之外的链接
		restrict_xpaths = [] #选中Xpath表达式或表达式列表选中的区域下的链接
		restrict_css = [] #选中CSS选择器或选择器列表选中区域下的所有链接
		tags = ['a','area'] #选中指定标签内的链接
		attrs = 'href' #选中指定属性内的链接
		process_value #接收一个形如process(value)的回调函数,对需要提取的链接进行处理
	    	->
	    	def process(value):
				m = re.search('javascript:go ToPage\('(.*?)'',value)
				if m:
					value = m.group(1) #返回括号组内容,group(0)是匹配到的整个字符串
				return value
			LinkExtractor(process_value=process)

---使用Exporter导出数据：负责数据导出的组件称为导出器Exporter
	基类
		BaseItemPipeline
	子类
		JOSON(JosonItemExporter)
		JOSON lines(JosonLinesItemExporter)
		CSV(CsvItemExporter)
		XML(XmlItemExporter)
		Pickle(PickleItemExporter)
		Marshal(MarshalItemExporter)
	
	--数据的导出可以使用命令行参数和在配置文件中自行配置
	#命令行参数：-t 指定文件格式 -o 指定输出路径 
	scrapy crawl spidername -t csv -o 'exportdata/%(name)s/%(time)s.data'		
	#配置文件:代码放在settings.py中,my_exporter.py在项目中新建
	FEED_URI = 'export_data/%(name)s.data' #路径
	FEED_FORMAT = 'csv' #格式
	FEED_EXPORT_ENCODING = 'gbk' #默认'utf-8'
	FEED_EXPORT_FIELDS = ['name','author','price']
	FEED_EXPORTERS = {'excel':projectname.my_exporter.ExcelItemExporter}

	->#自行创建ExcelItemExporter类,命名为my_exporter.py
	from scrapy.exporters import BaseItemExporter
	import xlwt
	class ExcelItemExporter(BaseItemExporter):
		def __init__(self,file,**kwargs):
			self._configure(kwargs)
			self.file = file
			self.wbook = xlwt.Workbook()
			self.wsheet = self.wbook.add_sheet('scrapy')
			self.row = 0
		def finish_exporting(self):
			self.wbook.save(self.file)
		def export_item(self,item):
			fields = self._get_serialized_fields(item)
			for col,v in enumerate(x for _,x in fields):
				self.wsheet.write(self.row,col,v)
			self.row += 1

---下载文件与图片： 
				FilesPipeline  							ImagesPipeline
导入路径 scrapy.pipelines.files.FilesPipeline	scrapy.pipelines.images.ImagesPipeline
Item字段 file_urls,files 							image_urls,images
下载目录  FILES_STORE								IMAGES_STORE

#在settings.py中启用FilesPipeline,通常将其置于其他Item Pipeline之前
ITEM_PIPELINES = {'scrapy.pipelines.files.FilesPipeline': 1}
FILES_STORE = "E:\\Sublime Text 3\\Files\\Spider\\example\\example\\spiders\\export_data"
->文件名存储为shal散列值,可在pipelines.py中实现FilesPipeline的子类,修改存储方式

#在settings.py中启用ImagesPipeline,以及其他可选项
ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 2}
IMAGES_STORE = "E:\\Sublime Text 3\\Files\\Spider\\example\\example\\spiders\\export_data"
IMAGES_THUMBS = { #为图片生成缩略图
	'small': (50,50),
	'big': (270,270)
}
IMAGES_MIN_WIDTH = 110 #尺寸过滤
IMAGES_MIN_HEIGHT = 110

---模拟登录-表单请求-post请求
#了解下form元素,掌握登录实质:
	'''当利用浏览器发起post请求时,浏览器利用响应头中的cookie信息(标识用户身份的session信息),同时
	读取响应头中的Location字段,依据其中描述的路径(/),再次发送一个GET请求。(登录时303页面重定向);
	GET请求中会携带POST请求获取的cookie信息,这一个工作由scrapy的下载中间件CookiesMiddleware自动完成'''
	<form>的method属性:决定了HTTP请求的方法,如post
	<form>的action属性:决定了HTTP请求的url,'action=#'代表当期页面url
	<form>的enctype属性:决定了表单数据的编码类型
	<form>的input属性:决定了表单数据的内容:
		->注意<div style='display:none;'>中还包含了隐藏的<input type='hidden'>,他们的值在value中,
			例如name=_next用来告诉服务器登录成功后页面跳转的地址;name=_formkey用来防止CSRF跨域攻击。
			<div style="display:none;">
				<input name="_next" type="hidden" value="/places/default/index">
				<input name="_formkey" type="hidden" value="97f8cb6c-bdd1-4a7c-b32d-26bd56cfa1b2">
				<input name="_formname" type="hidden" value="login">
			</div>
--FormRequest(formdata={}) #字典参数,Request的子类
	#直接构造FormRequest对象:
	>>>call('scrapy shell http://example.webscraping.com/places/default/user/login')
	>>>sel = response.xpath('//div[@style]/input') 
 	>>>fmdata = dict(zip(sel.xpath('./@name').extract(),sel.xpath('./@value').extract()))
 	>>>fmdata['email'] = '173371929@qq.com' #name='email'
 	>>>fmdata['password'] = 'jge520' #name=password
 	>>>request = FormRequest(url='http://example.webscraping.com/places/default/user/login',formdata=fmdata)
	#更为简单的方式:from_response方法:
	'''该方法会解析post请求的response中所包含的<form>元素信息,
	   并将隐藏的的<input>信息自动填入表单数据,此时只需构造用户名与密码即可'''
	>>>fmdata = {'email':'173371929@qq.com','password':'jge520'}	
	>>>	request = FormRequest.from_response(response,formdata=fmdata)
	>>>fetch(request)
	>>>"Welcome DoubleJ" in response.text >>>True #登录成功
->example:
	from scrapy.http import FormRequest,Request 
	class LoginSpider(scrapy.Spider):
		name = 'login'
		allowed_domains = ['example.webscraping.com']
		start_urls = ['http://example.webscraping.com/places/default/user/profile']

		def start_requests(self):
			yield Request(url='http://example.webscraping.com/places/default/user/login',
				callback = self.parse_post)
		def parse_post(self,response):
			fmdata = {'email':'173371929@qq.com','password':'jge520'}
			yield FormRequest.from_response(response,formdata=fmdata,callback=self.parse_star_urls)
		def parse_star_urls(self,response):
			if "Welcome DoubleJ" in response.text:
				yield from super().start_requests() #调用超类的start_requests()方法,即用start_urls发起请求并进行parse
		def parse(self,response):
			keys = response.css('table label::text').re('(.+):')
			values = response.css('table td.w2p_fw::text').extract()
			yield dict(zip(keys,values))

---识别验证码：通过pytesseract调用验证码识别库tesseract-ocr 		
	#下载windows版本tesseract-ocr https://github.com/UB-Mannheim/tesseract/wiki
	#pip install pytesseract
	#pip install Pillow/PIL
	from PIL import Image
	import pytesseract
	img = Image.open('imgpath.png') #打开图片
	img = img.convert(mode='L') # 转为黑白,提高识别成功率
	pytesseract.image_to_string(img) #识别

	->示例见verification_code_login.py

---Cookie 登录: 
	'''browsercookie库依赖于pycrypto库,pycrypto最多支持python3.3,因此需要分别进行安装:
	pip install pycryptodome
	python setup.py install
	一晚上才搞成功!!!'''
	chrome_cookiejar = browsercookie.chrome()
	firefox_cookiejar = browsercookie.firefox()
	for cookie in chrome_cookiejar: #可迭代对象,可访问其中的每个cookie对象
		print(cookie)

	--下载中间件CookiesMiddleware自动处理Cookie,但还不能使用浏览器的Cookie,
		利用browsercookie对CookiesMiddleware进行改良,实现一个能使用浏览器Cookie的中间件

	#下面的代码放在middlewares.py中
	import browsercookie
	from scrapy.downloadermiddlewares.cookies import CookiesMiddleware

	class BrowserCookiesMiddleware(CookiesMiddleware):
		def __init__(self,debug=False):
			super().__init__(debug)
			self.load_browser_cookies()
		def load_browser_cookies(self):
			#加载chrome浏览器中的Cookie
			jar = self.jars['chrome'] #self.jars是CookieJar字典
			chrome_cookiejar = browsercookie.chrome()
			for cookie in chrome_cookiejar:
				jar.set_cookie(cookie)

			#加载Firefox浏览器中的Cookie
			jar = self.jars['firefox']
			firefox_cookiejar = browsercookie.firefox()
			for cookie in firefox_cookiejar:
				jar.set_cookie(cookie)
	
	#同时在settings.py中启用BrowserCookiesMiddleware
	USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/65.0.3315.4 Safari/537.36'
	DOWNLOADER_MIDDLEWARES = {
	'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
	'example.middlewares.BrowserCookiesMiddleware': 701
	}

	#最终使用cookie登录时,只需在发起请求时使用元数据meta
	>>>scrapy shell
	>>>from scrapy import Request
	>>> url = 'https://passport.etest.net.cn/Manage/Index?see=1'
	>>> fetch(Request(url,meta={'cookiejar':'chrome'}))

---爬取动态页面：
'''javascript通过HTTP请求跟网站动态交互获取数据(AJAX),然后使用数据更新HTML页面,爬取动态页面
需要先执行页面中JavaScript渲染页面后再进行爬取'''
-->渲染引擎splash服务端点：
	
	#render.html端点
	请求地址: http://localhost:8050/render.html
	请求方式: GET/POST
	返回类型: html
	
	接受参数:
		url 		#必须的渲染页面url
		timeout 	#渲染超时时间
		proxy 		#代理服务器地址
		wait 		#等待渲染的时间
		images 		#是否下载图片,默认1为下载
		js_source 	#自定义的JavaScript代码,在页面渲染前执行
	>>> import requests
	>>> from scrapy.selector import Selector
	>>> splash_url = 'http://localhost:8050/render.html'
	>>>	args = {'url':'http://quotes.toscrape.com/js','timeout':5,'image':0}
	>>>	response = requests.get(splash_url,params = args)
	>>>	sel = Selector(response)
	>>> sel.css('div.quote span.text::text').extract()

	#execute 端点
	请求地址: http://localhost:8050/execute
	请求方式: POST
	返回类型: 自定义

	接收参数:
		lua_source  #必选自定义的lua脚本,用来模拟浏览器行为
		timeout 	#渲染超时时间
		proxy 		#代理服务器地址
	
	>>>import requests,json
	>>>lua_script = '''
		function main(splash)
			splash:go('http://example.com') #打开页面
			splash:wait(0.5)				#等待加载
			local title = splash:evaljs('document.title') #执行js获取结果
			return {title=title}  #返回json形式的结果
			end
			'''
	>>>splash_url = 'http://localhost:8050/execute'
	>>>headers = {'content-type':'application/json'}
	>>>data = json.dumps({'lua_source':lua_script})
	>>>response = requests.post(splash_url,headers=headers,data=data)
	>>>response.content
	>>>response.json()

	'''自定义的lua脚本必须包含一个main函数作为程序入口,main函数被调用时会传入一个splash对象,可以
	调用该对象上的方法操纵splash;
	splash根据main函数的返回值构造HTTP响应,main函数的返回值可以是字符串可以是lua中的表(类似字典)
	'''
	#splash常用属性和方法：
		splash.args #参数表,如splash.args.u
		splash:go #打开url并进行渲染
		splash:wait #等待渲染的时间
		splash:evaljs #执行一段js代码,并返回值
		splash:runjs #执行一段js代码,不返回值
		splash:url #提取当前页面url
		splash:url #提取当前页面html文本
		splash:js_enabled #开启/禁止js渲染,默认开启true
		splash.images_enabled #开启/禁止加载图片,默认true
		splash:get_cookies() #获取cookie信息

--->在scrapy中使用splash: pip install scrapy-splash

	#settings.py中
	SPLASH_URL = 'http://localhost:8050' #splash服务器地址
	
	#开启splash的两个下载中间件并调整HttpCompressionMiddleware的次序
	DOWNLOADER_MIDDLEWARES = {
	'scrapy_splash.SplashCookiesMiddleware': 723,
	'scrapy_splash.SplashMiddleware' :725,
	'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware':810
	}	

	#设置去重过滤器
	DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

	#用来支持cache_args(可选)
	SPIDER_MIDDLEWARES = {
	'scrapy_splash.SplashDeduplicateArgsMiddleware':100
	}

	->scrapy_splash中定义了一个SplashRequest类,只需使用scrapy_splash.SplashRequest
	替代scrapy.Request发起请求即可
	
	->SplashRequest常用参数:
		url/headers/cookies
		args #除url以外的参数,如wait,timeout,images,js_source
		cache_args #重复传递的参数可进行参数缓存,如cache_args=['js_source']
		endpoint #splash服务端点,默认为render.html,其他如execute/render.json/render.har/render.png等
		splash_url #Splash服务器地址,默认为None,即使用settings.py中的SPLASH_URL地址
->example:
	import scrapy
	from scrapy_splash import SplashRequest

	class QuotesSpider(scrapy.Spider):
		name = 'quotes'
		allow_domains = ['quotes.toscrape.com']
		start_urls = ['http://quotes.toscrape.com/js/']

		def start_requests(self):
			for url in self.start_urls:
				yield SplashRequest(url,args = {'images':0,'timeout':3})
		def parse(self,response):
			for sel in response.css('div.quote'):
				quote = sel.css('span.text::text').extract_first()
				author = sel.css('small.author::text').extract_first()
				yield {'quote':quote,'author':author}
			href = response.css('li.next>a::attr(href)').extract_first()
			if href:
				url = response.urljoin(href)
				yield SplashRequest(url,args={'images':0,'timeout':3})

----使用HTTP代理:信息中转站
	->下载中间件HttpProxyMiddleware默认启用,会在系统环境变量中搜索当前系统代理作为爬虫代理
	->在构造Request对象时通过meta参数的proxy字段手动设置代理:
		req = Request(url,meta={'proxy':'http://166.1.34.21:7117'})
	->如果代理需要身份验证：可按如下过程生成身份验证信息
		>>>from scrapy import Request
		>>>import base64
		>>> req = Request(url,meta={'proxy':'http://...'})
		>>>user = ''
		>>>passwd = ''
		>>>user_passwd = ('%s:%s'%(user,passwd)).encode('utf8')
		>>>req.headers['Proxy-Authorization'] = b'Basic' + base64.b64encode(user_passwd)
		>>>fetch(req)
	->获取免费代理free_http_proxy.py
	->实现随机代理middlewares.py:
	
	from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
	from collections import defaultdict
	import json,random

	class RandomHttpProxyMiddleware(HttpProxyMiddleware):
		def __init__(self,auth_encoding='latin-1',proxy_list_file=None):
			if not proxy_list_file:
				raise NotConfigured

			self.auth_encoding = auth_encoding
			self.proxies = defaultdict(list)

			with open(proxy_list_file) as f:
				proxy_list = json.load(f)
				for proxy in proxy_list:
					scheme = proxy['proxy_scheme']
					url = proxy['proxy']
					self.proxies[scheme].append(self._get_proxy(url, scheme))

		@classmethod
		def from_crawler(cls,crawler):
			auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING','latin-1')
			proxy_list_file = crawler.settings.get('HTTPPROXY_PROXY_LIST_FILE')
			return cls(auth_encoding,proxy_list_file)

		def __set__proxy(self,request,scheme):
			creds,proxy = random.choice(self.proxies[scheme])
			request.meta['proxy'] = proxy 
			if creds:
				request.headers['Proxy-Authorization'] = b'Basic' + creds

		->在settings.py中启用RandomHttpProxyMiddleware,并指定所要使用的代理服务器列表文件JSON
		DOWNLOADER_MIDDLEWARES = {
		#置于HttpProxyMiddleware(750)之前
		'example.middlewares.RandomHttpProxyMiddleware':745
		}
		#使用之前爬取的免费代理
		HTTPPROXY_PROXY_LIST_FILE = 'proxy_list.json'

----存入数据库:SQLite,MySQL,MongoDB,Redis
	#分别在pipelines.py和settings.py中实现
 
----分布式爬取:scrapy-redis
#redis的使用
sevice redis-server start
sevice redis-server restart
sevice redis-server stop

netstat -ntl
redis-cli -h 192.168.0.103

#redis基本命令
->字符串
SET key value
GET key
DEL key
->列表
LPUSH key value1 [value12] #插入值
RPUSH key value1 [value12]
LPOP key #弹出值
RPOP key 
LINDEX key index #获取列表key中index位置的值
LRANGE key start end 
LLEN key
->哈希
HSET key fied value #将哈希key的field字段赋值为value
HDEL key field1 [field2]
HGET key field 
HGETALL key
->集合
SADD key member1 [member2]
SREM key member1 [member2] #删除成员
SMEMBERS key #获取集合key中所有成员
SCARD key #获取成员数量
SISMEMBER key member #成员判断
->有序集合ZSet
ZADD key score1 member1 [score2 member2]
ZREM key member [member2] #删除成员
ZRANGE key start stop
ZRANGEBYSCORE key min max 

#使用scrapy-redis进行分布式爬取
->在settings.py中添加配置:
	REDIS_URL = 'redis://116.29.35.201:6379' #云服务器上的redis数据库
	SCHEDULER = 'scrapy_redis.scheduler.Scheduler' #使用scrapy_redis的调度器替代Scrapy的调度器
	DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter' #去重过滤器
	ITEM_PIPELINES = { #启用scrapy_redis的RedisPipeline将爬取到的数据汇总到Redis数据库
		'scrapy_redis.pipelines.RedisPipeline':300
	}
->可选项:
	SCHEDULER_PERSIST = True #爬虫停止后是保留/清理Redis中的请求队列以及去重集合,默认False

->将单机版本的Spider改为分布式,做如下改动:
	from scrapy_redis import RedisSpider
	
	# class BookSpider(scrapy.Spider):
	# 	...
	# 	start_urls = ['']
	class BookSpider(RedisSpider):
		...
		#请求队列在云服务器的redis数据库中以列表形式添加

->向各个主机分发任务:
	scp -r project_name username@ip：~/spider_file_name

->在任意主机上使用Redis客户端设置起始爬取点
	redis-cli -h 116.29.35.201
	lpush books:start_urls 'http://...' #<spider_name:start_urls>

->爬取完毕从Redis中取出:
	import redis
	import json

	ITEM_KEY = 'boos:items'

	def process_item(item):
		...

	def main():
		r = redis.StrictRedis(host='116.29.35.201',port=6379)
		for _ in range(r.llen(ITEM_KEY)):
			data = r.lpop(ITEM_KEY)
			item = json.loads(data.decode('utf8'))
			process_item(item)

if __name__ == '__main__':
	main()

		