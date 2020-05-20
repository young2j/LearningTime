#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-08
# @Author  : ${author} (${email})
# @Link    : ${link}
# @Version : $Id$
计算机管理 compmgmt.msc 
计算机服务 services.msc
管理员启动命令行 runas /user:administrator cmd
设置任务计划模块自动运行 sc config schedule start= auto
启动任务计划程序 taskschd.msc /s

pip install -U pip
pip list --oudated
pip search libname
pip install pkg -i https://pypi.tuna.tsinghua.edu.cn/simple/
=====================================================
pyinstaller -F/-D myfile.py #形成一个exe还是形成很多依赖文件，后者兼容性更好
            -i myicon.ico -p packagepath 
            -w/-c  # window/console 
            -n #为生成的exe起个名字
            --key  # 加密打包
pyi-makespec -F myfile.py # 生成spec文件
'''
RecursionError: maximum recursion depth exceeded
打开 myfile.spec 添加
import sys
sys.setrecursionlimit(1000000)
再次执行 pyinstaller -F myfile.spec -i myicon.ico
'''
# setup.py

# cython: language_level=3
from distutils.core import setup
from Cython.Build import cythonize
setup(
	name='reconciliation',
	ext_modules = cythonize('main.py')
	)

$ python setup.py build_ext --inplace
=====================================================

# 列出
conda env list 
# 创建
conda create -n your_env_name python=X.X #（2.7,3.6)
# 激活
Linux:  source activate your_env_name(虚拟环境名称)
Windows: activate your_env_name(虚拟环境名称)
# 安装包
conda install -n your_env_name packagename

# 关闭
Linux: source deactivate
Windows: deactivate

# 删除
conda remove -n your_env_name --all


#---env----

python3 -m venv tutorial-env

#在Windows上，运行:
tutorial-env\Scripts\activate.bat
#在Unix或MacOS上，运行:
source tutorial-env/bin/activate

#退出
deactivate
========================================================
import pip 
from subprocess import call
for dist in pip.get_installed_distributions():
	call("pip install -U " + dist.project_name,shell=True)

conda:
添加清华源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
更新所有包
conda update --all

jupyter config:
	jupyter notebook --generate-config
	
	pip install jupyter_contrib_nbextensions
	jupyter contrib nbextension install --user
	pip install jupyterthemes  
	jt -t monokai -fs 12 -T -N -tf ubuntu -tfs -10 -dfs 8 -ofs 10 -cellw 80% -lineh 130 -cursw 3
=======================遍历循环===================================

tups = {"name": "mengmeng", "looks": "beautiful", "age": 24}
for a, b in tups.items():
    print("%s:%s" % (a, b))
student = ["xiaomeng", "xiaozhi", "xiaoqiang"]
number = ["1002", "1003", "1004"]
for i in range(len(student)):
    print(student[i], "的学号是： ", number[i])
for a, b in zip(student, number):
    print(a, "的学号是： ", b)

========================函数========================================
# 定义阶乘函数-------------------------------------------------

def fact_iter(x, y):
	if x == 1:
		return y
	return fact_iter(x - 1, x * y)


def fact(n):
	return fact_iter(n, 1)

# 匿名函数------------------------------------------------------
c = lambda x, y=10: y**x
print([i for i in filter(lambda x: x > 3, [1, 2, 3, 4, 5])])

========================类======================================

class Student(object):
	def __init__(self, name, score):  # 类中的构造方法__init__(初始化)
		self.__name = name  # 类的属性（私有变量）
		self.__score = score  # 类的属性（私有变量）

	def info(self):  # 类中的非构造方法
		print("学生:%s;分数:%s" % (self.__name, self.__score))
	def get_score(self): #定义方法：可以外部访问私有变量
		return self.__score
	def modify_score(self,score): #定义方法：可以外部修改私有变量
		if score in range(0,100): #为什么还是能改成105也不提示？？？
			self.__score = score
		else:
			print("分数应该是0到100的数字")
stu = Student("小萌",95) #类的实例化
stu.info() #通过实例变量引用类中方法info()
print(stu.get_score()) #通过定义的方法访问私有变量
stu.modify_score(59) #通过定义的方法修改私有变量
print(stu.get_score())

# 多重继承----------------------------------------------------
class Animal(object):
	pass
class Mammal(Animal):
	pass
class Bird(Animal):
	pass
class Dog(Mammal):
	pass
class Bat(Mammal):
	pass
class Parrot(Bird):
	pass
class Ostrich(Bird):
    pass
class Runnable(object):
	def run(self):
			print("running")
class Flyable(object):
	def fly(self):
			print("flying")	
class Dog(Mammal,Runnable):
	pass
class Bat(Mammal,Flyable):
	pass

