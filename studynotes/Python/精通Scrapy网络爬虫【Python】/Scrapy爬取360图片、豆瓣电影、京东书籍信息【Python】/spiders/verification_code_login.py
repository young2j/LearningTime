#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-29 00:33:53
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$  


import scrapy,pytesseract,json
from scrapy import FormRequest,Request
from PIL import Image
from io import BytesIO
from scrapy.log import logger

class VerificationCodeSpider(scrapy.Spider):
	name = 'VerificationCode'
	allowed_domains = ['']
	start_urls = ['']

	def parse(self,response):
		pass

	login_url = '登录页面链接'
	user = '用户名'
	password = '密码'
	def start_requests(self):
		yield Request(self.login_url,callback=self.parse_login,dont_filter=True)
	def parse_login(self,response):#此方法既要完成登录有下载验证码图片
		login_response = response.meta.get('login_response') 
		#若response.meta[login_response]存在,则当前为验证码图片响应,否则为登录页面响应
		if not login_response: #登录页响应,提取验证码图片的url
			VC_url = response.css('label.field.prepend-icon img::attr(src)').extract_first()
			VC_url = response.urljoin(VC_url)
			yield Request(VC_url,
						callback=self.parse_login,
						meta = {'login_response':response},
						dont_filter = True)
		else: #此时为验证码图片的响应
			fmdata = {
			'email':self.user,
			'password': self.password,
			'code':self.parse_VC_by_ocr(response.body) # response.body是图片的二进制数据
			}
			yield FormRequest.from_response(login_response,
											callback=self.parse_login_ed,
											formdata = fmdata,
											dont_filter = True)
	#**********************************tesseract-ocr识别*******************************
	def parse_VC_by_ocr(self,data):
		img = Image.open(BytesIO(data)) 
		#data指response.body是二进制数据,为了构造Image对象,需要传入类文件对象(BytesIO)
		img = img.convert(mode='L')
		imgtext = pytesseract.image_to_string(img)
		img.close()
		return imgtext
	#**********************************网络平台识别************************************
	def parse_VC_by_net(self,data):
		import requests,base64
		url = 'http://ali-checkcode.showapi.com/checkcode'
		appcode = 'f94u2k5h5249850298450' #平台发放的用于识别身份
		
		form ={}
		form['convert_to_jpg'] = '0' #不转换为jpg
		form['img_base64'] = base64.b64encode(data) #对图片进行base64编码
		form['typeId'] = '4070' #验证码类型,4070代表7位汉字

		headers = {'Athorization': 'APPCODE' + appcode}
		response = requests.post(url,headers=headers,data=form)
		res = response.json()

		if res['showapi_res_code'] == 0:
			return res['showapi_res_body']['Result']
		return ''
	#**********************************自己识别***************************************
	def parse_VC_by_myself(self,data):
		img = Image.open(BytesIO(data))
		img.show()
		imgtext = input('输入验证码:')
		img.close()
		return imgtext
	#--------------------------------------------------------------------------------
	def parse_login_ed(self,response):
		#需要判断是否登录成功,不成功则重新登录
		info = json.loads(response.text) #form请求的正文是json串,包含了用户验证的结果,转为python字典后根据error字段判断
		if info['error'] == '0':
			logger.info('登录成功：-)')
			return super().start_requests()
		else:
			logger.info('登录失败：-( 重新登录...')
			return self.start_requests()




























