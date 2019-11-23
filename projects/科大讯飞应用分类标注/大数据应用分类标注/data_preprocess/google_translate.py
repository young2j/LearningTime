from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from langdetect import detect
from numpy import ndarray
from pandas import Series

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=chrome_options)

# driver = webdriver.Chrome()
# driver.implicitly_wait(2)

def google_translate(text,driver=driver,from_lang='ja',to_lang='zh-CN'):
	AC =  ActionChains(driver)
	driver.get("https://translate.google.cn")
	try:
		# 选择输入语言
		more_langs_input_button = driver.find_element_by_xpath("//div[@class='sl-more tlid-open-source-language-list']")
		more_langs_input_button.click()

		# lang_button = driver.find_element_by_xpath("//div[@value='ja']")
		lang_input_button = driver.find_element_by_xpath("//div[@class='language_list_item_wrapper language_list_item_wrapper-{}']".format(from_lang))
		lang_input_button.click()

		# 选择输出语言
		more_langs_output_button = driver.find_element_by_xpath("//div[@class='tl-more tlid-open-target-language-list']")
		more_langs_output_button.click()

		lang_output_button = driver.find_element_by_xpath("//div[@class='language_list_item_wrapper language_list_item_wrapper-{}']".format(to_lang)) #含有不可见节点，click出错
		# lang_output_button.click()
		AC.click(lang_output_button).perform()

		# 输入文本
		input_text = driver.find_element_by_xpath("//div[@class='text-dummy']")
		# text = "「 话 せ な か っ た こ と 」"
		# input_text.send_keys(text)
		if isinstance(text,str):
			if detect(text)==from_lang:
				AC.send_keys_to_element(input_text,text).perform()
				# output_text = driver.find_element_by_xpath("//span[@class='tlid-translation translation']/span")
				output_text = WebDriverWait(driver, 10).until(
					EC.presence_of_element_located(
						(By.XPATH,"//span[@class='tlid-translation translation']/span")
						))
				res = output_text.text
			else:
				res = text # 这里可以进一步扩展，自动检测切换输入语言

		elif isinstance(text,(list,ndarray,Series)):
			res = []
			for txt in text:
				if detect(txt)==from_lang:
					AC.send_keys_to_element(input_text,txt).perform()
					# output_text = driver.find_element_by_xpath("//span[@class='tlid-translation translation']/span")
					output_text = WebDriverWait(driver, 30).until(
						EC.presence_of_element_located(
							(By.XPATH,"//span[@class='tlid-translation translation']/span")
						))
					res.append(output_text.text)
				else:
					res.append(txt)
		return res

	except Exception as e:
		raise e
	finally:
		driver.quit() #driver.close()

if __name__ == '__main__':
	text = input("待翻译语句:")
	from_lang = input("待翻译语言(ja,zh-CN,en,de,...):")
	to_lang = input("需要翻译为(ja,zh-CN,en,de,...):")
	
	if from_lang=='':
		from_lang = 'ja'

	if to_lang=='':
		to_lang = 'zh-CN'
	res = google_translate(text,from_lang=from_lang,to_lang=to_lang)
	print(res)