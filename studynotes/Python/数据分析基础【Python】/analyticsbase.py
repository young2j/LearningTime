#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-28 19:27:10
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
========列表排序=========sorted、itemgetter
my_lists = [[1,2,3,4], [4,3,2,1], [2,4,1,3]]
my_lists_sorted_by_index_3 = sorted(my_lists, key=lambda index_value: index_value[3])

from operator import itemgetter #itemgetter 用于对一个列表集合按照多个索引位置排序
my_lists = [[123,2,2,444], [22,6,6,444], [354,4,4,678], [236,5,5,678], \
[578,1,1,290], [461,1,1,290]]
my_lists_sorted_by_index_3_and_0 = sorted(my_lists, key=itemgetter(3,0))

=======使用glob读取多个文本文件======glob.glob()
import os,sys,glob
filepath = sys.argv[1] #提供一个目录路径名
for file_path in glob.glob(os.path.join(filepath,"*.txt")) 
#os.path.join()将文件夹路径下所有符合特定模式的文件名连接起来,由glob.glob()扩展生成路径列表
	with open(file_path,"r",newline="") as filereader:
		for row in filereader:
			print(row.strip())

************************CSV文件处理**********************************
============读写CSV文件===================
---基础python---
import sys
input_file = sys.argv[1] 
output_file = sys.argv[2] 
with open(input_file, 'r', newline='') as filereader:
	with open(output_file, 'w', newline='') as filewriter:
		header = filereader.readline()
		header = header.strip()
		header_list = header.split(',')
		print(header_list)
		filewriter.write(','.join(map(str,header_list))+'\n')
		for row in filereader:
			row = row.strip()
			row_list = row.split(',')
			print(row_list)
			filewriter.write(','.join(map(str,row_list))+'\n')
---基础python(csv模块)---
import csv
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
with open(input_file, 'r', newline='') as csv_in_file:
	with open(output_file, 'w', newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file, delimiter=',') #创建了一个文件读取对象
		filewriter = csv.writer(csv_out_file, delimiter=',')#创建了一个文件写入对象
		for row_list in filereader:
			filewriter.writerow(row_list) #写入行至输出文件

---pandas---
import sys
import pandas as pd
input_file = sys.argv[1]
output_file = sys.argv[2]
data_frame = pd.read_csv(input_file)
print(data_frame)
data_frame.to_csv(output_file, index=False)

====================筛选特定的行==================
#行中的值满足某个条件
---基础python---
import csv,sys
input_file = sys.argv[1] #输入文件的路径名
output_file = sys.argv[2] #输出文件的路径名
with open(input_file,"r",newline = " ") as csv_in_file: 
#newline=""显示illegal newline value？去掉可行,下同。
	with open(output_file,"w",newline = " ") as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter =csv.writer(csv_out_file)
		header = next(filereader) #读取输入文件的第一行
		filewriter.writerow(header)
		for row_list in filereader:
			supplier = str(row_list[0]).strip()
			cost = str(row_list[3]).strip("$").replace(",", " ")
			if supplier=="Supplier Z" or float(cost)>600.0:
				filewriter.writerow(row_list)

---pandas---
import pandas as pd
import sys
input_file = sys.argv[1] 
output_file = sys.argv[2] 
data_frame = pd.read_csv(input_file)
data_frame["Cost"] = data_frame["Cost"].str.strip("$").astype(float)
data_frame_value_meets_conditon = data_frame.loc\
[(data_frame["Supplier Name"].str.contains("Z")) | (data_frame["Cost"]>600.0),:]
data_frame_value_meets_conditon.to_csv(output_file,index = False)

#行中的值属于某个集合
---基础python---	
import csv,sys
input_file = sys.argv[1] 
output_file = sys.argv[2]
important_dates = ["1/20/14","1/30/14"]
with open(input_file,"r",newline = " ") as csv_in_file: 
	with open(output_file,"w",newline = " ") as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter =csv.writer(csv_out_file)
		header = next(filereader) 
		filewriter.writerow(header)
		for row_list in filereader:
			if row_list[4] in important_dates:
				filewriter.writerow(row_list)
---pandas---
import pandas as pd
import sys
input_file = sys.argv[1] 
output_file = sys.argv[2] 
data_frame = pd.read_csv(input_file)
important_dates = ["1/20/14","1/30/14"]
data_frame_value_in_set = data_frame.loc\
[data_frame["Purchase Date"].isin(important_dates),:]
data_frame_value_in_set.to_csv(output_file,index = False)

#行中的值按模式匹配
---基础python---
import csv,sys,re
input_file = sys.argv[1] 
output_file = sys.argv[2]
pattern = re.compile(r"(?P<my_pattern_group>^001-.*)",re.I)
with open(input_file,"r",newline = " ") as csv_in_file: 
	with open(output_file,"w",newline = " ") as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter =csv.writer(csv_out_file)
		header = next(filereader) 
		filewriter.writerow(header)
		for row_list in filereader:
			invoice_number = row_list[1]
			if pattern.search(invoice_number)
				filewriter.writerow(row_list)
---pandas---
import pandas as pd
import sys
input_file = sys.argv[1] 
output_file = sys.argv[2] 
data_frame = pd.read_csv(input_file)
data_frame_value_matches_pattern = data_frame.loc\
[data_frame["Invoice Number"].str.startwith("001-"),:]
data_frame_value_matches_pattern.to_csv(output_file,index = False)

==========选取特定的列=======
#根据索引值选取
---基础python---
import csv,sys
input_file = sys.argv[1] 
output_file = sys.argv[2]
my_columns = [0,3] #创建索引
with open(input_file,"r",newline = " ") as csv_in_file: 
	with open(output_file,"w",newline = " ") as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter =csv.writer(csv_out_file)
		for row_list in filereader:
			row_list_output = [ ]
			for index_value in my_columns:
				row_list_output.append(row_list[index_value])
			filewriter.writerow(row_list_output)
---pandas---
import pandas as pd
import sys
input_file = sys.argv[1] 
output_file = sys.argv[2] 
data_frame = pd.read_csv(input_file)
data_frame_column_by _index = data_frame.iloc[:,[0,3]]
data_frame_column_by_index.to_csv(output_file,index =False)

#根据列标题选取
---基础python---
import csv,sys
input_file = sys.argv[1] 
output_file = sys.argv[2]
my_columns = ["Invoice Number","Purchase Date"] #创建要选取的标题
my_columns_index =[ ]
with open(input_file,"r",newline = " ") as csv_in_file: 
	with open(output_file,"w",newline = " ") as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter =csv.writer(csv_out_file)
		header = next(filereader)
		for index_value in range(len(header)):
			if header[index_value] in my_columns:
				my_columns_index.append(index_value)
		filewriter.writerow(my_columns)
		for row_list in filereader:
			row_list_output = [ ]
			for index_value in my_columns_index:
				row_list_output.append(row_list[index_value])
			filewriter.writerow(row_list_output)
---pandas---
import pandas as pd
import sys
input_file = sys.argv[1] 
output_file = sys.argv[2] 
data_frame = pd.read_csv(input_file)
data_frame_column_by _name = data_frame.loc[:,["Invoice Number","Purchase Date"]]
data_frame_column_by_name.to_csv(output_file,index = False)

============选取连续的行=====================
---基础python---
import csv,sys
input_file = sys.argv[1] 
output_file = sys.argv[2]
row_counter = 0
with open(input_file,"r",newline = " ") as csv_in_file: 
	with open(output_file,"w",newline = " ") as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter =csv.writer(csv_out_file)
		for row in filereader:
			if row_counter>=3 and row_counter<=15:
				filewriter.writerow([value.strip() for value in row])
			row_counter += 1

---pandas---
import pandas as pd
import sys
input_file = sys.argv[1] 
output_file = sys.argv[2] 
data_frame = pd.read_csv(input_file,header = None)
data_frame = data_frame.drop([0,1,2,16,17,18])
data_frame.columns = data_frame.iloc[0] #根据行索引选取一个单独行作为列索引？？？
data_frame = data_frame.reindex(data_frame.index.drop(3)) #重新生成索引？？？
data_frame.to_csv(output_file,index = False)

=================添加标题行===============
---基础python---
import csv,sys
input_file = sys.argv[1]
output_file = sys.argv[2]
with open(input_file,"r",newline = " ") as csv_in_file: 
	with open(output_file,"w",newline = " ") as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter =csv.writer(csv_out_file)
		header_list = ["Supplier Name","Invoice Number",\
		               "Part Number","Cost","Purchase Date"]
		filewriter.writerow(header_list)
		for row in filereader:
			filewriter.writerow(row)
---pandas---
import pandas as pd
import sys
input_file = sys.argv[1] 
output_file = sys.argv[2] 
header_list = ["Supplier Name","Invoice Number",\
		               "Part Number","Cost","Purchase Date"]
data_frame = pd.read_csv(input_file,header = None,names=header_list)
data_frame.to_csv(output_file,index = False)

=========文件计数与文件中的行列计数========
import csv,sys,os,glob
input_path = sys.argv[1]
file_counter = 0
for input_file in glob.glob(os.path.jion(input_path,"sales_*")):
	row_counter = 1
	with open(input_file,"r",newline=" ") as csv_in_file:
		filereader = csv.reader(csv_in_file)
		header = next(filereader)
		for row in filereader:
			row_counter += 1
	print("%s  %f  %f"%os.path.basename(input_file),row_counter,len(header))
	file_counter += 1