class type_dect(object):
	def __str__(self):
		return "地上跑的动物"
	__repr__=__str__


========================异常======================================
#try/except/else/finally的组合使用
def  a_divid_b(a,b):
	try:
		c = a/b
	except (ZeroDivisionError,SyntaxError,NameError) as e:
		raise
		print (e)
	else:
		return c
	finally: #不是说finally子句最后执行吗？结果好像不是？？
		print("this is a error capture programming")
a_divid_b(2, 1)
a_divid_b(2, 0)
======================时间和日期====================================
%a  简化星期名称         				 %m  月份
%A  完整星期名称          			 %M  分钟
%b  简化月份名称         				 %S  秒数
%B  完整月份名称         				 %y  去掉世纪的年份
%d  一个月中的天数       				 %Y  完整年份
%H  一天中的小时数					 %F  %Y-%m-%d的简写形式
%w  一星期中的第几天（0是星期天）		 %D  %m-%d-%y的简写形式
%W  一星期中的第几天（0是星期一）

import time,datetime,calendar
# 对象为时间戳--------
time.time() #时间戳
time.localtime() #本地时间
time.gmtime() #0时区时间(UTC)
time.ctime() #将时间戳转化为'Sat Dec  9 22:00:12 2017'

# 对象为时间元组struct_time--------
t = time.localtime() #本地时间形成的元组
time.mktime(t)#转化为时间戳
time.asctime(t) #'Sat Dec 9 22:00:12 2017'
time.strftime("%Y-%m-%d", t) #返回以字符串表示的时间strftime(format,tuple)
time.strptime("Sat Dec 9 22:00:12 2017", "%a %b %d %H:%M:%S %Y") #将字符串时间转化为时间元组

# 功能型时间函数
clock()#返回进程时间
time.sleep()#延迟时间

#datetime模块----------------
datetime.datetime.today()
datetime.datetime.now(tz)
datetime.timedelta(hours=3)#默认3天
# ......
dt=datetime.datetime.now()
dt.strftime("%Y-%m-%d %H:%M:%S")

#regex--------------
import re
re.match("hello", "hello world").span()

========================文件操作======================================
# 打开文件--
open("path","w+","buffering",encoding="utf-8")
# 读取文件--
open().read("byte")
open().readline(" ")
open().readlines(list) #读取对象为列表
# 写入文件--
open().write("byte")
open().writeline(" ")
open().writelines(list) #写入对象为列表
# 关闭文件--
open().close()

with open() as f:
	open().write(" ") #with自动调用close(),替代try/finally复杂命令
#文件重命名和删除--
os.rename(old,new)
os.remove(" ")

#文件内容迭代----
file = open("path")
while True:
	txt = file.read(1) #按字节迭代，txt = file.readline(1)->按行迭代
	if not txt:
		break
	print(txt)
file.close()
#懒加载式迭代-for循环----
import fileinput
for line in fileinput.input(path):
	print (line)
#StringIO()函数----
from io import StringIO
io_str = StringIO("Hello\nWorld\nWelcome")
while True:
	line = io_str.readline()
	if line =="":
		break
	print(line.strip())

StringIO().write("")
StringIO().readline()
StringIO().getvalue()

===================序列化与反序列化====================================

------python独有---------------
import pickle
# 内存->文件:pickle.dump()/pickle.dumps()-后者先读取为bytes.
dic =dict(name="萌萌",num=6017)
pickle.dumps(dic) #将数据通过特殊的形式转化为只有python语言认识的字符串
pickle.dump(dic) #将数据通过特殊的形式转化为只有python语言认识的字符串，并写入文件
try:
	file1 = open("./Files/Pyfiles/dump.txt","wb")
	pickle.dump(dic,file1)
finally:
	file1.close()
# 文件->内存:pickle.load()/pickle.loads()-后者先读取为bytes.
try:
	file1 = open("./Files/Pyfiles/dump.txt","rb")
	pickle.load(file1)
finally:
	file1.close()
------通用JSON序列化--------------
#处理的是字符串--
json.dumps()--序列化(编码) #将数据通过特殊的形式转化为所有程序语言都认识的字符串
json.loads()--反序列化(解码)
# 处理的是文件--
json.dump() #将数据通过特殊的形式转化为所有程序语言都认识的字符串，并写入文件
json.load()

import json
dic =dict(name="萌萌",num=6017)
json_dstr=json.dumps(dic)
print(json_dstr)
json_lstr=json.loads(json_dstr)
print(json_lstr)

repr() # 接收任何对象返回字符串的表达形式

