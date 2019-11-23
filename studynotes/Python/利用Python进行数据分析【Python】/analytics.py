==========ipython magic command========
command? command??
%run/ %paste/ %cpaste --
%timeit/ %who / %who_ls /%whos 
%xdel variable 
_  __ :最近两次的输出结果
_行号：输出结果
_i行号 ：输入结果
%logstart /%logstop /%logon /%logoff

dic.iteritems() #返回字典的键值

==============itertools===========
itertools.permutation() #将一个序列进行随机排列
itertools.combinations(items,2) #不放回抽样
itertools.combinations_with_replacement(items,2) #有放回抽样
itertools.product(items1,items2) #笛卡尔积,即排列组合

===========numpy=============
注意：1.ndarray的切片是原始数组的视图,视图上的任何修改都会反映都源数组上.
		需显示复制 -> array[3:6].copy()
		数组转置array.transpose((1,2,0))/array.T 和
		数组轴对换array.swapaxes(1,2) 也返回数据视图
	#对比	
	2.数组布尔型索引创建的是副本,且python关键字and与or无效
	3.花式索引,如array[[],[]]也是复制
 
array = np.array([[],[],[],...])
	array.shape #维度元组
	array.dtype #数据类型
		np.astype(np.float64) #显示转换数组数据类型
	array.ndim #几维的
np.zeros(n)/np.zeros((m,n)) #全0数组
	np.zeros_like() #根据另一个数组创建全1数组
np.ones(n)/np.ones((m,n)) #全1数组
	np.ones_like()
np.empty((x,y,z)) #随意值,元组均表示形状
	np.empty_like()
np.asarray() 
np.arange() #range的数组版
np.eye()/np.identity() #创建单位阵
np.linspace(a,b,n) #从a到b生成n个等间距的数
np.around(array,2) #np的round()
np.save(path,array)
np.load(path)
np.sort() 
np.argsort() #排序后返回原序号

np.concatenate()
np.vstack()
np.hstack()/array.flatten()
np.dstack()/array.T
#数组函数np.
	#一元ufunc--接收一个数组
	abs/fabs
	sqrt/square
	exp/log/log1p #log1p为log(1+x)
	sign #返回正负或0
	ceil/floor #向上/向下取整
	rint #四舍五入到最近整数
	modf #以独立数组形式返回数组的小数和整数部分
	isnan/isinf/isfinite
	cos/sin/tan/arcsin/...
	logical_not #not x 的真值
	
	#二元ufunc--接收2个数组
	add/substract/multiply/divide/floor_divide
	power #计算A的B次方
	maximum/fmax #元素级最大值运算,fmax忽略NaN
	minimum/fmin
	mod #求模,即取余
	copysign #将第二个数组中值的符号赋予第一个数组
	greater/greater_equal/less/less_equal/equal/not_equal
	logical_and/logical_or/logical_xor-> ^

np.where(cond,a,b) #满足条件为a,否则为b
	->cond :逻辑条件,利用np.logical_and/np.logical_or/np.logical_not表示复合逻辑
#数组统计方法
sum(axis=1)/mean()/std()/var()/min()/max()/
argmin()/argmax() #返回最值的索引
cumsum()/cumprod()

#数组排序
array.sort() #就地排序
np.sort()#顶级方法,返回排序副本

#数组的集合运算
np.unique()
np.diff(array,axis=1) #两个临近数值的减法,后一个数减前一个
np.intersect1d(array1,array2) 
np.union1d(array1,array2) 
np.in1d(array1,array2) #array1的值是否在array2中
np.setdiff1d(array1,array2) #在arra	y1中而不在array2中,即差集
np.setxor1d(array1,array2) #对称差,即非共同元素

#数组读写
np.load("path",array)/np.save()/np.savez()保存多个数组
np.loadtxt()/np.savetxt()

#线代运算numpy.linalg
mat.diag() #获取对角线元素,或将一维数组转为方阵
mat.dot() #矩阵乘法
mat.trace() #对角元素和
mat.det() #行列式
mat.eig() #计算特征值和特征向量
mat.inv() #计算逆矩阵
mat.pinv() #计算伪逆
mat.qr() #QR分解
mat.svd() #奇异值分解
mat.solve() #解线性方程组AX=b
mat.lstsq() #计算AX=b的最小二乘解