print("Number of files:%s"%file_counter)

==========从多个文件中连接数据append==================
---基础python---
import csv,sys,os,glob
input_path = sys.argv[1]
output_file = sys.argv[2]
first_file = True
for input_file in glob.glob(os.path.jion(input_path,"sale_*")):
	print(os.path.basename(input_file))
	with open(input_file,"r",newline=" ") as csv_in_file:
		with open(output_file,"a",newline =" ") as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)
		if first_file: #first_file用于控制第一个文件写入标题,其他不写入标题
			for row in filereader:
				filewriter.writerow(row)
			first_file = False
		else:
			header = next(filereader) #将每个文件标题赋予一个变量,后面的处理就可以跳过标题行
			for row in filereader:
				filewriter.writerow(row)

---pandas---
import pandas as pd
import sys,os,glob
input_path = sys.argv[1]
output_file = sys.argv[2]
all_data_frames = [ ]
for file in glob.glob(os.path.jion(input_path,"sales_*")):
	data_frame =pd.read_csv(file,index_col=None)
	all_data_frames.append(data_frame)
data_frame_concat = pd.concat(all_data_frames,axis = 0,ignore_index=True)
#concat()函数可以使用参数axis设置连接数据框的方式,axis=0表示垂直堆叠,axis=1表示平行堆叠
data_frame_concat.to_csv(output_file,index =False)

---其他连接函数:
pd.merge(dataframe1,dataframe2,on="key",how="inner")
#垂直连接
np.concatenate([array1,array2],axis=0) 
np.vstack((array1,array2))
np.r_[array1,array2]
#水平连接
np.concatenate([array1,array2],axis=1) 
np.hstack((array1,array2))
np.c_[array1,array2]

============计算每个文件中值的总和与均值============
---基础python---
import csv,os,sys,glob
input_path = sys.argv[1]
output_file = sys.argv[2]
output_header_list=["file_name","total_sales","average_sales"]
csv_out_file = open(output_file,"a",newline =" ")
filewriter = csv.writer(csv_out_file)
filewriter.writerow(output_header_list)
for input_file in glob.glob(os.path.jion(input_path,"sales_*")):
	with open(input_file,"r",newline=" ") as csv_in_file:
		filereader=csv.reader(csv_in_file)
		output_file_list =[ ]
		output_file_list.append(os.path.basename(input_file))
		header = next(filereader)
		total_sales =0.0
		number_of_sales =0.0
		for row in filereader:
			sale_amount = row[3]
			total_sales+=float(str(sale_amount).strip("$").replace(",",""))
			number_of_sales +=1
		average_sales = "{0:.2f}".format(total_sales/number_of_sales)
		output_file_list.append(total_sales)
		output_file_list.append(average_sales)
		filewriter.writerow(output_file_list)
csv_out_file.close()

---pandas---
import pandas as pd
import os,sys,glob
input_path = sys.argv[1]
output_file = sys.argv[2]
all_data_frames = [ ]
for input_file in glob.glob(os.path.jion(input_path,"sales_*")):
	data_frame =pd.read_csv(input_file,index_col=None)
	total_sales =pd.DataFrame([float(str(value).strip("$").replace(",", ""))\
	                     for value in data_frame.loc[:,"Sale Amount"]]).sum()
	average_sales =pd.DataFrame([float(str(value).strip("$").replace(",", ""))\
		                 for value in data_frame.loc[:,"Sale Amount"]]).mean()
	data = {"file_name":os.path.basename(input_file),
			"total_sales":total_sales,
			"average_cost":average_sales} 
	all_data_frames.append(pd.DataFrame(data,columns=["file_name","total_sales","average_sales"]))
data_frame_concat = pd.concat(all_data_frames,axis=0,ignore_index=True)
data_frame_concat.to_csv(output_file,index=False)
#pd.DataFrame(data,columns=[]),data可以是字典、列表

************************exel文件处理**********************************
#xlrd--exel read
#xlwt--exel write
import sys
from xlrd import open_workbook
input_file = sys.argv[1]
workbook = open_workbook(input_file)
print("Number of worksheets:",workbook.nsheets)
for worksheet in workbook.sheets():
	print("Worksheet name:",worksheet.name,"\tRows:",worksheet.nrows,"\tColumns:",worksheet.ncols)

open_workbook().nsheets
open_workbook().sheets()
open_workbook().sheets().name
open_workbook().sheets().nrows
open_workbook().sheets().ncols

=======读写excel文件========
---基础python---
import sys
from datetime import date 
form xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1]
output_file = sys.argv[2]
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet("jan_2013_output")
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name("january_2013")
	for row_index in range(worksheet.nrows):
		row_list_output = [ ]
		for col_index in range(worksheet.ncols)
			if worksheet.cell_type(row_index,col_index)==3:
				date_cell = xldate_as_tuple(worksheet.cell_value(row_index,col_index),workbook.datemode)
				date_cell = date(*date_cell[0:3]).strftime("%m/%d/%Y")		
				row_list_output.append(date_cell)
				output_worksheet.write(row_index,col_index,date_cell)
			else:
				non_date_cell = worksheet.cell_value(row_index,col_index)
				row_list_output.append(non_date_cell)
				output_worksheet.write(row_index,col_index,non_date_cell)
output_workbook.save(output_file)

xldate_as_tuple(cell_value,workbook.datemode) 
#可以将excel代表时间日期的数值转换为元组,单元格的值会被转化为元组中的代表日期的浮点数
#参数workbook.datemode是必需的，使函数确定日期是基于1990年还是1904年,并将数值转换为正确的元组
Workbook().add_sheet("sheetname") #在输出工作簿中创建工作表
Workbook().add_sheet("sheetname").write(row_index,col_index,data)
Workbook().save(filename)
worksheet = open_workbook().sheet_by_name("sheetname")#按名称读取工作簿中的工作表
			open_workbook().sheet_by_index(sheetx) #按索引号读取工作簿中的工作表
worksheet.cell_type(row_index,col_index) #单元格类型,"==3"表示单元格包含日期数据
worksheet.cell_value(row_index,col_index) #单元格的值

---pandas---
import pandas as pd
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
data_frame = pd.read_excel(input_file,sheetname = "january_2013")
writer = pd.ExcelWriter(output_file)
data_frame.to_excel(writer,sheet_name = "jan_2013_output",index = False)
writer.save()

pd.read_excel(path,sheetname) #读取文件
pd.ExcelWriter(path) #创建文件输出对象
pd.read_excel(path,sheetname).to_excel(输出对象,sheet_name)
pd.ExcelWriter(path).save() #输出excel文件后保存输出对象

=============筛选特定的行===========
#行中的值满足某个条件
---基础python---
import sys
from datetime import date 
form xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1]
output_file = sys.argv[2]
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet("jan_2013_output")
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name("january_2013")
	data = [ ]
	header = worksheet.row_values(0) #读取标题行
	data.append(header)
	for row_index in range(1,worksheet.nrows):
		row_list = [ ]
		sale_amount = worksheet.cell_value(row_index,3)
		if sale_amount>1400.0:
			for col_index in range(worksheet.ncols)
				cell_value =worksheet.cell_value(row_index,col_index)
				if worksheet.cell_type(row_index,col_index)==3:
					date_cell = xldate_as_tuple(cell_value,workbook.datemode)
					date_cell = date(*date_cell[0:3]).strftime("%m/%d/%Y")		
					row_list.append(date_cell)
				else:
					row_list.append(cell_value)
		if row_list: #判断row_list是否为空,只讲非空列表添加到data中。
			data.append(row_list) #将保留的行追加到data中可以得到新的连续行索引值,否则会出现缺口
	for list_index,output_list in enumerate(data): #？？？
		for element_index,element in enumerate(output_list): #？？？
			output_worksheet.write(list_index,element_index,element)			
output_workbook.save(output_file)

---pandas---
import pandas as pd
import sys
input_file = sys.argv[1]
output_file =sys.argv[2]
data_frame =pd.read_excel(input_file,"january_2013",index_col=None)
data_frame_value_meets_conditon = data_frame[data_frame["Sale Amount"].astype(float)>1400.0]
writer = pd.ExcelWriter(output_fileparam)
data_frame_value_meets_conditon.to_excel(writer,sheetname="jan_2013_output",index=False)
writer.save()

#行中的值属于某个集合
---基础python---
import sys
from datetime import date
from xlrd import open_workbook, xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1]
output_file = sys.argv[2]
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')
important_dates = ['01/24/2013', '01/31/2013']
purchase_date_column_index = 4
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	data = []
	header = worksheet.row_values(0)
	data.append(header)
	for row_index in range(1, worksheet.nrows):		
		purchase_datetime = xldate_as_tuple(worksheet.cell_value(row_index, purchase_date_column_index),workbook.datemode)
		purchase_date = date(*purchase_datetime[0:3]).strftime('%m/%d/%Y')
		row_list = []
		if purchase_date in important_dates:
			for column_index in range(worksheet.ncols):
				cell_value = worksheet.cell_value(row_index,column_index)
				cell_type = worksheet.cell_type(row_index, column_index)
				if cell_type == 3:
					date_cell = xldate_as_tuple(cell_value,workbook.datemode)
					date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
					row_list.append(date_cell)
				else:
					row_list.append(cell_value)
		if row_list:
			data.append(row_list)
	for list_index, output_list in enumerate(data):
		for element_index, element in enumerate(output_list):
			output_worksheet.write(list_index, element_index, element)