=======================字符串操作===============================
all([1,-5,3])#判断列表或元组所有元素非零返回Ture
any([]) #只要有一个元素非零，则返回Ture，全部为零返回False
------
name = "my \tname is {name} and i am {year} old"
name.capitalize() #大写
name.count("a") #计数
name.center(50,"-") #字符串居中，总长度50，不足处以-代替
name.ljust(50,'*')  #字符串居左，总长度50，不足处以*代替
name.rjust(50,'-')  #字符串居右，总长度50，不足处以-代替
name.endswith("ex") #以ex结尾
name.expandtabs(tabsize=30)#以tab隔开，tab长度为30
name.find("name") #查找name所在位置
name.format(name='alex',year=23) 
name.format_map({'name':'alex','year':12}) 
-------
'ab23'.isalnum() #判断是否字母和数字
'abA'.isalpha() #判断是否是字母
'1A'.isdigit() #判断是否是数字
'My Name Is '.istitle() #判断是否首字母均大写(标题)
'My Name Is '.isupper() #判断是否大写
'+'.join( ['1','2','3'])  #以+进行连接
'Alex'.lower() #小写 
'Alex'.upper() #大写
'    Alex\n'.strip() #去除空白
'\nAlex'.lstrip()  #去除左空白
'Alex\n'.rstrip()  #去除右空白
-------
p = str.maketrans("abcdefli",'123$@456') #生成对应规则
"alex li".translate(p) #按照对应规则翻译
-------
'alex li'.replace('l','L',1) #字符替换
'alex lil'.rfind('l') #从右开始查找位置
'1+2+3+4'.split('+') #按+分割，返回列表
'1+2\n+3+4'.splitlines() #按行分割
'Alex Li'.swapcase() #大小写互相转换
'lex li'.title() #首字母大写
'lex li'.zfill(50) #长度50，不足处以zero代替？ 
'1A'.isdecimal()
'a 1A'.isidentifier()#判读是不是一个合法的标识符
'33A'.isnumeric() #判断是否是整数？

=======================集合操作=======================================
list_1 = [1,4,5,7,3,6,7,9]
set_1 = set(list_1)
set_2 =set([2,6,0,66,22,8,4])
print(set_1,set_2)
---交集---
print(set_1.intersection(set_2))
print(set_1 & set_2)
---并集---
print(set_1.union(set_2))
print(set_2 | set_1)
---差集---
print(set_1.difference(set_2)) #在集合1中而不在集合2中
print(set_2.difference(set_1)) #在集合2中而不在集合1中
print(set_1 - set_2)
---子集---
set_3 = set([1,3,7])
print(set_3.issubset(set_1)) #判断集合3是否是集合1的子集
print(set_1.issuperset(set_3)) #判断集合1是否是集合3的子集

---对称差集---
print(set_1.symmetric_difference(set_2)) #去掉共同元素，返回一个互异元素集合
print(set_1 ^ set_2)

---交集判断---
set_4 = set([5,6,7,8])
print(set_3.isdisjoint(set_4)) #判断集合3与集合4是否有交集，无交集返回Ture

---增加集合元素---
set_1.add(999)
set_1.update([888,777,555])
print(set_1)

---删除集合元素---
set_1.pop() #出栈，即去掉末尾元素
set_1.discard(888) 

============================内置模块====================================
---------re---------
#基本语法
'.'     #默认匹配除\n之外的任意一个字符，若指定flag DOTALL,则匹配任意字符，包括换行
'^'     #匹配字符开头，若指定flags MULTILINE,这种也可以匹配上(r"^a","\nabc\neee",flags=re.MULTILINE)
'$'     #匹配字符结尾，或re.search("foo$","bfoo\nsdfsf",flags=re.MULTILINE).group()也可以
'*'     #匹配*号前的字符0次或多次，re.findall("ab*","cabb3abcbbac")  结果为['abb', 'ab', 'a']
'+'     #匹配前一个字符1次或多次，re.findall("ab+","ab+cd+abb+bba") 结果['ab', 'abb']
'?'     #匹配前一个字符1次或0次
'{m}'   #匹配前一个字符m次
'{n,m}' #匹配前一个字符n到m次，re.findall("ab{1,3}","abb abc abbcbbb") 结果'abb', 'ab', 'abb']
'|'     #匹配|左或|右的字符，re.search("abc|ABC","ABCBabcCD").group() 结果'ABC'
'[...]'	#用来表示一组字符,如[abc]用来匹配a,b或者c
'[^...]'#不在[]中的字符：[^abc] 匹配除了a,b,c之外的字符。

'(?iLmsux[:re])' #指定编译选项,可添加-号表示关闭如(?-i)。
			#但注意选项的有效范围是整条规则，即写在规则的任何地方，选项都会对全部整条正则式有效。
			# i = IGNORECASE ; 
			# L = LOCAL ;
			# m = MULTILINE ;
			# s = DOTALL ;
			# u = UNICODE ;
			# x = VERBOSE 。