#随机数numpy.random
seed() #随机数生成器的种子
permutation() #随机排列
shuffle() #就地随机排列
rand() #随机均匀分布
randint() #随机整数
randn() #随机标准正态
binomial() #随机二项分布
normal(loc=mean,scale=std,size=(m,n))# m行n列正态分布
standard_normal((shape)) #标准正态
beta()# Beta分布
chisquare() #卡方分布
gamma() #伽马分布
uniform() #[0,1]均匀分布

#补充
np.assert_array_almost_equal(,,decimal=3,err_msg='',verbose=True)

===========pandas============
from pandas import Series,DataFrame
import pandas as pd
#数据结构
---Series---
Series().index
Series().index.name #序列索引名
Series().values
Series().name #序列名 
Series().isnull()/pd.isnull()#检测缺失值
Series().notnull()/pd.notnull()
重要功能：在算术运算中会自动对齐不同索引的值
---DataFrame---
DataFrame(data,index=[],columns=[])
DataFrame().index.name
DataFrame().columns.name 
DataFrame().values 
DataFrame().T #转置

frame["A"] = frame["B"]=="a" #注意这种赋值操作A变量为逻辑值
	
index的属性和方法:如 DataFrame().index.is_unique
	append 
	diff
	intersection
	union
	isin
	delete #删除索引i处的元素,并得到新的index
	drop #删除传入的值,并得到新的index
	insert
	is_monotonic #各元素均大于等于前一个元素时为True(升序)
	is_unique
	unique 
df.index.contains('Intercept')
df.index.get_level_values(0)
df.index.get_values()/df_ols.index.values
df.index.labels
df.index.levels
df.index.set_levels()
df.index.set_labels()
df.index = df_ols.index.droplevel(1)
df.index.where(df_ols.index=='Intercept')

#重新索引reindex
  ``DataFrame.reindex`` supports two calling conventions
 
  * ``df.reindex(index=index_labels, columns=column_labels, ...)``
  * ``df.reindex(labels, axis={'index', 'columns'}, ...)``
reindex([index],[columns],fill_value=0,method=ffill,limit)
		-> method=ffill/pad/bfill/backfill
		->limit 最大填充量
s.reindex([1, 2, 3])

labels = [1, 2, 3]
s.loc[s.index.intersection(labels)]
s.loc[s.index.intersection(labels)].reindex(labels) #索引重复时

#删除行列
drop(,axis=0) #0表示作用于行,1表示作用于列

#DataFrame()的索引
ix[[index],[columns]] #提取子集 ---deprecated
xs[] #根据标签选取单行或单列
irow/icol[] #根据整数位置选取单列或单行

deprecated 0.21:
	get_value[,] #根据行标签和列标签获取值
		iget_value() #序列索引,获得第几个值
	set_value(index,col,value) #根据行标签和列标签设置值
new: 
	df.at[,]
	df.iat[,]

#DataFrame的运算
.add(,fill_value=0) +
sub -
mul *
div /
 
#函数与映射
apply(func,axis=1) #默认作于于列,axis=1作用于行
applymap(func) #作用于每一个值(元素级函数)

Series().map() #序列的元素级map

#排序
sort_index(axis=1,ascending=False) #列索引降序排列
sort_index(by=["a","b"]) #根据多列排序
order() #对值排序
#排名:根据值的大小给出排名
rank(ascending=True)  #默认赋予平级关系平均值,默认从小到大,参数改为从大到小排名
rank(method="first") #按顺序赋予排名
	->method="first" #按原始顺序排名
			"min/max" #按分组的最大/小排名
			"average" #默认

#描述统计(默认列)
sum()/cumsum()/cummin()/cummax()/cumprod()
mean(axis=1,skipna=False)/median()
var()/std()/mad()
min()/max()/quantile()
idxmax()/idxmin() #达到最大值或最小值的索引
argmax()/argmin() #同上
count()
diff() #一阶差分
pct_change() #计算百分数变化(如增长率)
describe()
skew()/kurt()
corr()/corrwith() #相关系数
cov()/covwith() #协方差

#唯一值,值计数,成员资格
unique()#唯一值
value_counts() #值计数,默认降序排列.对比count()
	pd.value_counts(obj.values,sort=False) #顶级pandas方法,可接收任何数组或序列
	df.apply(pd.value_counts).fillna(0) #传入数据框需要apply函数
