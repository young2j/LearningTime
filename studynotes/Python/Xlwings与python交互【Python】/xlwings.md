<h1 style='text-align:center'><code>xlwings</code></h1>
# 连接到工作簿

```python
import xlwings as xw
book = xw.Book() #新建一个工作簿
book = xw.Book('path/to/.xlsx') #连接到现有工作簿
```

```python
#如果同一工作簿在多个实例中打开。 要连接到活动应用程序实例中的工作簿，请使用
app = xw.App() 
app.books['Book1']
# 或类似现有应用程序的xw.apps [10559]，通过xw.apps.keys（）获取可用的PID
xw.apps[10559].books['FileName.xlsx']
```

# 语法概述

## 活动对象

```python
app = xw.apps.active # 活动应用程序——Excel实例
wb = xw.books.active # 活动app
sht = xw.sheets.active #活动工作簿
dataRange = xw.Range('A1') #活动应用程序中的活动工作簿里的活动工作表中的区域

wb = app.books.active #特定app
sht = wb.sheets.active #特定工作簿
```

## Range

### select

```python
xw.Range('A1')
xw.Range('A1:C3')
xw.Range((1,1))
xw.Range((1,1), (3,3))
xw.Range('NamedRange')
xw.Range(xw.Range('A1'), xw.Range('B2'))
```

```python
# 完整写法，下述Range是一样的【注意大小写】
xw.apps[763].books[0].sheets[0].range('A1')
xw.apps(10559).books(1).sheets(1).range('A1')
xw.apps[763].books['Book1'].sheets['Sheet1'].range('A1')
xw.apps(10559).books('Book1').sheets('Sheet1').range('A1')
```

### index & slice

```python
# rng[row,col]
# rng[col] 与pandas区别的地方
>>> rng = xw.Book().sheets[0].range('A1:D5')
>>> rng[0, 0]
 <Range [Workbook1]Sheet1!$A$1>
>>> rng[1]
 <Range [Workbook1]Sheet1!$B$1>
>>> rng[:, 3:]
<Range [Workbook1]Sheet1!$D$1:$D$5>
>>> rng[1:3, 1:3]
<Range [Workbook1]Sheet1!$B$2:$C$3>
```

> 快捷方式：

```python
sht = xw.Book().sheets['Sheet1']
sht['A1'] # 等价于sht.range('A1')
sht['A1:B5']
sht[0,1]
sht[:10,:10]
```

### api

>  style set/get

```python
font_name = sht.range('A1').api.Font.Name	# 获取字体名称
font_size = sht.range('A1').api.Font.Size	# 获取字体大小
bold = sht.range('A1').api.Font.Bold		# 获取是否加粗，True--加粗，False--未加粗
color = sht.range('A1').api.Font.Color	
```

# 数据结构

## 单元格cell

```python
sht['A1'].value # get
sht['A1'].value = 1 # set

# 等价于
sht.range('A1').value
sht.range('A1').value=1
```

## 列表row/col

```python
sht.range('A1:A5').value # get
sht.range('A1:A5').value = [1,2,3,4,5] # set 
# 注意！！！ 这是行方向赋值,结果赋值给了A1 B1 C1 D1 E1

#列方向赋值法一
sht.range('A1:A5').value =[[1],[2],[3],[4],[5]] 
列方向赋值法二
sht.range('A1:A5').options(transpose=True).value = [1,2,3,4,5]
```

```python
# 单个单元格作为列表表达
>>>sht.range('A1').options(ndim=1).value
  [1.0]
>>> sht.range('A1:A5').options(ndim=2).value
[[1.0], [2.0], [3.0], [4.0], [5.0]]
>>> sht.range('A1:E1').options(ndim=2).value
[[1.0, 2.0, 3.0, 4.0, 5.0]]  
```

```python
# 只需要指定起点位置'A10'或(10,1)，便可按列表输入
sht.range('A10').value = [['Foo 1', 'Foo 2', 'Foo 3'], [10, 20, 30]] # 两行
```

## 扩展expand

> expand args: 
>
> ​	table：down+right
>
> ​	down
>
> ​	right

```python
sht.range('A1').expand('table') #静态扩展，其值仅为当前table
sht.range('A1').options(expand='table') #动态扩展，当加入新数据时，会包含新的table值
```

## numpy

```python
sht.range('A1').value = np.eye(3)
sht.range('A1').options(convert=np.array,expand='table').value #返回np数组
#注意如果不expand，只返回起点处的值
```

## pandas

### DataFrame

```python
df = pd.DataFrame([[1,2],[3,4]],columns=['col1','col2'])
sht.range('A1').value=df
#sht.range('A1').options(index=False).value = df
#sht.range('A1').options(index=False, header=False).value = df
sht.range('A1').options(convert=pd.DataFrame，expand='table').value 
```

### Series

```python
s = pd.Series([1.1, 3.3, 5., np.nan, 6., 8.], name='myseries')
sht.range('A1').value = s
#sht.range('A1').options(index=False,name=False).value = s
sht.range('A1:B7').options(convert = pd.Series).value
```

# Python API

 http://docs.xlwings.org/en/stable/api.html 

