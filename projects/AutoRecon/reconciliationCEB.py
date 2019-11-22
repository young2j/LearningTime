#!/usr/bin/env python
# coding: utf-8
# 建行对账
# 
import pandas as pd
import numpy as np
import re
import xlsxwriter

# 整理表格
class DealExcelCEB(object):
    def __init__(self,nc_path,bank_path):
        self.nc_path = nc_path
        self.bank_path = bank_path

    def dealNC(self):
        # read
        nc_ceb = pd.read_excel(self.nc_path,header=None)
        nc_ceb = nc_ceb.dropna(how='all')

        # deal year/head/tail
        year = nc_ceb.iloc[0,0]
        init_period = nc_ceb.iloc[2,:] # 暂时保存期初行
        month_year_sum = nc_ceb.tail(2) # 暂时保存本月及本年累计行

        # drop useless rows
        nc_ceb.columns = nc_ceb.iloc[1,:] 
        nc_ceb = nc_ceb.drop([0,1,2]) 
        nc_ceb = nc_ceb.head(len(nc_ceb)-2)

        time = str(year) + '-' + nc_ceb['月'].astype(str) + '-' + nc_ceb['日'].astype(str)
        nc_ceb.insert(0,'日期',pd.to_datetime(time,format='%Y-%m-%d').astype(str).str.slice(0,10))

        nc_ceb.reset_index(drop=True,inplace=True)

        # 提取交易时间
        time_pattern1 = re.compile(r'\d{4}-\d+-\d+')
        time_pattern2 = re.compile(r'\d{4}\.\d+\.\d+')
        time_pattern3 = re.compile(r'\d+\.\d+')

        transac_time = nc_ceb['摘要'].copy()
        for i in range(len(transac_time)):
            time1 = time_pattern1.findall(transac_time[i]) #[2019-07-01]
            if time1 !=[]:
                transac_time[i] = time1[0]
            else:
                time2 = time_pattern2.findall(transac_time[i]) #[2019.8.2]
                if time2!=[]:
                    transac_time[i] = time2[0]
                else:
                    time3 = time_pattern3.findall(transac_time[i]) #[8.2] #[2019.7]
                    try:
                        if len(str(time3[0]).split('.')[0])==4:
                            transac_time[i] = None
                        else:
                            transac_time[i] = str(year) + '.' + time3[0]
                    except IndexError:
                        transac_time[i] = None

        nc_ceb.insert(6,'交易日期',transac_time)
        nc_ceb['交易日期']=pd.to_datetime(transac_time,format='%Y-%m-%d')

        # 生成对账标记
        nc_ceb.insert(0,"银行索引",None)
        nc_ceb.insert(0,'对账一致',None)

        # 转换字段类型
        nc_ceb.columns = list(map(lambda x: str(x).strip(),nc_ceb.columns))
        nc_ceb.loc[:,['银行账户名称','摘要']] = nc_ceb[['银行账户名称','摘要']].apply(lambda s: s.str.strip().str.replace('[ （）()]',''))
        nc_ceb.loc[:,['借方','贷方','余额']] = nc_ceb[['借方','贷方','余额']].apply(lambda s: s.astype(np.float64))

        nc_ceb.drop(['月','日'],axis=1,inplace=True)

        return nc_ceb

    def dealBANK(self):
        # read
        ceb = pd.read_excel(self.bank_path,header=None)
        ceb = ceb.dropna(how='all')

        if ceb.iloc[0,0]=='组织':
            ceb.columns = ceb.loc[0,:]
            ceb = ceb.drop(0)

            need_fields = ["组织","银行","账号","币种","交易日期","收入","支出","当前余额", 
                           "用途","对方户名", "对方账号","来源","备注","业务类型","资金系统单据号"]
            for col in need_fields:
                if col not in ceb.columns:
                    ceb[col] = None
            ceb['交易日期'] = pd.to_datetime(ceb['交易日期'])

            strip_fields = ["组织","账号","币种","用途","对方户名","备注","业务类型"]
            ceb.loc[:,strip_fields] = ceb[strip_fields].apply(lambda s: s.str.strip().str.replace('[ （）()]','')) 

        else:            
            # drop useless rows
            for row in ceb.index:
                for col in ceb.columns:
                    if str(ceb.loc[row,col]).strip()=='交易时间':
                        header_row = row
            #             print(header_row)
                        break
            ceb.columns = ceb.loc[header_row,:]
            ceb = ceb.loc[header_row+1:,:]
            
            
            # transform columns
            ceb.columns = list(map(lambda x: str(x).strip(),ceb.columns))
                
            rename_dict = {
                "贷方发生额":"收入",
                "借方发生额":"支出",
                "账户余额":"当前余额",
                "摘要":"用途",
                "对方名称":"对方户名",
            }

            ceb.rename(columns=rename_dict,inplace=True)

            ceb['交易日期'] = pd.to_datetime(ceb['交易日期'].str.slice(0,10),format='%Y-%m-%d')  
            
            ceb["银行"] = 'CEB-光大银行'
            ceb["来源"] = 'U-CEB'
            ceb['币种'] = 'CNY-人民币'
            ceb['资金系统单据号'] = None
            ceb['组织'] = None
            ceb['业务类型'] = None
            ceb['备注'] = None
            ceb['账号'] = None


            # drop useless columns
            need_fields = ["组织","银行","账号","币种","交易日期","收入","支出","当前余额", 
                           "用途","对方户名", "对方账号","来源","备注","业务类型","资金系统单据号"]
            ceb = ceb[need_fields]
        
            strip_fields = ["组织","账号","币种","用途","对方户名","备注","业务类型"]
            ceb.loc[:,strip_fields] = ceb[strip_fields].apply(lambda s: s.str.strip().str.replace('[ （）()]',''))
            
        # 对账标记
        ceb.insert(0,"NC索引",None)
        ceb.insert(0,'对账一致',None)
        ceb.reset_index(inplace=True)
        ceb.sort_values(['index'])
        ceb.drop(['index'],axis=1,inplace=True)


        num_fields = ['收入','支出','当前余额']

        ceb.loc[:,num_fields] = ceb[num_fields].apply(lambda s: s.astype(str).str.strip().replace({'':None}).astype(np.float64))

        return ceb