isin()

#缺失值
dropna() #默认删除含有缺失值的行,删除后索引值不变
dropna(axis=1,how="all") #删除全为缺失值的列

fillna(0,inplace=True,method,limit) #inplace就地修改,method与limit同reindex
fillna({1:0,2:0.5}) #可传入字典实现对不同列缺失值的填充

#层次化索引
--创建层次化索引
	index=[[],[],...]
	MultiIndex.from_arrays([[],[]],names=[])
data.index #MultiIndex为元组列表
data[第一层,第二层] #多重索引类似于ix[,]用法
df.index.names
df.columns.names
	#重排序
	df.sort_values(ascending=True)
	df.sortlevel(0) #根据第一层索引排序
	df.swaplevel(0,1) #第一二层索引互换
	#根据索引级别level进行统计,功能同groupby
	df.sum(level="index",axis=1)
	#行列索引转换
	set_index("col",drop=False) #将列转换为行索引,参数为保留列
	reset_index() #与上述相反,索引级别会被转移到列
--重塑层次化索引
data.stack() #堆积,"竖着放"
data.unstack() #非堆积,"横着放"
data.unstack('').stack(0,dropna=False) 
	#stack操作默认为最内层,可以传入索引级别或名指定,也默认删除缺失值 

#面板数据
pd.Panel() #items(vars) x major(stkcd) x minor(year)
pd.Panel().swapaxes("items", "minor") #行列互换
pd.Panel().ix['major','minor','items'] #Panel提取子集
pd.Panel().to_frame() #堆积式,一般最熟悉的形式
	to_panel() #面板式,to_frame的逆运算

#读取文件
pd.read_csv()
pd.read_table(path,sep='')
pd.read_fwf()/pd.read_clipboard()
Series.from_csv(path,parse_dates=True) #将df读取为序列

read_csv()/read_table()的参数：
	path/sep或delimiter
	header=None      #第一行不作为标题
	index_col=[""] 	 #将列作为行索引(传入编号或名字)==set_index()
	names=[""] 		 #自定义列名
	skiprows=[]/skip_footer=[]      
	nrows=5
	na_values=[""]   #替换NA的值
	parse_dates=False/[] #解析日期,可指定列
	keep_date_col=False #解析多列日期,用于保持连接的列
	date_parser 	 #解析日期的函数
	converters 		 #字典参数{'col':func}可对列映射应用函数func
	encoding="utf-8"
	thousands  
	      #千分位分隔符
#输出文件
pd.to_csv(path,sep='',na_rep='',...)
	index=False,header=False #不输出行列标签
	cols=['','',...] #写出部分列

pd.date_range(start,end,periods,freq)

#Excel 读写
pd.ExcelFile('xls').parse('sheet1')

#JSON
import json
json.loads("json") #将json转换为python形式
json.dumps("obj")  #将python对象转换为json格式


#数据合并
pd.merge(df1,df2,...) #只能合并df
	on='' #连接键
	left_on='' / right_on=''
	how='inner' #left/right/outer
	left_index/right_index=True/False #将索引用作连接键
	sort='True' #默认排序,大数据禁用可获得更好的性能
	suffixes='' #重叠列后缀
	copy='False'

df1.join([df2,df3],on='',how='') #默认索引合并,也可用on指定

pd.concat([df1,df2],...)
	axis=0/1 #连接轴,默认0
	join='inner/outer' #连接方式
	join_axes=[] #指定用于连接的索引
	keys=[] #用于创建层次化索引,与axis=1连用,keys会成为列索引
	names=[] #层次化索引名
	ignore_index='False/True' #是否保留原有索引,产生一组新索引range(total_length)
	verify_integrity='False' #是否允许重复

#利用外来数据填补缺失数据
df1.combine_first(df2) #利用df2的数据为df1的缺失数据打补丁

# 数据透视表
data.pivot('index','columns','values') #功能等价于
	-> data.set_index('col1','col2').unstack('col2')
#处理重复值
data.duplicated() #判断重复值
data.drop_duplicates(subset=[''],take_last=True/keep='last') #指定删除重复值,保留最后一个重复值
#值替换
data.replace(a,b) #a体替换为b
data.replace({a:b,c:d}) #传入字典替换多个值
#重命名
data.rename(index={'':''},columns={'':''},inplace=True)