'(?# )' #注释。(?# )之间的内容将被忽略。

'(?<=…)' #前向界定,后向搜索 注：不可以在前向界定的括号里写正则式
		 #括号中 … 代表希望匹配的字符串的前面应该出现的字符串。
'(?=…)'  #后向界定,前向搜索 注：可以在后向界定写正则式
		 #括号中的 …代表希望匹配的字符串后面应该出现的字符串。

'(?<!...)' # 前向非界定
		   # 当希望的字符串前面不是'…'的内容时才匹配
'(?!...)' #后向非界定
		  #当希望的字符串后面不跟着…内容时才匹配。

'*?' '+?' '??' #加?表示最小匹配，即懒惰

'\A'    #只从字符开头匹配，re.search("\Aabc","alexabc") 是匹配不到的
'\Z'    #匹配字符结尾，同$
'\d'    #匹配数字0-9
'\D'    #匹配非数字
'\w'    #匹配[A-Za-z0-9]
'\W'    #匹配非[A-Za-z0-9]
'\s'    #匹配空白字符、\t、\n、\r , re.search("\s+","ab\tc1\n3").group() 结果 't'
'\S'	#匹配任意非空字符
'\G'	#匹配最后匹配完成的位置
'\b'	#匹配一个单词边界，也就是指单词和空格间的位置。例如，'er\b' 可以匹配"never" 中的 'er'，但不能匹配 "verb" 中的 'er'。
			# '\b左边界.*右边界\b' \b可以就理解为空格位置
'\B'	#匹配非单词边界。'er\B' 能匹配 "verb" 中的 'er'，但不能匹配 "never" 中的 'er'。
'\1...\9'#匹配第n个分组的子表达式。


'组的用法'
'(...)' #无命名组
		#re.search("(abc){2}a(123|456)c", "abcabca456c").group() 结果 abcabca456c
'(?P<name>...)' #命名组
 		'''分组匹配 re.search("(?P<province>[0-9]{4})(?P<city>[0-9]{2})(?P<birthday>[0-9]{4})",
 	                "371481199306143242").groupdict("city") 
    	结果{'province': '3714', 'city': '81', 'birthday': '1993'}'''
'(?P=name)' #命名组的调用
'\number'   #通过序号调用已匹配的组,每个组都有一个序号,从左到右从1开始.0号组为整个正则式本身。

'(?: re)'	#类似 (...), 但是不表示一个组,称为无捕获组

'(?(group_id/name)yes-pattern|no-pattern)'#条件匹配功能。判断指定组是否已匹配，执行相应的规则。

'注意：'
	# re.search((...).+(...)).group(id|name) 是懒惰查找,返回包含组信息的第一个结果,即默认0组
	# re.search((...).+(...)).groups() 也是懒惰查找,只返回第一个匹配结果的组信息
	# re.findall((...).+(...)) 全查找，但只返回组信息

"关于 '|' 要注意两点："

	#第一,它在'[]'之中不再表示或，而表示他本身的字符。

	#第二,它的有效范围是它两边的整条规则，比如'dog|cat'匹配的是'dog'和'cat',而不是'g'和'c'。
	#如果想限定它的有效范围，必需使用一个无捕获组'(?: )'包起来。
	#比如要匹配 'I have a dog'或'I have a cat'，需要写成 
		# r'I have a (?:dog|cat)’,而不能写成 r'I have a dog|cat'

#最常用的匹配语法
re.match() #从头开始匹配
	re.match().group([index|id]) #获取匹配的组，缺省返回组 0, 也就是全部值
	re.match().groups()   # 返回全部的组
	re.compile().groupdict()  #返回以组名为key,匹配的内容为 values 的字典
re.search() #匹配包含
	re.search().start()
	re.search().end()
	re.search().expand(template) #根据一个模版用找到的内容替换模版里的相应位置
re.findall() #把所有匹配到的字符放到列表中返回
re.split() #以匹配到的字符当做列表分隔符
re.sub()       #匹配字符并替换
re.subn()	#匹配字符串并替换,同时会返回替换次数
re.escape(r'(*+?)') #跳过re的符号功能,表示其本身.
re.compile(pattern)
	re.compile().flags
	re.compile().pattern
	re.compile().groupindex
#反斜杠的困扰 
'''与大多数编程语言相同，正则表达式里使用"\"作为转义字符，这就可能造成反斜杠困扰。
假如你需要匹配文本中的字符"\"，那么使用编程语言表示的正则表达式里将需要4个反斜杠"\\\\"：
前两个和后两个分别用于在编程语言里转义成反斜杠，转换成两个反斜杠后再在正则表达式里转义成一个反斜杠。
Python里的原生字符串很好地解决了这个问题，这个例子中的正则表达式可以使用r"\\"表示。
同样，匹配一个数字的"\\d"可以写成r"\d"。有了原生字符串，你再也不用担心是不是漏写了反斜杠，
写出来的表达式也更直观。'''

