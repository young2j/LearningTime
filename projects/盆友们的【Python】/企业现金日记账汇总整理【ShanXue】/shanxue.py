import pandas as pd
path = "C:\\Users\\Jge\\Desktop\\account\\account1.xlsx"
data = pd.read_excel(path, keep_date_col=True).fillna("")


index = ["期间", "总帐日期", "凭证编号", "日记账摘要"]
grouped1 = data.groupby(index[:-1])
data["对方科目"] = None
grouped2 = data.groupby(index)

for g1, df1 in enumerate(grouped1[["借方金额", "贷方金额"]]):
	df_sub1 = df1[1]
	for i1, val1 in enumerate(df_sub1["借方金额"], start=df_sub1.index[0]):
		val2_list = []
		i2_list = []
		for i2, val2 in enumerate(df_sub1["贷方金额"], start=df_sub1.index[0]):
			if val2 != 0:
				i2_list.append(i2)
				val2_list.append(val2)
		if val1 not in val2_list:
			for i in i2_list:
				data.iloc[i1, 7] = data.iloc[i, 6]
	# # print("***********************************\n",df_sub1)
	# for i1a,val1a in enumerate(df_sub1["贷方金额"],start=df_sub1.index[0]):
	# 	val2a_list = [ ]
	# 	i2a_list = [ ]
	# 	for i2a,val2a in enumerate(df_sub1["借方金额"],start=df_sub1.index[0]):
	# 		if val2a != "NA":
	# 			i2a_list.append(i2a)
	# 			val2a_list.append(val2a)
	# 	if val1a != "NA" and val1a not in val2a_list:
	# 		for i22a in i2a_list:
	# 			data.iloc[i1a,7] = data.iloc[i22a,6]


for g2, df2 in enumerate(grouped2[["借方金额", "贷方金额"]]):
	# print("^^^^^^^^^^^^^^^^^^^",df2)
	df_sub2 = df2[1]
	# print(df_sub2.index)
	# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",df_sub2)
	for i11, val11 in enumerate(df_sub2["借方金额"], start=df_sub2.index[0]):
		# print("---",i11,val11)
		for i22, val22 in enumerate(df_sub2["贷方金额"], start=df_sub2.index[0]):
			# print("++++"i22,val22)
			# if val11 == "NA":
			# 	pass
			while val11 != "":
				if val11 == val22:
					data.iloc[i11, 7] = data.iloc[i22, 6]
					data.iloc[i22, 7] = data.iloc[i11, 6]
			else :
				continue
    # for i11a,val11a in enumerate(df_sub2["贷方金额"],start=df_sub2.index[0]):
    # 	# print("---",i11,val11)
    # 	for i22a,val22a in enumerate(df_sub2["借方金额"],start=df_sub2.index[0]):
    # 		# print("++++"i22,val22)
    # 		# if val11 == "NA":
    # 		# 	pass
    # 		if val11a != "NA" and val11a == val22a:
    # 			data.iloc[i11a,7] = data.iloc[i22a,6]
    # 			data.iloc[i22a,7] = data.iloc[i11a,6]

pathout = "C:\\Users\\Jge\\Desktop\\account\\account1_0.xlsx"
writer = pd.ExcelWriter(pathout)
data.to_excel(writer, index=False)
writer.save()