#面元划分
pd.cut(x, bins,right=False,retbins=True) #按区间划分,right参数表示右边为闭区间
	有俩个属性labels->表示属于哪个区间
			 levels->表示具体区间划分水平
	可以自行设置分组名称->pd.cut(x, bins,labels=['',''])
pd.qcut(x, q) #按分位数划分,q可以是单个数值也可以是自定义区间[,,]			 

#随机重排序与取样
np.random.permutation(N) #随机排序->N为数据集的大小len
df.take(np.random.permutation(N)[:n]) #取前n行为样本

#生成虚拟变量
pd.get_dummies(df[''],prefix='') #其实是二值变量矩阵
	pd.get_dummies(pd.cut(x, bins)) #结合例子

#字符串操作
string.index('') #返回发现的第一个字符索引位置,不存在引发异常
string.find('') #返回发现的第一个字符索引位置,不存在为-1
	string.rfind('') #从最后开始找
string.count()
string.endswith()/string.startswith()
''.join() 
string.replace('','')
string.strip()
string.split()
string.ljust()/string.rjust() #用空格填充字符串空白处

#正则表达式
regex=re.compile(r'')
regex.findall() #查找所有
	regex.finditer() #通过迭代器逐个返回
regex.search() #查找所有,但只返回第一个
regex.match() #只匹配字符串起始位置
regex.split()
regex.sub('',data) #对data进行查找并替换为''
	regex.subn()
	
	#利用Series的str属性进行矢量化操作,可跳过NA值
	data.str.contains('')
	data.str.cat('') #元素级字符串连接,可指定分隔符
	data.str.count('')
	data.str.endswith('')
	data.str.startswith('')
	data.str.findall('')
	data.str.match('')
	data.str.pad(side="left")
	data.str.center() #相当于str.pad(side='both')
	data.str.split()
	data.str.strip()
	data.str.replace()
	data.str.slice() #子串截取

===============matplotlib=================
plt.style.available
plt.style.use()

from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
monthdays = MonthLocator()
mondays = WeekdayLocator(MONDAY)  # 主要刻度
alldays = DayLocator()    # 次要刻度
ax.xaxis.set_major_locator(mondays) #主轴
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d')) #主轴日期格式
ax.xaxis.set_minor_locator(alldays) #次轴

-------------------------------------
import matplotlib.pyplot as  plt
from numpy.random import randn

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)                                
	-> fig,axes = plt.subplots(nrows,ncols,sharex,sharey,subplot_kw,figsize=(8,6)) 
		#创建figure和subplot的两个步骤合为一步,subplot_kw为创建subplot的关键字字典
plt.plot() #直接使用命令会自动创建figure和subplot

#调整subplot周围的间距
plt.subplots_adjust(left=None,bottom=None,right=None,top=None,wspace=None,hspace=None)

#颜色color,标记marker,线型linestyle
plt.plot(x,y,linestyle="--",color='g',marker='o')
	->plt.plot(x,y,'go--') #隐式指定标记和线型必须放在颜色后面

#修改非实际数据点的连接方式(默认线性)--drawstyle
plt.plot(randn(30).cumsum(),'k-',drawstyle='steps-post',label='steps-post')
plt.legend(loc='best')

#轴范围、刻度、标签、标题、图例
plt.xlim()不带参数为获取范围属性,带参数为设置属性,分别对应
	ax.get_xlim()
	ax.set_xlim()

ax.set_xticks() #设置刻度
ax.set_xticklabels() #设置刻度标签

ax.set_xlabel() #设置轴标签
ax.set_title() #设置标题

设置图例有两种方法：
	ax.plot(...,label='') #创建图形时通过图例标签label指定
	ax.legend() #单独明确设置

#添加注释annotate、文本text与箭头arrow
ax.text(x,y,'text',family="monospace",fontsize=10) #(x,y)指定坐标位置
ax.annotate('',xy=(x,y=y.asof(x)),xytext(x',y'),arrowprops=dict(facecolor='black'),
				horizontalalignment='left',verticalalignment='top') #y.asof(x) 找到对应x的y值

#绘制几何图形-这些对象被称为块matplotlib.patches
需要先创建块对象,然后添加到subplot中
fig = plt.figure()
ax = fig.add_subplot（1,1,1）