# 对账规则
class CheckCEB(object):
    def __init__(self,nc_ceb,ceb,nc_file_name,ceb_file_name,save_path=None):
        self.nc_ceb = nc_ceb
        self.ceb = ceb
        self.nc_file_name = nc_file_name
        self.ceb_file_name = ceb_file_name
        self.save_path = save_path

    def rec_loans(self):
        '''
        收到归还借款
        eg:
            收到wangwb-王文彬归还F0403-因公临时借款
        
        rule:
            1. 借贷金额相同
            2. 银行——对方名称：王文彬
        '''
        regex_rec_loans = re.compile(r'收到.*归还.*借款$')
        is_rec_loans = self.nc_ceb['摘要'].str.match(regex_rec_loans)
        nc_rec_loans = self.nc_ceb[is_rec_loans]
        
        for nc_idx in nc_rec_loans.index:
            cond1 = (self.ceb['收入']==self.nc_ceb.loc[nc_idx,'借方']) #借贷金额相同
            ceb_rec_loans = self.ceb[cond1]

            for idx in ceb_rec_loans.index:
                otherside_cond = (ceb_rec_loans.loc[idx,'对方户名'] in self.nc_ceb.loc[nc_idx,'摘要'])
                if otherside_cond: # 对方单位为 nc摘要中的姓名
                    self.nc_ceb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ceb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ceb.loc[nc_idx,'银行索引'] = idx
                    self.ceb.loc[idx,'NC索引'] = nc_idx 


    def prepay_firmamount(self):
        '''
        支付公司预付款
        eg: 
        支付贵州格源建筑装饰工程有限公司遵义领地．蘭台府项目售楼部和样板房精装修、售楼部幕墙装饰施工合同预付款

        rule:
            1. 借贷金额相同
            2. 银行——对方名称：  贵州格源建筑装饰工程有限公司                                               
            3. 银行——摘要：  装修工程款
        '''
        
        regex_prepay_firm_amount = re.compile(r'预付.*公司.*款|支付.*公司.*预付款')
        is_prepay_firm_amount = self.nc_ceb['摘要'].str.match(regex_prepay_firm_amount)
        nc_prepay_firm_amount = self.nc_ceb[is_prepay_firm_amount]
        
        for nc_idx in nc_prepay_firm_amount.index:
            cond1 = (self.ceb['支出']==self.nc_ceb.loc[nc_idx,'贷方']) #借贷金额相同
            ceb_prepay_firm_amount = self.ceb[(cond1)]

            for idx in ceb_prepay_firm_amount.index:
                otherside_cond = ceb_prepay_firm_amount.loc[idx,'对方户名'] in self.nc_ceb.loc[nc_idx,'摘要'] # 对方单位是 nc摘要中的公司
                if otherside_cond:
                    self.nc_ceb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ceb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ceb.loc[nc_idx,'银行索引'] = idx
                    self.ceb.loc[idx,'NC索引'] = nc_idx      

    def pay_reimburse(self):
        '''
        支付报销款
        eg:
            支付zoudh0408-邹德会报销F010101-办公用品款BX-190902-000288
        
        rule: 
            1. 借贷金额相同
            2. 银行——摘要：财务报销－备注：报销费用
            3. 银行——对方名称:邹德会
        '''
        regex_pay_reimburse = re.compile(r'支付.*报销.*款.*')
        is_pay_reimburse = self.nc_ceb['摘要'].str.match(regex_pay_reimburse)
        nc_pay_reimburse = self.nc_ceb[is_pay_reimburse]
        print(nc_pay_reimburse)
        for nc_idx in nc_pay_reimburse.index:
            cond1 = (self.ceb['支出']==self.nc_ceb.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.ceb['用途'].str.contains('报销'))
            ceb_pay_reimburse = self.ceb[(cond1&cond2)]

            for idx in ceb_pay_reimburse.index:
                otherside_cond = (ceb_pay_reimburse.loc[idx,'对方户名'] in self.nc_ceb.loc[nc_idx,'摘要'])
                if otherside_cond: # 对方单位为 nc摘要中的姓名/公司
                    self.nc_ceb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ceb.loc[idx,'对账一致'] = 'yes' 
                    self.nc_ceb.loc[nc_idx,'银行索引'] = idx
                    self.ceb.loc[idx,'NC索引'] = nc_idx      


    def pay_loans(self):
        '''
        支付借款
        eg: 
            支付yuanquan-袁泉借F0403-因公临时借款JK-190903-000138
        
        rule:
            1. 借贷金额相同
            2. 银行——对方名称：袁泉
        '''
            
        regex_pay_loans = re.compile(r'支付.*借.*借款.*')
        is_pay_loans = self.nc_ceb['摘要'].str.match(regex_pay_loans)
        nc_pay_loans = self.nc_ceb[is_pay_loans]
        
        for nc_idx in nc_pay_loans.index:
            cond1 = (self.ceb['支出'] == self.nc_ceb.loc[nc_idx,'贷方']) #借贷金额相同
            ceb_pay_loans = self.ceb[(cond1)]

            for idx in ceb_pay_loans.index:
                otherside_cond = (ceb_pay_loans.loc[idx,'对方户名'] in self.nc_ceb.loc[nc_idx,'摘要'])
                if otherside_cond: # 对方单位为 nc摘要中的姓名
                    self.nc_ceb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ceb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ceb.loc[nc_idx,'银行索引'] = idx
                    self.ceb.loc[idx,'NC索引'] = nc_idx

    def pay_bidbond(self):
        '''
        退还投标保证金
        eg:
        nc——
            退还投标保证金 150000
            退还投标保证金 20000
        
        bank——
        交易日期    借方发生额    贷发发生额  账户余额     摘要
        2019-09-06  20000               2276075.58  退投标保证金
        2019-09-06              20000   2296075.58  账号不存在；原交易流水号：901304015643；
        2019-09-06  20000               2276075.58  退投标保证金
        2019-09-06  -20000              2389319.18  网银跨行汇款失败，收款行拒绝原因：账号解析失败
        2019-09-06  20000               2369319.18  退投标保证金
        2019-09-06  50000               2389319.18  退投标保证金
        2019-09-06  50000               2439319.18  退投标保证金
        2019-09-06  50000               2489319.18  退投标保证金
    
        rule:
            > 双边汇总
            
            1. 银行——摘要：退投标保证金/账号不存在/汇款失败
            2. 汇总nc贷方金额
            3. 汇总银行借方金额
            4. 汇总银行贷方金额
            5. 2-3=1
        '''
        is_bidbond = self.nc_ceb['摘要'].str.contains("退还投标保证金")
        nc_bidbond = self.nc_ceb[is_bidbond]

        purpose_cond1 = self.ceb['用途'].str.contains("退投标保证金")
        purpose_cond2 = self.ceb['用途'].str.contains("账号不存在|汇款失败")
        
        # 分两种情况,以免匹配到其他情况中的 '账号不存在'
        ceb_bidbond = self.ceb[(purpose_cond1|purpose_cond2)]
        ceb_sum = ceb_bidbond['支出'].sum()-ceb_bidbond['收入'].sum()

        ceb_bidbond_ = self.ceb[purpose_cond1]
        ceb_sum_ = ceb_bidbond_['支出'].sum()-ceb_bidbond_['收入'].sum()
        
        if nc_bidbond['贷方'].sum() == ceb_sum:
            self.nc_ceb.loc[nc_bidbond.index,'对账一致'] = 'yes'
            self.ceb.loc[ceb_bidbond.index,'对账一致'] = 'yes'
            self.nc_ceb.loc[nc_bidbond.index,'银行索引'] = ';'.join(map(str,ceb_bidbond.index.values))
            self.ceb.loc[ceb_bidbond.index,'NC索引'] = ';'.join(map(str,nc_bidbond.index.values))

        elif nc_bidbond['贷方'].sum() == ceb_sum_:
            self.nc_ceb.loc[nc_bidbond.index,'对账一致'] = 'yes'
            self.ceb.loc[ceb_bidbond_.index,'对账一致'] = 'yes'
            self.nc_ceb.loc[nc_bidbond.index,'银行索引'] = ';'.join(map(str,ceb_bidbond_.index.values))
            self.ceb.loc[ceb_bidbond_.index,'NC索引'] = ';'.join(map(str,nc_bidbond.index.values))

    def export_excel(self):
        nc_rows_counts = self.nc_ceb['对账一致'].value_counts(dropna=False)
        ceb_rows_counts = self.ceb['对账一致'].value_counts(dropna=False)

        try:
            nc_yes_rows = nc_rows_counts['yes']
        except KeyError:
            nc_yes_rows = 0
        nc_notmatch_rows = nc_rows_counts.sum()-nc_yes_rows

        try:
            ceb_yes_rows = ceb_rows_counts['yes']
        except KeyError:
            ceb_yes_rows = 0
        ceb_notmatch_rows = ceb_rows_counts.sum()-ceb_yes_rows
        

        print('\n')
        print("+--------------------------------------------------+")
        print("¦                  RESULTS                         ¦")
        print("+--------------------------------------------------+")
        print("¦ EXCEL    ¦       NC_CEB     ¦         CEB        ¦")
        print("+--------------------------------------------------+")
        print("¦ TOTAL    ¦{0:^18}¦{1:^20}¦".format(nc_rows_counts.sum(),ceb_rows_counts.sum()))
        print("+--------------------------------------------------+")
        print("¦ MATCH    ¦{0:^18}¦{1:^20}¦".format(nc_yes_rows,ceb_yes_rows))
        print("+--------------------------------------------------+")
        print("¦ NOTMATCH ¦{0:^18}¦{1:^20}¦".format(nc_notmatch_rows,ceb_notmatch_rows))
        print("+--------------------------------------------------+")
        print('\n')


        self.nc_ceb['交易日期'] = self.nc_ceb['交易日期'].astype(str).str.slice(0,10)
        self.ceb['交易日期'] = self.ceb['交易日期'].astype(str).str.slice(0,10)

        
        save_file = self.save_path + '\\' + self.nc_file_name + '+' + self.ceb_file_name + '.xlsx'
        print("结果保存至:\n\t%s\n" %(save_file))
        # self.nc_ceb.to_excel(self.save_path + '/nc_ceb.xlsx')
        # self.ceb.to_excel(self.save_path + '/ceb.xlsx')
        writer = pd.ExcelWriter(save_file,engine='xlsxwriter')
        self.nc_ceb.to_excel(writer,sheet_name=self.nc_file_name,startrow=1,startcol=1,header=False,index=False)
        self.ceb.to_excel(writer,sheet_name=self.ceb_file_name,startrow=1,startcol=1,header=False,index=False)
        
        workbook = writer.book
        nc_sheet = writer.sheets[self.nc_file_name]
        ceb_sheet = writer.sheets[self.ceb_file_name]

        header_format = workbook.add_format({
                        "bold":True,
                        "bg_color":'#67d8ef',
                        'font_size':15,
                        'font_name':"微软雅黑",
                        "align":'center',
                        'border':2,
                })
        cell_format = workbook.add_format({
                        "font_size":12,
                        "font_name":"微软雅黑",
                        "border":1,
                        "border_color":'#67d8ef',
                        "align":"left",
            })

        yes_format = workbook.add_format({
                                    "bg_color":"#ffff00",
                                    "font_size":12,
                                    "font_name":"微软雅黑",
                                    "border":1,
                                    "border_color":'#67d8ef',
                                    "align":"left"
                        })
        
        # nc
        # row format
        
        nc_rows,nc_cols = self.nc_ceb.shape
        for i in range(nc_rows+5):
            nc_sheet.set_row(i,22,cell_format)

        yes_index = self.nc_ceb[self.nc_ceb['对账一致']=='yes'].index+1
        for i in yes_index:
            nc_sheet.set_row(i,22,yes_format)

        # col format
        nc_sheet.set_column(0,nc_cols+5,22)

        nc_sheet.write_row('B1',self.nc_ceb.columns,header_format)
        nc_sheet.write_column('A2',self.nc_ceb.index,header_format)
        nc_sheet.freeze_panes(1,1)
        nc_sheet.set_tab_color('#FF9900')

        #ceb
        # row format
        ceb_rows,ceb_cols = self.ceb.shape
        for i in range(ceb_rows+5):
            ceb_sheet.set_row(i,22,cell_format)

        yes_index = self.ceb[self.ceb['对账一致']=='yes'].index+1
        for i in yes_index:
            ceb_sheet.set_row(i,22,yes_format)

        # col format
        ceb_sheet.set_column(0,ceb_cols+5,22)

        ceb_sheet.write_row('B1',self.ceb.columns,header_format)
        ceb_sheet.write_column('A2',self.ceb.index,header_format)
        ceb_sheet.freeze_panes(1,1)
        ceb_sheet.set_tab_color('#FF9900')

        writer.save()



    def doall(self):
        self.rec_loans()
        self.prepay_firmamount()
        self.pay_reimburse()
        self.pay_loans()
        self.pay_bidbond()


        self.export_excel()

    def __call__(self):
        return self.doall()