#匹配模式flags
flags=re.I(re.IGNORECASE) #忽略大小写（括号内是完整写法，下同）
flags=re.M(MULTILINE) #多行模式，改变'^'和'$'的行为（参见上图）
flags=re.S(DOTALL) #点任意匹配模式，改变'.'的行为

---------random----------
random.random() #生成一个0到1的随机浮点数
random.uniform(a,b) #生成一个指定范围a到b的随机浮点数
random.randint(a,b) #生成一个[a,b]的随机整数
random.randrange(a,b,step=c) #步长为c,从[a,b)随机取一个数
random.choice(sequence) #从序列中随机获取一个元素，在python中list、tuple、character都属于sequence
random.sample(sequence,k) #从指定序列中获取指定长度k的片段
random.shuffle(sequence) #对序列进行随机排列(洗牌)

---------glob----------
glob.glob(path) # 将路径作为列表返回
---------OS-------------
os.getcwd() #类似linux系统中的pwd
os.chdir() #cd
os.curdir() #返回当前目录 "."
os.pardir() #获取父目录 ".."
os.makedirs("dirname1/dirname2") #生成多层目录层级
os.removedirs("dirname") #递归删除空目录
os.mkdir("dirname") #生成单级目录"mkdir dirname"
os.rmdir("dirname") #删除单级空目录"rmdir dirname"
os.listdir("dirname") #列出指定目录所有文件和子目录
os.remove() #删除一个文件
os.rename("oldname","newname") #重命名
os.stat("path/filename") #获取文件或者目录信息
os.system("bash command") #用于执行
os.path.abspath(path) #返回path规范化绝对路径
os.path.split(path) #将path分割为目录和文件二元组
os.path.dirname(path) #返回path的目录
os.path.basename(path) #返回path的文件名
os.path.exists(path) #判断path是否存在
os.path.isabs(path) #判断是否绝对路径
os.path.isfile(path) #判断是否是存在的文件
os.path.isdir(path) #判断是否是存在的目录
os.path.join(path1,path2,[...]) #返回组合路径
os.path.getatime(path) #返回path下的文件或目录最后存取时间
os.path.getmtime(path) #返回path下的文件或目录最后修改时间
os.sep #输出操作系统特定的路径分隔符win：\\，linux:/
os.linesep #输出行终止符 win：\t\n,linux:\n
os.pathsep #输出文件路径分隔符
os.name #输出指示当前系统的字符串win:"nt",linux:"posix"
os.environ #输出环境变量

--------sys---------
sys.argv #读取命令行参数列表,argv[0]是代码本身文件路径,argv[1]是第一个参数
sys.exit()
sys.version
sys.path #返回模块的搜索路径
sys.platform #返回操作系统平台名称

sys.maxint #最大的int值 ?
sys.stdout.write("please:") 
val = sys.stdin.readline()[:-1] #?

-----shutil---------文件、文件夹、压缩包的处理模块
shutil.copyfileobj(fsrc, fdst[, length]) #将文件fsrc内容拷贝到另一个文件fdst中，可以部分内容length
shutil.copyfile(src, dst) #拷贝文件
shutil.copymode(src, dst) #仅拷贝权限,内容、组、用户均不变
shutil.copy(src, dst) #拷贝文件和权限
shutil.copystat(src, dst) #拷贝状态信息，包括：mode bits, atime, mtime, flags
shutil.copy2(src, dst) #拷贝文件和状态信息
shutil.copytree(src, dst, symlinks=False, ignore=None) #递归的去拷贝文件(拷贝目录)
shutil.rmtree(path[, ignore_errors[, onerror]]) #递归的去删除文件(删除目录)
shutil.move(src, dst) #递归的去移动文件(移动目录)
---压缩---
shutil.make_archive(base_name, format,...) #创建压缩包并返回文件路径
'''
base_name： 压缩包的文件名，也可以是压缩包的路径。只是文件名时，则保存至当前目录，否则保存至指定路径
format：	压缩包种类，“zip”, “tar”, “bztar”，“gztar”
root_dir：要压缩的文件夹路径（默认当前目录）
owner：	用户，默认当前用户
group：	组，默认当前组
logger：	用于记录日志，通常是logging.Logger对象

将 /Users/wupeiqi/Downloads/test 下的文件打包放置 /Users/wupeiqi/ 下,命名为"www"
shutil.make_archive("/Users/wupeiqi/www", 'gztar', root_dir='/Users/wupeiqi/Downloads/test')
'''
---解压---
shutil 对压缩包的处理是调用 ZipFile 和 TarFile 两个模块来进行的，详细：