retc = plt.Rectangle((x,y), width, height,color,alpha) #四边形对象
circ = plt.Circle((x,y),0.15,color='b',alpha=0.3) #圆或椭圆对象
pgon = plt.Polygon([[x1,y1],[x2,y2],[x3,y3]],color,alpha) #多边形对象,三个坐标为三角形

ax.add_patch(rect) #添加对象
ax.add_patch(circ)
ax.add_patch(pgon)

# 图表保存
plt.savefig('.svg/png/jpg/pdf',dpi=400,bbox_inches='tight',facecolor='w',format='png')

#自定义matplotlib的配置
custom_options={'family':'monospace',
				'weight': 'bold',
				'size': 'small'}
plt.rc('font',**custom_options) #rc第一个参数为对象如'figure','axes','xtick','grid','legend'

#pandas绘图
--序列绘图
s.plot(...) 
	ax=ax #在其上作图的matplotlib subplot 对象
	style='ko--' #风格字符串
	alpha=0.5
	kind='line/bar/barh/kde' #图形类型
	use_index=True #将对象的索引用作刻度标签
	rot=45 #刻度标签旋转角度
	xticks=[2,3,5] #x轴刻度值
	xlim=[0,10] #轴范围
	grid=True #显示网格线
	logy #Y轴适用对数尺度
--数据框绘图
df.plot()
	... 适用以上序列绘图参数
	subplots=True #将各列绘制到单独的子图中
	sharex/sharey
	figsize #表示图形大小的元组
	title #图形标题
	legend=True
	sort_columns #以字母表顺序绘制列,默认当前顺序

#柱状图
df.plot(kind="barh",stacked=True,alpha=0.5) #堆积柱状图
	妙用s.value_counts().plot(kind='bar')

ax.bar(bottom=range(4,20,2),width=df[:,0],left=df[:,1],height=2,color='g',alpha=0.2)
pandas创建交叉表：pd.crosstab(index,columns)

#直方图和密度图
df['columns'].hist(bins=50)
df['columns'].plot(kind='kde')

#散点图与散点图矩阵
plt.scatter(x, y)
pd.scatter_matrix(df,diagonal='kde',color='k',alpha=0.3) #对角线diagonal放置密度图

===========seaborn=============
import seaborn as sns
sns.set_context('paper'/'talk'/'notebook'/'poster')#内置主题
sns.set_palette('muted'/'Blues_d'/'Blues'/'RdBu') #调色板
sns.distplot(x,bins,kde=True,rug=True) 
sns.jointplot(x, y,size) #散点直方图夹相关系数
sns.lmplot(x, y, data,size) #仅线性回归等同于sns.jointplot(x, y, kind='reg',size)
sns.heatmap(data,annot=True,linewidths=.5)
sns.pairplot(data)

============数据聚合agg与分组运算groupby============
df.groupby([]).size() #此方法可返回分组大小,即分的组各有多少
df.groupby().name #返回分组名

#对分组进行迭代
for name,group in  df.groupby('key1') #返回一个二元元组(keyvalue,dfn)
for (name1,name2),group in  df.groupby(['key1','key2']) #返回一个嵌套二元元组((keyvalue1,keyvalue2),dfn)

#分组依据
	#根据dtype分组
		grouped = df.groupby(df.dtype,axis=1) #列向根据数据类型分组
		dict(list(grouped)) #数据分组后实质形成了分组的数据片段,做成字典后可以根据键值进行索引
	#根据字典分组
		df.groupby(dict,axis=1) #如果分组的依据是一个以索引为键的字典,则分组是按照键值对的值分组的

	#根据函数分组
		df.groupby(len) #直接传入函数,根据索引的长度分组

	#混合分组
		df.groupby([len,key_list]) #分组依据可以是数组、列表、字典、序列和函数,可以混合使用
	#根据索引级别分组
		df.groupby(level='indexname',axis=1)
#GroupBy对象的选取
df.groupby(['key1','key2']).[['data1']] #传入列表或数组,返回的对象时一个已分组的DataFrame
df.groupby(['key1','key2']).['data1'] #传入标量形式的单个列名,返回的对象时一个已分组的Series

#数据聚合
df.groupby().describe()
df.groupby().prod() #非NA的积
df.groupby().first() #第一个非NA值
df.groupby().last() #最后一个非NA值
df.groupby().agg([(colname1,func1),(colname2,func2)]) #func可以为自定义函数,colname为聚合列名,默认为函数名
	df.groupby().agg().add_prefix('') #快速统一添加前缀命名