output_workbook.save(output_file)

---pandas---
import pandas as pd
import sys
input_file = sys.argv[1]
output_file =sys.argv[2]
data_frame =pd.read_excel(input_file,"january_2013",index_col=None)
important_dates = ["01/24/2013","01/31/2013"]
data_frame_value_in_set = data_frame[data_frame["Purchase Date"].isin(important_dates)]
writer = pd.ExcelWriter(output_file)
data_frame_value_in_set.to_excel(writer,sheet_name="jan_2013_output",index=False)
writer.save()

#行中的值匹配特定模式
---基础python---
import re
import sys
from datetime import date
from xlrd import open_workbook, xldate_as_tuple
from xlwt import Workbook

input_file = sys.argv[1]
output_file = sys.argv[2]
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')

pattern = re.compile(r'(?P<my_pattern>^J.*)')
customer_name_column_index = 1

with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	data = []
	header = worksheet.row_values(0)
	data.append(header)
	for row_index in range(1, worksheet.nrows):		
		row_list = []
		if pattern.search(worksheet.cell_value(row_index, customer_name_column_index)):
			for column_index in range(worksheet.ncols):
				cell_value = worksheet.cell_value(row_index,column_index)
				cell_type = worksheet.cell_type(row_index, column_index)
				if cell_type == 3:
					date_cell = xldate_as_tuple(cell_value,workbook.datemode)
					date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
					row_list.append(date_cell)
				else:
					row_list.append(cell_value)
		if row_list:
			data.append(row_list)
	
	for list_index, output_list in enumerate(data):
		for element_index, element in enumerate(output_list):
			output_worksheet.write(list_index, element_index, element)

output_workbook.save(output_file)

---pandas---
import pandas as pd
import sys
input_file = sys.argv[1]
output_file =sys.argv[2]
data_frame =pd.read_excel(input_file,"january_2013",index_col=None)
data_frame_value_matches_pattern = data_frame[data_frame["Customer Name"].str.startwith("J")]
writer = pd.ExcelWriter(output_file)
data_frame_value_matches_pattern.to_excel(writer,sheet_name="jan_2013_output",index=False)
writer.save()

=========选取特定的列===========
#列索引值
---基础python---
import sys
from datetime import date
from xlrd import open_workbook, xldate_as_tuple
from xlwt import Workbook

input_file = sys.argv[1]
output_file = sys.argv[2]

output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')

my_columns = [1, 4]

with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	data = []
	for row_index in range(worksheet.nrows):
		row_list = []
		for column_index in my_columns:
			cell_value = worksheet.cell_value(row_index,column_index)
			cell_type = worksheet.cell_type(row_index, column_index)
			if cell_type == 3:
				date_cell = xldate_as_tuple(cell_value,workbook.datemode)
				date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
				row_list.append(date_cell)
			else:
				row_list.append(cell_value)
		data.append(row_list)

	for list_index, output_list in enumerate(data):
		for element_index, element in enumerate(output_list):
			output_worksheet.write(list_index, element_index, element)

output_workbook.save(output_file)

---pandas---
import pandas as pd
import sys
input_file = sys.argv[1]
output_file =sys.argv[2]
data_frame =pd.read_excel(input_file,"january_2013",index_col=None)
data_frame_column_by_index = data_frame.iloc[:,[1:4]]
writer = pd.ExcelWriter(output_file)
data_frame_column_by_index.to_excel(writer,sheet_name="jan_2013_output",index=False)
writer.save()

#列标题
---基础python---
import sys
from datetime import date
from xlrd import open_workbook, xldate_as_tuple
from xlwt import Workbook

input_file = sys.argv[1]
output_file = sys.argv[2]

output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')

my_columns = ['Customer ID', 'Purchase Date']

with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	data = [my_columns]
	header_list = worksheet.row_values(0)
	header_index_list = []
	for header_index in range(len(header_list)):
		if header_list[header_index] in my_columns:
			header_index_list.append(header_index)
	for row_index in range(1,worksheet.nrows):
		row_list = []
		for column_index in header_index_list:
			cell_value = worksheet.cell_value(row_index,column_index)
			cell_type = worksheet.cell_type(row_index, column_index)
			if cell_type == 3:
				date_cell = xldate_as_tuple(cell_value,workbook.datemode)
				date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
				row_list.append(date_cell)
			else:
				row_list.append(cell_value)
		data.append(row_list)

	for list_index, output_list in enumerate(data):
		for element_index, element in enumerate(output_list):
			output_worksheet.write(list_index, element_index, element)

output_workbook.save(output_file)