import zipfile
# 压缩
z = zipfile.ZipFile('laxi.zip', 'w')
z.write('a.log')
z.write('data.data')
z.close()

# 解压
z = zipfile.ZipFile('laxi.zip', 'r')
z.extractall()
z.close()

import tarfile
# 压缩
tar = tarfile.open('your.tar','w')
tar.add('/Users/wupeiqi/PycharmProjects/bbs2.zip', arcname='bbs2.zip')
tar.add('/Users/wupeiqi/PycharmProjects/cmdb.zip', arcname='cmdb.zip')
tar.close()

# 解压
tar = tarfile.open('your.tar','r')
tar.extractall()  # 可设置解压地址
tar.close()

----------xml.etree.ElementTree-----------
xml.etree.ElementTree.parse("xml文档").getroot().tag
xml.etree.ElementTree.parse("xml文档").getroot().iter("节点")
xml.etree.ElementTree.parse("xml文档").getroot().remove("节点")

import xml.etree.ElementTree as ET

tree = ET.parse("xmltest.xml") #解析xml文档
root = tree.getroot() #获取xml所有节点
print(root.tag) #'data'

# 遍历xml文档
for a in root:
	print(a.tag, a.attrib) #遍历子节点
	for b in a:
		print(b.tag, b.text,b.attrib) #遍历孙节点

# 只遍历year 节点
for node in root.iter('year'):
    print(node.tag, node.text)

#修改
for node in root.iter('year'):
    new_year = int(node.text) + 1
    node.text = str(new_year)
    node.set("updated","yes")
 
tree.write("xmltest.xml")
 
#删除
for country in root.findall('country'):
   rank = int(country.find('rank').text)
   if rank > 50:
     root.remove(country)
 
tree.write('output.xml')

#创建
new_xml = ET.Element("personinfolist")
personinfo = ET.SubElement(new_xml, "personinfo", attrib={"enrolled": "yes"})
name = ET.SubElement(personinfo, "name")
name.text = "Alex Li"
age = ET.SubElement(personinfo, "age", attrib={"checked": "no"})
sex = ET.SubElement(personinfo, "sex")
age.text = '56'
personinfo2 = ET.SubElement(new_xml, "personinfo", attrib={"enrolled": "no"})
name = ET.SubElement(personinfo2, "name")
name.text = "Oldboy Ran"
age = ET.SubElement(personinfo2, "age")
age.text = '19'

et = ET.ElementTree(new_xml)  # 生成文档对象
et.write("test.xml", encoding="utf-8", xml_declaration=True)

ET.dump(new_xml)  # 打印生成的格式
 
---------------configparser-------------
#生成配置文件-----configparser.ConfigParser()
import configparser
 
config = configparser.ConfigParser()
config["DEFAULT"] = {'ServerAliveInterval': '45',
                      'Compression': 'yes',
                     'CompressionLevel': '9'}
 
config['bitbucket.org'] = {}
config['bitbucket.org']['User'] = 'hg'
config['topsecret.server.com'] = {}
topsecret = config['topsecret.server.com']
topsecret['Host Port'] = '50022'     # mutates the parser
topsecret['ForwardX11'] = 'no'  # same here
config['DEFAULT']['ForwardX11'] = 'yes'
with open('example.ini', 'w') as configfile:
   config.write(configfile)

#读取配置文件内容----config.read(),config.sections()
config.read('example.ini')
	['example.ini']
config.sections() #输出节点
	['bitbucket.org', 'topsecret.server.com']
'bitbucket.org' in config
	True
config['bitbucket.org']['User']
	'hg'
config['DEFAULT']['Compression']
	'yes'
import ConfigParser
  
config = ConfigParser.ConfigParser()
config.read('i.cfg')
  
#按节点读取----
secs = config.sections()
print secs

options = config.options('group2')
print options
  
item_list = config.items('group2')
print item_list
  
val = config.get('group1','key')
val = config.getint('group1','key')
  
#改写-------
sec = config.remove_section('group1')
config.write(open('i.cfg', "w"))
  
sec = config.has_section('wupeiqi')
sec = config.add_section('wupeiqi')
config.write(open('i.cfg', "w"))
   
config.set('group2','k1',11111)
config.write(open('i.cfg', "w"))
  
config.remove_option('group2','age')
config.write(open('i.cfg', "w"))

------------hashlib加密模块----------
import hashlib
 
----md5---- 
hash = hashlib.md5()
hash.update("HelloIt's me天王盖地虎".encode(encoding="utf-8"))
print(hash.hexdigest())
 
----sha1---- 
hash = hashlib.sha1()
hash.update('admin')
print(hash.hexdigest())
 