df.groupby().agg({"var1":['min','max'],'var2':'sum'}) #传入字典实现对不同变量计算不同的值

#禁用分组键
	#GroupBy默认以分组键作为索引,通过as_index=False禁用
		df.groupby([],as_index=False) #效果等同于reset_index
	#分组键会跟原始对象的索引共同构成结果对象中的层次化索引,通过group_keys=False禁用
		df.groupby('',group_keys=False)

#分组运算后数据转换
df.groupby().transform(np.mean) #通过transform进行聚合,会以原数据的形式返回结果,而不是'取出数据'

#apply函数
df.groupby().apply(func,fargs) #func一般为自定义函数,fargs为函数参数

#分位数和桶分析
pd.cut(x,n) #按长度等分为n部分
pd.qcut(x,n,labels=False) #按数量等分,传入参数labels=False,返回的结果是分组编号,即属于第几个n分位数

#分组填充缺失值
fill_mean = lambda g: g.fillna(g.mean())
df.groupby().apply(fill_mean)

#分组加权平均
df.groupby().apply(lambda g: np.average(g['data'],weights=g['weights']))

#分组线性回归
import statsmodels.api as sm
def regress(data,yvar,xvars):
	Y=data[yvar]
	X=data[xvars]
	X['intercept'] = 1
	result = sm.OLS(Y,Xendog).fit()
	return result.params
df.groupby().apply(regress,'y',['x','z'])

#GroupBy的应用--透视表和交叉表
	df.pivot_table(['',''],rows=[''],cols=[''],aggfunc='sum',fill_value=0,margins=True) #默认所有列,默认聚合分组平均
	pd.pivot_table() #顶级方法

	pd.crosstab(index, columns,margins) #交叉表,属于透视表的一种,只用于计算个数,即count

#字典映射dict.get()--允许没有映射关系时也能'通过'
dic = {}
func = lambda x : dic.get(x,x)
df[''].map(func)

#求比例--例如总赞助额比例
totals.div(totals.sum(1),axis=0)

========================时间序列=====================
datetime.datetime 可简写为datetime
#日期与时间属性的调用
datetime(2012,8,3,12,4,30).year/month/day
datetime.timedelta(926,56700).days/seconds

#日期解析
	#标准库datetime
	datetime.strptime(timestr)
	#一个实用但不完美的工具dateutil.parser.parse
	from dateutil.parser import parse
	parse(timestr,dayfirst=True) #国际通用格式日在前,需加dayfirst参数
	#pandas解析日期--pandas.tseries.index.DatetimeIndex
	pd.to_datetime(timestr)

#datetime格式定义
	noted in line 117-125 of pystudy.py file

#时间序列的索引
	ts.index
	ts.index.is_unique #is_unique属性用于判断索引是否唯一

#时间序列的切片选取
	ts[timestr]
		#传入的索引可以是字符串日期、datetime或Timestamp
		ts['2/4/2013']
		#范围查询
		ts['2011-6':'2012-10'] 或 ts.truncate(after='2012-10') #after表示截止
		#切片所产生的是源时间序列的视图
	#对比数据框的选取
	df.ix['2/3/2011']

#生成日期范围
	pd.date_range(start,end,period,freq,normalize,tz,...) #用于生成指定长度的DatetimeIndex
		->normalize=True #表示将时间规范化到午夜,即当日零点

#频率和日期偏移量offsets
from pandas.tseries.offsets import YearEnd,MonthEnd,Day,Hour,Minute
Hour(n) #表示n小时
Minute(n) #表示n分钟
Hour(2)+Minute(40)+MonthEnd(1) #偏移量可通过加法连接
	->频率可用字符串表示,如'2h30min'
	
	->常用时间序列的基础频率
		D #每日历日
		B #每工作日
		H #每小时
		T/min #每分
		S #每秒
		M #每月最后一个日历日
		BM #每月最后一个工作日
		MS #每月第一个日历日
		BMS #每月第一个工作日
		W-MON/W-TUE/... #指定星期几开始的每周
		WOM-1MON/WOM-2MON/... #每月的第几个星期几
		A-JAN/A-DEC/... #指定以几月结束的一年