---pandas---
import pandas as pd
import sys
input_file = sys.argv[1]
output_file =sys.argv[2]
data_frame =pd.read_excel(input_file,"january_2013",index_col=None)
data_frame_column_by_name = data_frame.loc[:,["Customer ID","Purchase Date"]
writer = pd.ExcelWriter(output_file)
data_frame_column_by_name.to_excel(writer,sheet_name="jan_2013_output",index=False)
writer.save()

============处理多个工作表==============
#筛选特定行(所有工作表)
---基础python---
import sys
from datetime import date
from xlrd import open_workbook, xldate_as_tuple
from xlwt import Workbook

input_file = sys.argv[1]
output_file = sys.argv[2]

output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('filtered_rows_all_worksheets')

sales_column_index = 3
threshold = 2000.0

first_worksheet = True
with open_workbook(input_file) as workbook:
	data = []
	for worksheet in workbook.sheets():
		if first_worksheet:
			header_row = worksheet.row_values(0)
			data.append(header_row)
			first_worksheet = False
		for row_index in range(1,worksheet.nrows):
			row_list = []
			sale_amount = worksheet.cell_value(row_index, sales_column_index)
			sale_amount = float(str(sale_amount).replace('$', '').replace(',', ''))
			if sale_amount > threshold:
				for column_index in range(worksheet.ncols):
					cell_value = worksheet.cell_value(row_index,column_index)
					cell_type = worksheet.cell_type(row_index, column_index)
					if cell_type == 3:
						date_cell = xldate_as_tuple(cell_value,workbook.datemode)
						date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
						row_list.append(date_cell)
					else:
						row_list.append(cell_value)
			if row_list:
				data.append(row_list)

	for list_index, output_list in enumerate(data):
		for element_index, element in enumerate(output_list):
			output_worksheet.write(list_index, element_index, element)

output_workbook.save(output_file)

---pandas---
import pandas as pd
import sys
input_file = sys.argv[1]
output_file =sys.argv[2]
data_frame =pd.read_excel(input_file,sheet_name=None,index_col=None)
row_output = [ ]
for worksheet_name,data in data_frame.items():
	row_output.append(data[data["Sale Amount"].astype(float)>2000.0])
filtered_rows = pd.concat(row_output,axis=0,ignore_index=True)
writer = pd.ExcelWriter(output_file)
filtered_rows.to_excel(writer,sheet_name="sale_amount_gter2000",index=False)
writer.save()

pd.read_excel().items() #迭代工作表的名称和数据内容

#筛选特定列(所有工作表)
---基础python---
import sys
from datetime import date
from xlrd import open_workbook, xldate_as_tuple
from xlwt import Workbook

input_file = sys.argv[1]
output_file = sys.argv[2]

output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('selected_columns_all_worksheets')

my_columns = ['Customer Name', 'Sale Amount']
	
first_worksheet = True
with open_workbook(input_file) as workbook:
	data = [my_columns]
	index_of_cols_to_keep = []
	for worksheet in workbook.sheets():
		if first_worksheet:
			header = worksheet.row_values(0)
			for column_index in range(len(header)):
				if header[column_index] in my_columns:
					index_of_cols_to_keep.append(column_index)
			first_worksheet = False
		for row_index in range(1, worksheet.nrows):
			row_list = []
			for column_index in index_of_cols_to_keep:	
				cell_value = worksheet.cell_value(row_index, column_index)
				cell_type = worksheet.cell_type(row_index, column_index)
				if cell_type == 3:
					date_cell = xldate_as_tuple(cell_value,workbook.datemode)
					date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
					row_list.append(date_cell)
				else:
					row_list.append(cell_value)
			data.append(row_list)

	for list_index, output_list in enumerate(data):
		for element_index, element in enumerate(output_list):
			output_worksheet.write(list_index, element_index, element)

output_workbook.save(output_file)

---pandas---
import pandas as pd
import sys
input_file = sys.argv[1]
output_file =sys.argv[2]
data_frame =pd.read_excel(input_file,sheet_name=None,index_col=None) #将所有工作表读入一个字典
column_output = [ ]
for worksheet_name,data in data_frame.items():
	column_output.append(data.loc[:,["Customer Name","Sale Amount"]]) #生成数据框列表
selected_columns = pd.concat(column_output,axis=0,ignore_index=True) #将所有数据框连接为一个最终数据框
writer = pd.ExcelWriter(output_file)
selected_columns.to_excel(writer,sheet_name="selected_columns_all_worksheets",index=False)
writer.save()

#筛选行(一组或部分工作表)
---基础python---
import sys
from datetime import date
from xlrd import open_workbook, xldate_as_tuple
from xlwt import Workbook

input_file = sys.argv[1]
output_file = sys.argv[2]

output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('set_of_worksheets')

my_sheets = [0,1]
threshold = 1900.0
sales_column_index = 3

first_worksheet = True
with open_workbook(input_file) as workbook:
	data = []
	for sheet_index in range(workbook.nsheets):
		if sheet_index in my_sheets:
			worksheet = workbook.sheet_by_index(sheet_index)
			if first_worksheet:
				header_row = worksheet.row_values(0)
				data.append(header_row)
				first_worksheet = False
			for row_index in range(1,worksheet.nrows):
				row_list = []
				sale_amount = worksheet.cell_value(row_index, sales_column_index)
				if sale_amount > threshold:
					for column_index in range(worksheet.ncols):
						cell_value = worksheet.cell_value(row_index,column_index)
						cell_type = worksheet.cell_type(row_index, column_index)
						if cell_type == 3:
							date_cell = xldate_as_tuple(cell_value,workbook.datemode)
							date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
							row_list.append(date_cell)
						else:
							row_list.append(cell_value)
				if row_list:
					data.append(row_list)

	for list_index, output_list in enumerate(data):
		for element_index, element in enumerate(output_list):
			output_worksheet.write(list_index, element_index, element)

output_workbook.save(output_file)

---pandas---
import pandas as pd
import sys
input_file = sys.argv[1]
output_file =sys.argv[2]
my_sheets =[0,1]
data_frame =pd.read_excel(input_file,sheetname=my_sheets,index_col=None) #将所有工作表读入一个字典
threshold = 1900.0
row_list = [ ]
for worksheet_name,data in data_frame.items():
	row_list.append(data[data["Sale Amount"].astype(float)>threshold]) #生成数据框列表
filtered_rows = pd.concat(row_list,axis=0,ignore_index=True) #将所有数据框连接为一个最终数据框
writer = pd.ExcelWriter(output_file)
filtered_rows.to_excel(writer,sheet_name="set_of_worksheets",index=False)
writer.save()

=============处理多个工作簿=============
#工作表及行列计数(内省工作簿)
import sys,os,glob
from xlrd import open_workbook
input_path = sys.argv[1]
workbook_counter = 0
for input_file in glob.glob(os.path.join(input_path,"*.xls*")):
	workbook = open_workbook(input_file)
	print("Workbook:%s" % os.path.basename(input_file))
	print("Number of worksheets:%d" % workbook.nsheets)
	for worksheet in workbook.sheets():
		print("Worksheet name:",worksheet.name,"\tRows:",worksheet.nrows,"\tColumns:",worksheet.ncols)
	workbook_counter += 1
print("Number of Excel workbooks:%d" % workbook_counter)

#从多个工作簿中连接数据
---基础python---
import glob,os,sys 
from datetime import date
from xlrd import open_workbook, xldate_as_tuple
from xlwt import Workbook

input_folder = sys.argv[1]
output_file = sys.argv[2]

output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('all_data_all_workbooks')

data = []
first_worksheet = True
for input_file in glob.glob(os.path.join(input_folder, '*.xls*')):
	print os.path.basename(input_file)
	with open_workbook(input_file) as workbook:
		for worksheet in workbook.sheets():
			if first_worksheet:
				header_row = worksheet.row_values(0)
				data.append(header_row)
				first_worksheet = False
			for row_index in range(1,worksheet.nrows):
				row_list = []
				for column_index in range(worksheet.ncols):
					cell_value = worksheet.cell_value(row_index,column_index)
					cell_type = worksheet.cell_type(row_index, column_index)
					if cell_type == 3:
						date_cell = xldate_as_tuple(cell_value,workbook.datemode)
						date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
						row_list.append(date_cell)
					else:
						row_list.append(cell_value)
				data.append(row_list)

for list_index, output_list in enumerate(data):
	for element_index, element in enumerate(output_list):
		output_worksheet.write(list_index, element_index, element)

output_workbook.save(output_file)

---pandas---
import pandas as pd
import os,sys,glob
input_path = sys.argv[1]
output_file = sys.argv[2]
all_workbooks = glob.glob(os.path.join(input_path,"*.xls*"))
data_frames = [ ]
for workbook in all_workbooks:
	all_worksheets = pd.read_excel(workbook,sheetname=None,index_col=None)
	for worksheet_name,data in all_worksheets.items():
		data_frames.append(data)
all_data_concatenated = pd.concat(data_frames,axis=0,ignore_index=True)
writer = pd.ExcelWriter(output_file)
all_data_concatenated.to_excel(writer,sheet_name="all_data_all_workbooks",index=False)
writer.save()

=========在每个工作簿和每个工作表中计算总数和均值=========
---基础python---
import glob,os,sys
from datetime import date
from xlrd import open_workbook, xldate_as_tuple
from xlwt import Workbook

input_folder = sys.argv[1]
output_file = sys.argv[2]

output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('sums_and_averages')

all_data = []
sales_column_index = 3

header = ['workbook', 'worksheet', 'worksheet_total', 'worksheet_average',\
 					'workbook_total', 'workbook_average']
all_data.append(header)

for input_file in glob.glob(os.path.join(input_folder, '*.xls*')):
	with open_workbook(input_file) as workbook:
		list_of_totals = []
		list_of_numbers = []
		workbook_output = []
		for worksheet in workbook.sheets():
			total_sales = 0
			number_of_sales = 0
			worksheet_list = []
			worksheet_list.append(os.path.basename(input_file))
			worksheet_list.append(worksheet.name)
			for row_index in range(1,worksheet.nrows):
				try:
					total_sales += float(str(worksheet.cell_value(row_index,sales_column_index)).strip('$').replace(',',''))
					number_of_sales += 1.
				except:
					total_sales += 0.
					number_of_sales += 0.
			average_sales = '%.2f' % (total_sales / number_of_sales)
			worksheet_list.append(total_sales)
			worksheet_list.append(float(average_sales))
			list_of_totals.append(total_sales)
			list_of_numbers.append(float(number_of_sales))
			workbook_output.append(worksheet_list)
		workbook_total = sum(list_of_totals)
		workbook_average = sum(list_of_totals)/sum(list_of_numbers)
		for list_element in workbook_output:
			list_element.append(workbook_total)
			list_element.append(workbook_average)
		all_data.extend(workbook_output) #使用extend以使workbook_output中的每个列表成为一个独立元素,否则每个元素都是一个列表的列表
		
for list_index, output_list in enumerate(all_data):
	for element_index, element in enumerate(output_list):
		output_worksheet.write(list_index, element_index, element)

output_workbook.save(output_file)

---pandas---
import pandas as pd
import os,sys,glob
input_path = sys.argv[1]
output_file = sys.argv[2]
all_workbooks = glob.glob(os.path.join(input_path,"*.xls*"))
data_frames = [ ]
for workbook in all_workbooks:
	all_worksheets = pd.read_excel(workbook,sheetname=None,index_col=None)
	workbook_total_sales = [ ]
	workbook_number_of_sales =[ ]
	worksheet_data_frames = [ ]
	worksheets_data_frame =None
	workbook_data_frame = None
	for worksheet_name,data in all_worksheets.items():
		total_sales = pd.DataFrame([float(str(value).strip("$").replace(",", ""))\
			for value in data.loc[:,"Sale Amount"]]).sum()
		number_of_sales = len(data.loc[:,"Sale Amount"])
		average_sales = pd.DataFrame(total_sales/number_of_sales)

		workbook_total_sales.append(total_sales)
		workbook_number_of_sales.append(number_of_sales)

		data = dict("workbook"=os.path.basename(workbook),
				 	"worksheet"=worksheet_name,
				 	"worksheet_total"=total_sales,
				 	"worksheet_average"=average_sales)
		worksheet_data_frames.append(pd.DataFrame(data,columns=\
			["workbook","worksheet","worksheet_total","worksheet_average"]))		
	
	worksheets_data_frame = pd.concat(worksheet_data_frames,axis=0,ignore_index=True)	
	
	workbook_total = pd.DataFrame(workbook_total_sales).sum()
	workbook_total_number_of_sales = pd.DataFrame(workbook_number_of_sales).sum()
	workbook_average = pd.DataFrame(workbook_total/workbook_total_number_of_sales)
	workbook_stats = {"workbook":os.path.basename(workbook),
					"workbook_total":workbook_total,
					"workbook_average":workbook_average}
	workbook_stats = pd.DataFrame(workbook_stats,columns=["workbook","workbook_total","workbook_average"])
	workbook_data_frame = pd.merge(worksheets_data_frame,workbook_stats,on="workbook",how="left")
	data_frames.append(workbook_data_frame)
all_data_concatenated = pd.concat(data_frames,axis=0,ignore_index=True)
writer = pd.ExcelWriter(output_file)
all_data_concatenated.to_excel(writer,sheet_name="sums_and_averages",index=False)
writer.save()

==============================数据库==================================
***********数据库基本操作*************
MySQL command line:mysql; #进入数据库命令行界面 
SHOW DATABASES; #显示数据库系统中已有数据库
CREATE DATABASE dbname; #创建名为dbname的数据库
USE dbname; #使用dbname数据库

CREATE TABLE IF NOT EXISTS tablename #如果不存在tablename则创建tablename数据表
(A VARCHAR(20), #可变字符串字段
 B CHAR(20) # 固定长度字符串字段(两端对齐)
 C ENUM, #允许值(如small、medium、large)字段(分类字段???)
 D BLOB, # 长度可变大量文本字段
 E FLOAT, #浮点数字段
 F DATE, #日期字段,存储形式为"YYYY-MM-DD"
 G NUMERIC(11,2));  #数字字段,表示数位总数11,小数点后数位为2

DESCRIBE tablename; #查看数据表信息
CREATE USER "username"@"localhost" IDENTIFIED BY "password"; #为数据库创建一个新用户
GRANT ALL PRIVILEGES ON dbname.* TO "username"@"localhost";#授予用户数据库所有权限
FLUSH PRIVILEGES; #刷新权限

***********利用内置模块sqlite3创建数据库、表*************
import sqlite3

con = sqlite3.connect("E:\\Python3.6\\data_analysis_source_code\\mydatabase\\my_database.db") #创建数据库
query = '''CREATE TABLE sales
			(customer VARCHAR(20),
			product VARCHAR(40),
			amount FLOAT,
			date DATE);''' #创建SQL查询语句,意为创建一个包含四个属性的表(三对引号表示多行字符串)
con.execute(query) #执行创建表的SQL命令
con.commit() #将修改提交到数据库,当作出修改时必须使用此方法来保存修改

#接下来在表中插入数据
data = [('Richard Lucas', 'Notepad', 2.50, '2014-01-02'),
		('Jenny Kim', 'Binder', 4.15, '2014-01-15'),
		('Svetlana Crow', 'Printer', 155.75, '2014-02-03'),
		('Stephen Randolph', 'Computer', 679.40, '2014-02-20')] #元组列表,分别对应4行数据
statement = "INSERT INTO sales Values(?,?,?,?)"#SQL命令:向表中插入数据,?为占位符
con.executemany(statement,data) #执行插入数据的SQL命令,数据自动赋予占位符?
con.commit()

#查询sales表
cursor = con.execute("SELECT * FROM sales")
rows = cursor.fetchall() #返回rows元组列表(即data对象);fetchone/fetchmany/fetchall

#计算查询结果中行的数量
row_counter = 0
for row in rows:
	print(row)
	row_counter += 1
print("Number of rows:%d" % row_counter)
con.close()

#加载CSV文件中的数据------------
import csv,sqlite3,sys
con = sqlite3.connect("E:\\Python3.6\\data_analysis_source_code\\mydatabase\\my_database.db") #创建数据库连接
c = con.cursor() #创建游标,游标比数据库连接对象(con)支持更多的方法
create_table = """CREATE TABLE IF NOT EXISTS Suppliers
				(Supplier_Name VARCHAR(20),
				Invoice_Number VARCHAR(20),
				Part_Number VARCHAR(20),
				Cost FLOAT,
				Purchase_Date DATE);"""
c.execute(create_table)
con.commit()

input_file = open("E:\\Python3.6\\data_analysis_source_code\\mydatabase\\supplier_data.csv","r")
file_reader = csv.reader(input_file,delimiter=",")
header = next(file_reader,None) #去标题(不要None结果一样)
for row in file_reader:
	data = [ ]
	for col_index in range(len(header)):
		data.append(row[col_index])
		print(data)
	c.execute("INSERT INTO Suppliers VALUES(?,?,?,?,?);",data) 
con.commit()

#查询Suppliers表
output = c.execute("SELECT*FROM Suppliers")
rows = output.fetchall() #rows元组列表
for row in rows:
	output = [ ]
	for col_index in range(len(row)):
		output.append(str(row[col_index]))
	print(output)

#更新数据库中表的记录------------
input_file = sys.argv[1]
con = sqlite3.connect(':memory:') #在内存中创建数据库
query = """CREATE TABLE IF NOT EXISTS sales
			(customer VARCHAR(20), 
				product VARCHAR(40),
				amount FLOAT,
				date DATE);"""
con.execute(query)
con.commit()

# Insert a few rows of data into the table
data = [('Richard Lucas', 'Notepad', 2.50, '2014-01-02'),
		('Jenny Kim', 'Binder', 4.15, '2014-01-15'),
		('Svetlana Crow', 'Printer', 155.75, '2014-02-03'),
		('Stephen Randolph', 'Computer', 679.40, '2014-02-20')]
for tuple in data:
	print(tuple)
statement = "INSERT INTO sales VALUES(?, ?, ?, ?)"
con.executemany(statement, data)
con.commit()
	
# Read the CSV file and update the specific rows
file_reader = csv.reader(open(input_file, 'r'), delimiter=',')
header = next(file_reader, None)
for row in file_reader:
	data = []
	for column_index in range(len(header)):
		data.append(row[column_index])
	print(data)
	con.execute("UPDATE sales SET amount=?, date=? WHERE customer=?;", data)
	#注意：读取的CSV文件中变量顺序要与UPDATE中amount,date,customer一致
con.commit()

# Query the sales table
cursor = con.execute("SELECT * FROM sales")
rows = cursor.fetchall()
for row in rows:
	output = []
	for column_index in range(len(row)):
		output.append(str(row[column_index]))
	print(output)

************利用MySQLdb模块与mysql进行交互*****************
import csv,sys,MySQLdb
from datetime import datetime,date

input_file = sys.argv[1]
con = MySQLdb.connect(host="localhost",port=3306,db="my_suppliers",user="root",password="jge520")
c = con.cursor()

file_reader = csv.reader(open(input_file,"r",newline=""))
header = next(filereader)
for row in file_reader:
	data=[ ]
	for col_index in range(len(header)):
		if col_index < 4:
			data.append(str(row[col_index]).lstrip("$").replace(",","").strip())
		else:
			a_date = datetime.date(datetime.strptime(str(row[col_index]),"%m/%d/%Y")).strftime("%Y-%m-%d")
			data.append(a_date)
	c.execute("INSERT INTO Suppliers VALUES(%s,%s,%s,%s,%s);",data)
con.commit()
#查询
c.execute("SELECT*FROM Suppliers")
rows = c.fetchall()
for row in rows:
	row_list_output = [ ]
	for col_index in range(len(row)):
		row_list_output.append(str(row[col_index]))
	print(row_list_output)
con.close()
#查询表中记录并写入CSV文件--------
output_file = sys.argv[1]
con = MySQLdb.connect(host="localhost",port=3306,db="my_suppliers",user="root",password="jge520")
c = con.cursor()
filewriter = csv.writer(open(output_file,"w",newline=""),delimiter=",")
header = ['Supplier Name','Invoice Number','Part Number','Cost','Purchase Date']
filewriter.writerow(header)
c.execute("SELECT*FROM Suppliers WHERE Cost>700.0;")
rows = c.fetchall()
for row in rows:
	filewriter.writerow(row)
con.close()
#更新表中记录---------
input_file = sys.argv[1]
con = MySQLdb.connect(host="localhost",port=3306,db="my_suppliers",user="root",password="jge520")
c = con.cursor()

file_reader = csv.reader(open(input_file,"r",newline=""),delimiter=",")
header = next(filereader)
for row in file_reader:
	data=[ ]
	for col_index in range(len(header)):
			data.append(str(row[col_index]).strip())
	c.execute("UPDATE Suppliers SET Cost=%s,Purchase_Date=%s WHERE Supplier_Name=%s;",data)
con.commit()
#查询
c.execute("SELECT*FROM Suppliers")
rows = c.fetchall()
for row in rows:
	output = [ ]
	for col_index in range(len(row)):
		output.append(str(row[col_index]))
	print(output)
con.close()

=============================应用程序=================================

********根据CSV文件中的数值序列在一大堆文件中查找*(查找历史记录)**********
import csv,sys,os,glob
from datetime import date 
from xlrd import open_workbook,xldate_as_tuple

item_numbers_file = sys.argv[1] #搜索依据,及需要搜索数值序列CSV文件路径
path_to_folder = sys.argv[2] #搜索的目标文件夹路径
output_file = sys.argv[3] #输出文件路径

item_numbers_to_find = [ ]
with open(item_numbers_file,"r",newline="") as item_numbers_csv_file:
	filereader = csv.reader(item_numbers_csv_file)
	for row in filereader:
		item_numbers_to_find.append(row[0]) #row[0]表示第一列

filewriter = csv.writer(open(output_file,"a",newline=""))
file_counter = 0
line_counter = 0
count_of_item_numbers = 0
for input_file in glob.glob(os.path.join(path_to_folder,"*.*")):
	file_counter += 1
	if input_file.split(".")[1] == "csv":
		with open(input_file,"r",newline="") as csv_in_file:
			filereader = csv.reader(csv_in_file)
			header = next(filereader)
			for row in filereader:
				row_of_output =[ ]
				for column in range(len(header)):
					if column == 3: ####
						cell_value = str(row[column]).lstrip("$").replace(",","").strip()
						row_of_output.append(cell_value)
					else: ####这里if和else仅仅是在将CSV文件内容读入row_of_output
						cell_value = str(row[column]).strip()
						row_of_output.append(cell_value)
				row_of_output.append(os.path.basename(input_file))
				if row[0] in item_numbers_to_find:
					filewriter.writerow(row_of_output)
					count_of_item_numbers += 1
				line_counter += 1
	elif input_file.split(".")[1] == "xls" or "xlsx":
		workbook = open_workbook(input_file)
		for worksheet in workbook.sheets():
			try:
				header = worksheet.row_values(0)
			except IndexError:
				pass
			for row in range(1,worksheet.nrows):
				row_of_output = [ ]
				for column in range(len(header)):
					if worksheet.cell_type(row,column) == 3:
						cell_value=xldate_as_tuple(worksheet.cell(row,column).value,datemode)
						cell_value=str(date(*cell_value[0,3])).strip()
						row_of_output.append(cell_value)
					else:
						cell_value=str(worksheet.cell_value(row,column)).strip()
						row_of_output.append(cell_value)
				row_of_output.append(os.path.basename(input_file))
				row_of_output.append(worksheet.name)
				if str(worksheet.cell_value(row,0)).split(".")[0].strip() in item_numbers_to_find:
					filewriter.writerow(row_of_output)
					count_of_item_numbers += 1
				line_counter += 1
print("Number of files:",file_counter)
print("Number of lines:",line_counter)
print("Number of item numbers:",count_of_item_numbers)

*******为CSV文件分类计算统计量*(嵌套字典、计算时间间隔)********
import csv,sys
from datetime import date,datetime

def date_diff(date1,date2):
	try:
		diff = str(datetime.strptime(date1,"%m/%d/%Y")-datetime.strptime(date2,"%m/%d/%Y")).split()[0]
	except:
		diff = 0
	if diff == "0:00:00":
		diff = 0
	return diff
input_file = sys.argv[1]
output_file = sys.argv[2]
packages = { }

previous_name = "N/A"
previous_package = "N/A"
previous_package_date = "N/A"
first_row = True
today = date.today().strftime("%m/%d/%Y")
with open(input_file,"r",newline="") as input_csv_file:
	filereader = csv.reader(input_csv_file)
	header = next(filereader)
	for row in filereader:
		current_name = row[0]
		current_package = row[1]
		current_package_date = row[3]
		if current_name not in packages:
			packages[current_name] = { }
		if current_package not in packages[current_name]:
			packages[current_name][current_package] = 0
		if current_name != previous_name:
			if first_row:
				first_row = False
			else:
				diff = date_diff(today,previous_package_date)
				if previous_package not in packages[previous_name]:
					packages[previous_name][previous_package] = int(diff)
				else:
					packages[previous_name][previous_package] += int(diff)
		else:
			diff = date_diff(current_package_date,previous_package_date)
			packages[previous_name][previous_package] += int(diff)
		previous_name = current_name
		previous_package = current_package
		previous_package_date = current_package_date
header = ["Customer Name","Category","Total Time (in Days)"]
with open(output_file,"w",newline="") as output_csv_file:
	filewriter=csv.writer(output_csv_file)
	filewriter.writerow(header)
	for customer_name,customer_name_value in packages.items():
		for package_category,package_category_value in packages[customer_name].items():
			row_of_output = [ ]
			print(customer_name,package_category,package_category_value)
			row_of_output.append(customer_name)
			row_of_output.append(package_category)
			row_of_output.append(package_category_value)
			filewriter.writerow(row_of_output)

***********处理纯文本文件txt**********
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
messages = { }
notes = [ ]
with open(input_file,"r",newline="") as text_file:
	for fow in text_file:
		if "[Note]" in row:
			row_list = row.split(" ",4)
			day = row_list[0].strip()
			note = row_list[4].strip("\n").strip()
			if note not in notes:
				notes.append(note)
			if day not in messages:
				messages[day]={ }
			if note not in messages[day]:
				messages[day][note] = 1
			else:
				messages[day][note] += 1
filewriter = open(output_file,"w",newline="")
header = ["Date"]
header.extend(notes)
header = ",".join(map(str,header)) + "\n" #map函数在header中的每个元素上应用str()函数
print(header)
filewriter.write(header)
for day,day_value in messages.items():
	row_of_output = [ ]
	row_of_output.append(day)
	for index in range(len(notes)):
		if notes[index] in day_value.keys():
			row_of_output.append(day_value[notes[index]])
		else:
			row_of_output.append(0)
	output = ",".join(map(str,row_of_output)) + "\n" ###
	print(output)
	filewriter.write(output)
filewriter.close()

=============================图与图表=================================

#matplotlib,扩展工具箱basemap、cartopy用于制作地图，mplot3D用于3D绘图
***********************matplotlib.pyplot*********************
---条形图bar_plot---

import matplotlib.pyplot as plt #惯常的import语句
plt.style.use("ggplot") #使用ggplot2风格的图形

customers = ["ABC","DEF","GHI","JKL","MNO"]
customers_index = range(len(customers))
sale_amounts = [127,90,201,111,232]

fig = plt.figure() #matplotlib绘图首先要创建一个基础图,然后在基础图中创建一个或多个子图
ax1 = fig.add_subplot(1,1,1) #创建一个一行一列并使用第一个的子图
ax1.bar(customers_index,sale_amounts,align="center",color="darkblue") 
#创建条形图bar(x,y,align,color),align="center"设置条形图与标签中间对齐

ax1.xaxis.set_ticks_position("bottom")#设置X轴刻度的位置在底部
ax1.yaxis.set_ticks_position("left") #设置Y轴刻度的位置在左侧

plt.xticks(customers_index,customers,rotation=0,fontsize="small")
#将刻度线标签由客户索引值更改为客户名称,rotation=0表示刻度标签水平无倾斜角度
plt.xlabel("Customer Name")
plt.ylabel("Sale Amount")
plt.title("Sale Amount per Customer")

plt.savefig("bar_plot.png",dpi=400,bbox_inches="tight")#bbox_inches表示将图形四周的空白部分去掉
plt.show()#表示在一个新窗口中显示

---直方图histogram---

import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")

mu1,mu2,sigma = 100,130,15
x1 = mu1 + sigma*np.random.randn (10000)
x2 = mu2 + sigma*np.random.randn(10000)
#np.random.randn()返回标准正态分布数组,同random.standard_normal()
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
n,bins,patches = ax1.hist(x1,bins=50,normed=False,color="darkgreen")
n,bins,patches = ax1.hist(x2,bins=50,normed=False,color="orange",alpha=0.5)
#bins=50表示每个变量的值分成50份,normed=False表示频率分布图而不是概率密度
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
plt.xlabel("Bins")
plt.ylabel("Number of Values in Bin")
fig.suptitle("Histograms",fontsize=14,fontweight="bold") #为基础图添加一个居中的标题
ax1.set_title("Two Frequency Distributions") #为子图添加一个居中标题
plt.savefig("Histogram.png",dpi=400,bbox_inches="tight")
plt.show()

---折线图line_plot---

from numpy.random import randn
import matplotlib.pyplot as plt

plot_data1 = randn(50).cumsum()
plot_data2 = randn(50).cumsum()
plot_data3 = randn(50).cumsum()
plot_data4 = randn(50).cumsum()

plt.style.use("ggplot")
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(plot_data1,marker=r"o",color=u"blue",linestyle="-",label="Blue Solid")
ax1.plot(plot_data2,marker=r"+",color=u"red",linestyle="--",label="Red Dashed")
ax1.plot(plot_data3,marker=r"*",color=u"green",linestyle="-.",label="Green Dash Dot")
ax1.plot(plot_data4,marker=r"s",color=u"orange",linestyle=":",label="Orange Dotted")
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
ax1.set_title("Line plots:Markers,Colors,and linestyles")
plt.xlabel("Draw")
plt.ylabel("Random Number")
plt.legend(loc="best") #loc="best"根据图中空白把图例放在最合适的位置
plt.savefig("line_plot.png",dpi=1500,bbox_inches="tight")
plt.show()

---散点图scatter_plot---

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(1,15,1) #stat=1,stop=15,step=1,返回数组
y_linear = x+5*np.random.randn(14) 
y_quadratic = x**2+10*np.random.randn(14) 
fn_linear = np.poly1d(np.polyfit(x, y_linear, deg=1))
'''
[1] np.poly1d(c_or_r,r=False)返回一维多项式(方程),例如p=np.poly1d((2,2,2,3))返回：
	2 x**3 + 2 x**2 + 2 x + 3 = 0
	若r=True,则(2,2,2,3)为根,p.c查看系数,p.r查看根,p(num)方程等于num. 
[2] np.polyfit()返回线性拟合的系数,degree为拟合程度
'''
fn_quadratic = np.poly1d(np.polyfit(x, y_quadratic, deg=2))

plt.style.use("ggplot")
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(x,y_linear,"bo", #"bo"蓝色圆圈
		x,y_quadratic,"go", #"go"绿色圆圈,下类似. 
		x,fn_linear(x),"b-",
		x,fn_quadratic(x),"g-",linewidth=2) 
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
ax1.set_title("Scatter Plots Regression Lines")
plt.xlabel("x")
plt.ylabel("f(x)",rotation=90)
plt.xlim(min(x)-1,max(x)+1) #设置X轴的范围
plt.ylim(min(y_quadratic)-10,max(y_quadratic)+10)
plt.savefig("scatter_plot.png",dpi=400,bbox_inches="tight")
plt.show()

---箱线图box_plot---

import numpy as np
import matplotlib.pyplot as plt

N=500
normal = np.random.normal(loc=0, scale=1, size=N)
#返回正态分布,loc为mean的位置,scale为sd的大小,size为样本数
lognormal = np.random.lognormal(mean=0, sigma=1, size=N)#对数正态分布
index_value = np.random.random_integers(low=0, high=N-1, size=N)#创建随机索引
normal_sample = normal[index_value]
lognormal_sample = lognormal[index_value]
box_plot_data = [normal,normal_sample,lognormal,lognormal_sample]

plt.style.use("ggplot")
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
box_labels = ["normal","normal_sample","lognormal","lognormal_sample"]
ax1.boxplot(box_plot_data,notch=False,sym=".",vert=True,whis=1.5,showmeans=True,labels=box_labels)
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
ax1.set_title("Box Plots") #plt.title()
ax1.set_xlabel("Distribution") #plt.xlabel()
ax1.set_ylabel("Value",rotation=90) #plt.ylabel()
plt.savefig("box_plot.png",dpi=400,bbox_inches="tight")
plt.show()

***********************pandas*********************
#向统计图中添加第二Y轴,误差棒和数据表,plot函数默认折线图,可通过kind创建其他图形
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_frame = pd.DataFrame (np.random.rand(5,3),#np.random.rand(5,3)为5行3列随机数组
			index=["Customer 1","Customer 2","Customer 3","Customer 4","Customer 5"],
			columns=pd.Index(["Metric 1","Metric 2","Metric 3"],name="Metrics")) 
#pd.DataFrame(data,index,columns,name):
#  name  columns1 columns2 columns3
# index1   data     data     data 
# index2   data     data     data 
# index3   data     data     data 
plt.style.use("ggplot")
fig,axes = plt.subplots(nrows=1,ncols=2) #创建一个基础图和一行两列的子图
ax1,ax2 = axes.ravel() #将子图分别赋予ax1,ax2,等同于索引axes[0,0]和axes[0,1]
data_frame.plot(kind="bar",ax=ax1,alpha=0.75,title="Bar Plot")
plt.setp(ax1.get_xticklabels(),rotation=45,fontsize=10) #设置刻度标签属性
plt.setp(ax1.get_yticklabels(),rotation=0,fontsize=10)
ax1.set_xlabel("Customer")
ax1.set_ylabel("Value")
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")

colors = dict(boxes="DarkBlue",whiskers="Gray",medians="Red",caps="Black")
data_frame.plot(kind="box",color=colors,sym="r.",ax=ax2,title="Box Plot") #离群值红色圆点
plt.setp(ax2.get_xticklabels(),rotation=45,fontsize=10) #设置刻度标签属性
plt.setp(ax2.get_yticklabels(),rotation=0,fontsize=10)
ax2.set_xlabel("Metric")
ax2.set_ylabel("Value")
ax2.xaxis.set_ticks_position("bottom")
ax2.yaxis.set_ticks_position("left")

plt.savefig("pandas_plots.png",dpi=400,bbox_inches="tight")
plt.show()

***********************ggplot*********************
from ggplot import *

print(mtcars.head())
plt1 = ggplot(aes(x='mpg'), data=mtcars) +\
 		geom_histogram(fill='darkblue', binwidth=2) +\
		xlim(10, 35) + ylim(0, 10) +\
		xlab("MPG") + ylab("Frequency") +\
		ggtitle("Histogram of MPG") +\
		theme_matplotlib()
print(plt1)

print(meat.head())
plt2 = ggplot(aes(x='date', y='beef'), data=meat) +\
		geom_line(color='purple', size=1.5, alpha=0.75) +\
		stat_smooth(colour='blue', size=2.0, span=0.15) +\
		xlab("Year") + ylab("Head of Cattle Slaughtered") +\
		ggtitle("Beef Consumption Over Time") +\
		theme_seaborn()
print(plt2)

print(diamonds.head())
plt3 = ggplot(diamonds, aes(x='carat', y='price', colour='cut')) +\
		geom_point(alpha=0.5) +\
		scale_color_gradient(low='#05D9F6', high='#5011D1') +\
		xlim(0, 6) + ylim(0, 20000) +\
		xlab("Carat") + ylab("Price") +\
		ggtitle("Diamond Price by Carat and Cut") +\
		theme_gray()
print(plt3)

ggsave(plt3, "ggplot_plots.png")

***********************seaborn*********************
#可以对成对变量间的相关性、线性与非线性回归模型以及统计估计的不确定性进行可视化
import seaborn as sb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import savefig

sb.set(color_codes =True) #seaborn有自己的默认调色板,参数默认False
# 热力图
corr = df.corr()
_,ax = plt.subplots()
sb.heatmap(corr,ax=ax)

#直方图
x = np.random.normal(size = 100)
sb.distplot(x,bins=20,kde=False,rug=True,label="Histogram w/o Density")
sb.utils.axlabel("Value","Frequency")
plt.title("Histogram of a Random Sample from a normal Distribution")
plt.legend()
plt.show()

#带有回归直线的散点图与单变量直方图
mean,cov = [5,10],[(1,0.5),(0.5,1)]
data = np.random.multivariate_normal(mean, cov, 200)
data_frame = pd.DataFrame(data,columns=["x","y"])
sb.jointplot(x="x", y="y",data=data_frame,kind="reg").set_axis_labels("x","y")
plt.suptitle("Joint Plot of Two Variables")
plt.show()

#成对变量之间的散点图与单变量直方图
iris = sb.load_dataset("iris")
sb.pairplot(iris)
plt.show()

#某几个变量的箱线图
tips = sb.load_dataset("tips")
sb.factorplot(x="time",y="total_bill",hue="smoker",col="day",data=tips,kind="box",size=4,aspect=0.5)
plt.show()

#带有bootstrap置信区间的线性回归
sb.lmplot(x="total_bill",y="tip", data=tips)
plt.show()

#带有bootstrap置信区间的logit回归
tips["big_tip"] = (tips.tip/tips.total_bill)>0.15
sb.lmplot(x="total_bill", y="big_tip", data=tips,logistic=True,	y_jitter=0.03).set_axis_labels("Total Bill","Big Tip")
plt.title("logistic Regression")
plt.show()
savefig("seaborn_plots.png")
=======================描述性统计与建模======================
************葡萄酒数据处理与分析*************
---描述性统计---
import numpy as np
import pandas as pd
import seaborn as sb 
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.formula.api import ols,glm

wine = pd.read_csv("E:\\Python3.6\\data_analysis_source_code\\statistics\\winequality-both.csv",sep=",",header=0)
wine.columns = wine.columns.str.replace(" ","_")
print(wine.head())

print(wine.describe()) #描述性统计量
print(sorted(wine.quality.unique())) #找出唯一值
print(wine.quality.value_counts()) #每一个唯一值出现的次数

---分组、直方图与t检验---
#按酒的类型分组计算质量的描述性统计量
wine.groupby("type")[["quality"]].describe().unstack("type") #单中括号也可以的
# 按酒的类型计算质量的特定分位数
wine.groupby("type")[["quality"]].quantile([0.25,0.75]).unstack("type")
#查看红酒、白酒的质量分布
red_wine_quality = wine.loc[wine["type"]=="red","quality"]
white_wine_quality = wine.loc[wine["type"]=="white","quality"]
sb.set_style("dark")
print(sb.distplot(red_wine_quality,norm_hist=True,kde=False,color="red",label="Red wine"))
print(sb.distplot(white_wine_quality,norm_hist=True,kde=False,color="white",label="white wine"))
sb.axlabel(Quality Score, "Density")
plt.title("Distribution of Quality by Wine Type")
plt.legend()
plt.show()
#检验红酒和白酒的平均质量是否有差异
print(wine.groupby("type")["quality"].agg(["std"])) #agg(["std/mean/var/sum"])计算统计量
tstat,pvalue,df = sm.stats.ttest_ind(red_wine_quality,white_wine_quality)#T检验返回t值、p值、和自由度df
print("tstat:%.3f pvalue:%.4f df:%i"%(tstat,pvalue,df))

---成对变量之间的相关性和统计图---
print(wine.corr()) #相关系数矩阵
#取出部分样本数据进行绘图
def take_sample(data_frame,replace=False,n=200): #定义不重复随机取样函数
	return data_frame.loc[np.random.choice(data_frame.index,replace=replace,size=n)]
red_sample = take_sample(wine.loc[wine["type"]=="red",:])
white_sample = take_sample(wine.loc[wine["type"]=="white",:])
wine_sample = pd.concat([red_sample,white_sample])

wine["in_sample"] = np.where(wine.index.isin(wine_sample.index),1,0)
#生成新变量,若为样本值则取值为1,否则取值为0,np.where(cond,x,y)条件cond为真返回x,否则返回y
print(pd.crosstab(index=wine.in_sample, columns=wine.type,margins=True))
#pd.crosstab()生成列联表,默认为频数

sb.set_style("dark")
sb.pairplot(wine_sample,kind="reg",
			plot_kws={"ci":False,"x_jitter":0.25,"y_jitter":0.25},
			hue="type",diag_kind="hist",
			diag_kws={"bins":10,"alpha":1.0},
			palette=dict(red="red",white="white"),
			markers=["o","s"],vars=["quality","alcohol","residual_sugar"])
plt.suptitle("Histogram and Scatter Plots",fontsize=14,x=0.5,y=0.999,
			horizontalalignment="center",verticalalignment="top")
plt.show()

---线性回归---
my_formula = "quality~alcohol+ chlorides + citric_acid + density + \
			fixed_acidity + free_sulfur_dioxide + pH + residual_sugar + \
			sulphates + total_sulfur_dioxide + volatile_acidity" #类似R语言的回归公式定义
lm =ols(my_formula,data=wine).fit()
# lm = glm(my_formula,data=wine,family=sm.families.Gaussian()).fit()
print(lm.summary()) #回归结果
print("\nQuantities you can extract from the result:\n%s" % dir(lm))
print("\nCoefficients:\n%s" % lm.params)
print("\nCoefficient Std Errors:\n%s" % lm.bse)
print("\nAdj. R-squared:\n%.2f" % lm.rsquared_adj)
print("\nF-statistic: %.1f  P-value: %.2f" % (lm.fvalue, lm.f_pvalue))
print("\nNumber of obs: %d  Number of fitted values: %s" % (lm.nobs, len(lm.fittedvalues)))

dir(lm) #包含所有回归的结果信息
lm.params #返回参数序列,可以索引lm.params[1]或lm.params["alcohol"],下同
lm.bse 
lm.rsquared_adj
lm.fvalue 
lm.tvalues 
lm.f_pvalue 
lm.nobs 
lm.fittedvalues

#变量标准化---
dependent_variable = wine['quality']
independent_variables = wine[wine.columns.difference(['quality', 'type', 'in_sample'])] #difference([])去掉变量
independent_variables_standardized = (independent_variables - independent_variables.mean()) / independent_variables.std()
#pandas中可以对观测进行公式变化,pandas会把这个公式扩展到行与列中
wine_standardized = pd.concat([dependent_variable, independent_variables_standardized], axis=1)
lm_standardized = ols(my_formula, data=wine_standardized).fit()
print(lm_standardized.summary())

#预测---
new_observations = wine.ix[wine.index.isin(range(10)), independent_variables.columns] #wine.ix[,]???
y_predicted = lm.predict(new_observations)
y_predicted_rounded = [round(score, 2) for score in y_predicted]
print(y_predicted_rounded)

lm.predict()
round(number, ndigits) #保留小数位数

************客户流失数据处理与分析*************
churn = pd.read_csv("E:\\Python3.6\\data_analysis_source_code\\statistics\\churn.csv",sep=",",header=0)
churn.columns = [heading.lower() for heading in churn.columns.str.replace(" ","_").str.replace("\'","").str.strip("?")]
churn["churn01"] = np.where(churn["churn"]=="True",1.,0.)
print(churn.head())
#分组计算描述性统计量
print(churn.groupby("churn")["day_charge","eve_charge","night_charge","intl_charge","account_length","custserv_calls"].agg(["count","mean","std"]))
#分组为不同变量计算不同统计量
print(churn.groupby("churn").agg({"day_charge":["mean","std"],
								"eve_charge":["mean","std"],
								"night_charge":["mean","std"],
								"intl_charge":["mean","std"],
								"account_length":["count","min","max"],
								"custserv_calls":["count","min","max"]}))
#等宽分组计算统计量
churn['total_charges'] = churn['day_charge'] + churn['eve_charge'] + \
						 churn['night_charge'] + churn['intl_charge']
# churn.total_charges = churn.day_charge + churn.eve_charge + \
# 						 churn.night_charge + churn.intl_charge
# churn.total_charges = sum([churn.day_charge,churn.eve_charge,\
# 						 churn.night_charge,churn.intl_charge])
factor_cut = pd.cut(churn.total_charges,5,precision=2)
def get_stats(group):
	return {"min":group.min(),"max":group.max(),\
			"count":group.count(),"mean":group.mean(),\
			"std":group.std()}
grouped = churn.custserv_calls.groupby(factor_cut)
print(grouped.apply(get_stats).unstack())

#等深分组计算统计量-分位数划分
factor_qcut = pd.qcut(churn.account_length,[0,0.25,0.5,0.75,1]) #可使用整数4替代[0,0.25,0.5,0.75,1]
grouped = churn.custserv_calls.groupby(factor_qcut)
print(grouped.apply(get_stats).unstack())

#创建虚拟二值变量pd.get_dummies()根据分类变量创建虚拟变量
intl_dummies = pd.get_dummies(churn.intl_plan,prefix="intl_plan")
vmail_dummies = pd.get_dummies(churn["vmail_plan"],prefix="vmail_plan")
churn_with_dummies = churn[["churn"]].join([intl_dummies,vmail_dummies])
print(churn_with_dummies.head())

qcut_names = ["1st_quantile","2nd_quantile","3rd_quantile","4th_quantile"]
total_charges_quantile = pd.qcut(churn.total_charges, 4, labels=qcut_names) #按四分位数分组并为分位数打上标签
dummies = pd.get_dummies(total_charges_quantile,prefix="total_charges")
churn_with_dummies = churn.join(dummies)
#注意churn[["churn"]].join(dummies)单独把churn列取出与dummies连接,而churn.join(dummies)是与数据框churn连接
print(churn_with_dummies.head())

#创建数据透视表
print(churn.pivot_table(["total_charges"],index=["churn","custserv_calls"])) #默认为均值
print(churn.pivot_table(["total_charges"],index=["churn"],columns=["custserv_calls"])) #默认为均值
print(churn.pivot_table(["total_charges"],index=["custserv_calls"],columns=["churn"],aggfunc="mean",fill_value="NaN",margins=True)) 

#logit回归(需要单独设置因变量、自变量而不是定义回归公式)
dependent_variable = churn["churn01"]
independent_variables = churn[["account_length","custserv_calls","total_charges"]]
independent_variables_with_constant = sm.add_constant(independent_variables,prepend=True)#在第一列添加常数1

logit_model = sm.Logit(dependent_variable,independent_variables_with_constant).fit() #PerfectSeparationError???
#logit_model = smf.glm(output_variable, input_variables, family=sm.families.Binomial()).fit()
print(logit_model.summary())
print("\nQuantities you can extract from the result:\n%s" % dir(logit_model))
print("\nCoefficients:\n%s" % logit_model.params)
print("\nCoefficient Std Errors:\n%s" % logit_model.bse)

#logit系数解释
logit_marginal_effects = logit_model.get_margeff(method='dydx', at='overall')
print(logit_marginal_effects.summary())

print("\ninvlogit(-7.2205 + 0.0012*mean(account_length) + 0.4443*mean(custserv_calls) + 0.0729*mean(total_charges))")

#自变量在均值处成功的概率
def inverse_logit(model_formula):
	from math import exp
	return (1.0 / (1.0 + exp(-model_formula)))*100.0

at_means = float(logit_model.params[0]) + \
	float(logit_model.params[1])*float(churn['account_length'].mean()) + \
	float(logit_model.params[2])*float(churn['custserv_calls'].mean()) + \
	float(logit_model.params[3])*float(churn['total_charges'].mean())

print("Probability of churn when independent variables are at their mean values: %.2f" % inverse_logit(at_means))
#自变量在均值处变化一个单位成功的概率
cust_serv_mean = float(logit_model.params[0]) + \
	float(logit_model.params[1])*float(churn['account_length'].mean()) + \
	float(logit_model.params[2])*float(churn['custserv_calls'].mean()) + \
	float(logit_model.params[3])*float(churn['total_charges'].mean())
		
cust_serv_mean_minus_one = float(logit_model.params[0]) + \
		float(logit_model.params[1])*float(churn['account_length'].mean()) + \
		float(logit_model.params[2])*float(churn['custserv_calls'].mean()-1.0) + \
		float(logit_model.params[3])*float(churn['total_charges'].mean())

print("Probability of churn when account length changes by 1: %.2f" % (inverse_logit(cust_serv_mean) - inverse_logit(cust_serv_mean_minus_one)))

#预测
new_observations = churn.ix[churn.index.isin(range(10)),independent_variables.columns]
new_observations_with_constant = sm.add_constant(new_observations,prepend=True)

y_predicted = logit_model.predict(new_observations_with_constant)
y_predicted_rounded = [round(score, 2) for score in y_predicted]
print(y_predicted_rounded)

=======================按计划自动运行脚本======================
---windows---
打开任务计划程序task scheduler
cmd： taskschd.msc /s
win+R: taskschd.msc

---macOS/Unix---
crontab:cron表文件,用于列出需要自动运行的可执行文件

10 15 * * * /path/name.py 
0 6,12,18 * * 1-5 /path/name.py
30 20 * * 6 /path/name.py
00 11 1-7 * * ["$(date '+\%a')"="Mon"] && /path/name.py
分 时 天 月 星期    条件语句 #星期天为0

cron表文件：
创建：touch crontab_file.txt
打开：crontal -e 
加载：crontab crontab_file.txt
删除：rm crontab_file.txt
编辑：crontab -e
查看：crontab -l 