----sha256---- 
hash = hashlib.sha256()
hash.update('admin')
print(hash.hexdigest())
 
----sha384---- 
hash = hashlib.sha384()
hash.update('admin')
print(hash.hexdigest())
 
----sha512---- 
hash = hashlib.sha512()
hash.update('admin')
print(hash.hexdigest())

----hmac----#更牛逼的加密模块
import hmac
h = hmac.new(b"12345","you are 250你是".encode(encoding="utf-8"))
print(h.digest()) #十进制
print(h.hexdigest()) #十六进制

===================面向对象编程===========================
class Dog(object):
	def __init__(self,name):
		self.name = name
	def singledog(self):
		print("%s:汪汪汪。。。"% self.name)
Dog("小郑子").singledog()

class Role(object):
	n = 123 #类变量:共有属性，节省内存
	n_list = []
	name = "我是类name"
	def __init__(self, name, role, weapon, life_value=100, money=15000):
		#构造函数:__init__在实例化时做一些类的初始化的工作
		self.name = name #实质为r1.name=name,实例变量(静态属性),作用域就是实例本身
		self.role = role
		self.weapon = weapon
		self.__life_value = life_value #私有属性
		self.money = money
	def __del__(self):
		#析构函数：__del__在实例释放、销毁的时候自动执行的,通常用于做一些收尾工作,如关闭一些数据库连接,关闭打开的临时文件
		print("%s 彻底死了。。。。" %self.name)
	def show_status(self): #定义一个方法查看私有属性
		print("name:%s weapon:%s life_val:%s" %(self.name,self.weapon, self.__life_value))
	def __shot(self): #私有方法
		print("shooting...")
	def got_shot(self):# 类的方法，功能 （动态属性）
		self.__life_value -=50
		print("%s:ah...,I got shot..."% self.name)
	def buy_gun(self, gun_name):
		print("%s just bought %s" % (self.name,gun_name))

r1 = Role('Chenronghua','police','AK47') #把一个类变成一个具体对象的过程叫 实例化(初始化一个类Role，造了一个对象r1)
r1.buy_gun("AK47")
r1.got_shot()
r1.__shot() #私有方法，无法外部调用
print(r1.show_status())

r2 = Role('jack', 'terrorist', 'B22')  #生成一个角色
r2.got_shot()

-----继承-----
class People(object): #新式类
	def __init__(self,name,age):
		self.name = name
		self.age = age
		self.friends = []
		print("--doens't run ")
	def eat(self):
		print("%s is eating..." % self.name)
    def talk(self):
		print("%s is talking..." % self.name)
	def sleep(self):
		print("%s is sleeping..." % self.name)

class Relation(object):
	def __init__(self,n1,n2):
		print("init in relation")
	def make_friends(self,obj): #w1
		print("%s is making friends with %s" % (self.name,obj.name))
		self.friends.append(obj.name)

class Man(Relation,People):
	def __init__(self,name,age,money):
    #	People.__init__(self,name,age) #调用People的__init__属性
		super(Man,self).__init__(name,age) #新式类写法
		self.money  = money
	    print("%s 一出生就有%s money" %(self.name,self.money))
	def piao(self):
		print("%s is piaoing ..... 20s....done." % self.name)
	def sleep(self):
		People.sleep(self)
		print("man is sleeping ")

class Woman(People,Relation):
	def get_birth(self):
		print("%s is born a baby...." % self.name)

m1 = Man("NiuHanYang",22)
w1 = Woman("ChenRonghua",26)

m1.make_friends(w1)
w1.name = "陈三炮"
print(m1.friends[0])

----静态方法----
'''通过@staticmethod装饰器即可把其装饰的方法变为一个静态方法，
静态方法是不可以访问实例变量或类变量的，其实相当于跟类本身已
经没什么关系了，它与类唯一的关联就是需要通过类名来调用这个方法'''
class Dog(object):
	def __init__(self,name):
        self.name = name
 
    @staticmethod #把eat方法变为静态方法
    def eat(self):
        print("%s is eating" % self.name)
 
d = Dog("ChenRonghua")
d.eat()
'''调用d.eat()会出错误，当eat变成静态方法后，通过实例调用时不会自动把实例本身当作一个参数传给self。
想让上面的代码可以正常工作有两种办法:
1. 调用时主动传递实例本身给eat方法，即d.eat(d) 
2. 在eat方法中去掉self参数，但这也意味着，在eat中不能通过self.调用实例中的其它变量了'''

----类方法----
#通过@classmethod装饰器实现，类方法只能访问类变量，不能访问实例变量
class Dog(object):
	#name = "我是类变量" #定义一个类变量
    def __init__(self,name):
        self.name = name

    @classmethod
    def eat(self):
        print("%s is eating" % self.name)