#时间序列的超前和滞后
ts.shift(2)/ts.shift(-2) 前移2个单位/后移两个单位 #对数据进行位移
ts.shift(2,freq='3D')/ts.shift(-1,freq='A-DEC') #传入频率可实现对时间戳的位移而不是对数据位移
	#显式地将日期前后滚动
	MonthEnd(2).rollforward(datetime.now()) #前滚
	MonthEnd(2).rollback(datetime.now()) #后滚

#时区
import pytz--pandas已经包含了pytz
pytz.common_timezones() #查看所有时区
	#时区的本地化->转换
	ts.tz_localize('Asia/Shanghai')
	ts.tz_localize('Asia/Shanghai').tz_convert('UTC')
	#时区意识型时间戳
	pd.Timestap('2011-03-12 04:00',tz='US/Eastern').tz_convert('Europe/Moscow').value
	->无论哪个时区,时区意识型时间戳对象内部都保存了UTC时间戳值'.value'
	->不同时区的运算会被转为UTC

#时期
pd.Period(2007,freq='A-DEC') #表示2007年1月1日-2007年12月31日
pd.period_range(start,end,freq) #可创建规则的时期范围
	#时期的频率转换
	pd.Period().asfreq('M',how='start/end')
	pd.Period('2012Q4',freq='Q-DEC').asfreq('D','start') #前部分表示2012年的第四个季度,季度的划分是以12月为财年末
	#时期与时间戳的转换
	ts.to_period('M').to_timestamp(how='end')

#创建PeriodIndex
pd.PeriodIndex(year=data.year,quarter=data.quarter,freq='Q-DEC')

#重采样--升采样/降采样
	ts.resample(**args)
		feq #重采样频率,如'M','5min',Second(15)
		how='mean' #产生聚合值得函数,其他'sum','ohlc','median','max','min'等
		axis=0 #重采样的轴
		fill_method=None #升采样时的插值方式,如ffill,bfill,默认不插值
		limit=None #插值填充的期数
		kind=None #选择聚合到period还是timestamp,默认聚合到时间序列的索引类型
		closed='right' #降采样中哪一端闭合(包含)
		label='right' #降采样中如何设置聚合值的标签(面元边界)
		loffset=None #将聚合标签进行偏移,如'-1s'
		convention='end' #升采样所采用的约定'start'与'end'
	example->
		ts.resample('5min',how='sum',closed='left',label='left',loffset='-1s')
		df.resample('A-DEC',fill_method='ffill',limit=11)

#移动窗口函数和指数加权函数--pd.
rolling_count #移动窗口非NA观测值的数量
rolling_sum #移动窗口的和
rolling_mean #移动窗口的平均值
rolling_median #移动窗口的中位数
rolling_var/std #移动窗口的方差和标准差
rolling_skew/kurt #移动窗口的偏度和峰度
rolling_min/max #移动窗口的最大和最小值
rolling_quantile #移动窗口指定分位数位置的值
rolling_corr/cov #移动窗口的相关系数和协方差
rolling_apply #对移动窗口应用数组函数,函数可自定义
ewma  #指数加权移动平均
ewmvar/ewmstd  #指数加权移动方差和标准差
ewmcorr/ewmcov  #指数加权移动相关系数和协方差

--example:
fig,axes = plt.subplots(2,1,sharex=True,sharey=True,figsize=(12,7))
aple_px = close_px.AAPL['2005':'2009']

ma60 = pd.rolling_mean(aple_px, window=60,min_periods=50)
ewma60 = pd.ewma(aple_px,span=60)#span为时间间隔,作为衰减因子使得近期观测值拥有更大的权重

aple_px.plot(style='k-',ax=axes[0])
ma60.plot(style='k--',ax=axes[0])
aple_px.plot(style='k-',ax=axes[1])
ewma60.plot(style='k--',ax=axes[1])
axes[0].set_title('Simple MA')
axes[1].set_title('Exponentially-weighted MA')

	#二元移动窗口函数
	pd.rolling_corr(x,y,window,min_periods)
	pd.rolling_corr(df,ts,window,min_periods)

#样本中特定值的百分等级
from scipy.stats import percentileofscore
score_at_2percent=lambda x:percentileofscore(x, 0.02)
pd.rolling_apply(arg, window, func) #func处如score_at_2percent




