d = Dog("ChenRonghua")
d.eat()

----属性方法----
#通过@property把一个方法变成一个静态属性
class Dog(object):
    def __init__(self,name):
        self.name = name
 
    @property
    def eat(self):
        print(" %s is eating" %self.name)
 
d = Dog("ChenRonghua")
d.eat()
'''调用会出以下错误，说NoneType is not callable, 
因为eat此时已经变成一个静态属性了， 不是方法了， 
想调用已经不需要加()号了，直接d.eat就可以了'''
class Flight(object):
    def __init__(self,name):
        self.flight_name = name

    def checking_status(self):
        print("checking flight %s status " % self.flight_name)
        return  1

    @property
    def flight_status(self):
        status = self.checking_status()
        if status == 0 :
            print("flight got canceled...")
        elif status == 1 :
            print("flight is arrived...")
        elif status == 2:
            print("flight has departured already...")
        else:
            print("cannot confirm the flight status...,please check later")
    
    @flight_status.setter #修改
    def flight_status(self,status):
        status_dic = {
            0 : "canceled",
            1 :"arrived",
            2 : "departured"
        }
        print("\033[31;1mHas changed the flight status to \033[0m",status_dic.get(status) )

    @flight_status.deleter  #删除
    def flight_status(self):
        print("status got removed...")

f = Flight("CA980")
f.flight_status
f.flight_status =  2 #触发@flight_status.setter 
del f.flight_status #触发@flight_status.deleter 

----类的特殊成员方法----

1.__doc__ :表示类的描述信息

class Foo:
    """ 描述类信息，这是用于看片的神奇 """
	def func(self):
		pass
print(Foo.__doc__)

2.__module__:表示当前操作的对象在那个模块
3.__class__ :表示当前操作的对象的类是什么
3. __init__:构造方法，通过类创建对象时，自动触发执行。
4.__del__:析构方法，当对象在内存中被释放时，自动触发执行。
'''此方法一般无须定义，因为Python是一门高级语言，程序员在使用时
无需关心内存的分配和释放，因为此工作都是交给Python解释器来执行，
所以，析构函数的调用是由解释器在进行垃圾回收时自动触发执行的'''
5.__call__:对象后面加括号，触发执行。
'''构造方法的执行是由创建对象触发的，即：对象 = 类名() ；而对于 
__call__ 方法的执行是由对象后加括号触发的，即：对象() 或者 类()()'''
6.__dict__:查看类或对象中的所有成员属性、方法 #类/对象.__dict__
7.__str__：在打印对象时，默认输出该方法的返回值
8.__getitem__、__setitem__、__delitem__：用于索引操作，如字典。分别表示获取、设置、删除数据
class Foo(object):
    def __getitem__(self, key):
        print('__getitem__',key)
 
    def __setitem__(self, key, value):
        print('__setitem__',key,value)
 
    def __delitem__(self, key):
        print('__delitem__',key)
 
obj = Foo()
 
result = obj['k1']  # 自动触发执行 __getitem__
obj['k2'] = 'alex'  # 自动触发执行 __setitem__
del obj['k1']  #触发执行 __delitem__
9.__new__, __metaclass__：#对象是通过执行类的构造方法创建，类对象是 type 类的一个实例，即：类是通过type类的构造方法创建
#__new__先于__init__执行
#metaclass 详解文章：http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python 得票最高那个答案写的非常好

----反射----
class Foo(object):
    def __init__(self):
        self.name = 'wupeiqi'
 
    def func(self):
        return 'func'
obj = Foo()
 
# 检查是否含有成员 
hasattr(obj, 'name')
hasattr(obj, 'func')
 
# 获取成员 
getattr(obj, 'name')
getattr(obj, 'func')
 
# 设置成员 
setattr(obj, 'age', 18)
setattr(obj, 'show', lambda num: num + 1)
 
# 删除成员
delattr(obj, 'name')
delattr(obj, 'func')

==========================socket=================================
#http://www.cnblogs.com/wupeiqi/articles/5040823.html
==========================thread=================================
#http://www.cnblogs.com/alex3714/articles/5230609.html
#
==========================字体颜色控制===========================
格式：\033[显示方式;前景色;背景色m
 
说明：
前景色            背景色           颜色
---------------------------------------
30                40              黑色
31                41              红色
32                42              绿色
33                43              黃色
34                44              蓝色
35                45              紫红色
36                46              青蓝色
37                47              白色
显示方式           意义
-------------------------
0                终端默认设置
1                高亮显示
4                使用下划线
5                闪烁
7                反白显示
8                不可见
 
例子：
\033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
\033[0m          <!--采用终端默认设置，即取消颜色设置-->
