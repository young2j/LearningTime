#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import re

# 整理NC表
class DealExcelABC(object):
    def __init__(self,nc_path,bank_path):
        self.nc_path = nc_path
        self.bank_path = bank_path

    def dealNC(self):
        # read
        nc_abc = pd.read_excel(self.nc_path,header=None)
        nc_abc = nc_abc.dropna(how='all')

        # deal year/head/tail
        year = nc_abc.iloc[0,0]
        init_period = nc_abc.iloc[2,:] # 暂时保存期初行
        month_year_sum = nc_abc.tail(2) # 暂时保存本月及本年累计行

        # drop useless rows
        nc_abc.columns = nc_abc.iloc[1,:] 
        nc_abc = nc_abc.drop([0,1,2]) 
        nc_abc = nc_abc.head(len(nc_abc)-2)

        time = str(year) + '-' + nc_abc['月'].astype(str) + '-' + nc_abc['日'].astype(str)
        nc_abc.insert(0,'日期',pd.to_datetime(time,format='%Y-%m-%d').astype(str).str.slice(0,10))

        nc_abc.reset_index(drop=True,inplace=True)

        # 提取交易时间
        time_pattern1 = re.compile(r'\d{4}-\d+-\d+')
        time_pattern2 = re.compile(r'\d{4}\.\d+\.\d+')
        time_pattern3 = re.compile(r'\d+\.\d+')

        transac_time = nc_abc['摘要'].copy()
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

        nc_abc.insert(6,'交易日期',transac_time)
        nc_abc['交易日期']=pd.to_datetime(transac_time,format='%Y-%m-%d')

        # 生成对账标记
        nc_abc.insert(0,"银行索引",None)
        nc_abc.insert(0,'对账一致',None)

        # 转换字段类型
        nc_abc.columns = list(map(lambda x: str(x).strip(),nc_abc.columns))
        nc_abc.loc[:,['银行账户名称','摘要']] = nc_abc[['银行账户名称','摘要']].apply(lambda s: s.str.strip().str.replace('[ （）()]',''))
        nc_abc.loc[:,['借方','贷方','余额']] = nc_abc[['借方','贷方','余额']].apply(lambda s: s.astype(np.float64))
        
        nc_abc.drop(['月','日'],axis=1,inplace=True)

        return nc_abc

    def dealBANK(self):
        # read
        abc = pd.read_excel(self.bank_path,header=None)
        abc = abc.dropna(how='all')

        if abc.iloc[0,0]=='组织':
            abc.columns = abc.loc[0,:]
            abc = abc.drop(0)

            need_fields = ["组织","银行","账号","币种","交易日期","收入","支出","当前余额", 
                           "用途","对方户名","对方账号","交易行名","来源","备注","业务类型","资金系统单据号"]
            for col in need_fields:
                if col not in abc.columns:
                    abc[col] = None
            abc['交易日期'] = pd.to_datetime(abc['交易日期'])

            strip_fields = ["组织","账号","币种","用途","对方户名","对方账号","备注","业务类型"]
            abc.loc[:,strip_fields] = abc[strip_fields].apply(lambda s: s.str.strip().str.replace('[ （）()]',''))

        else:
            # drop useless rows
            for row in abc.index:
                for col in abc.columns:
                    if str(abc.loc[row,col]).strip()=='交易时间':
                        header_row = row
            #             print(header_row)
                        break
                    elif str(abc.loc[row,col]).strip()=='交易日期':
                        header_row = row
                        break
            abc.columns = abc.loc[header_row,:]
            abc = abc.loc[header_row+1:,:]
            
            
            # transform columns
            abc.columns = list(map(lambda x: str(x).strip(),abc.columns))
    
            rename_dict = {
                "交易时间": "交易日期",
                "收入金额":"收入",
                "支出金额":"支出",
                "账户余额":"当前余额",
                "本次余额":"当前余额",
                "交易用途":"用途", #一种格式
                "交易附言":"用途" #另一种格式
            }
            abc.rename(columns=rename_dict,inplace=True)

            abc['交易日期'] = pd.to_datetime(abc['交易日期'].str.slice(0,8),format='%Y-%m-%d')
            abc["银行"] = 'ABC-农业银行'
            abc["来源"] = 'U-ABC'
            abc['币种'] = 'CNY-人民币'
            abc['资金系统单据号'] = None
            abc['备注'] = None
            abc['组织'] = None
            abc['账号'] = None
            abc['业务类型'] = None
        
            need_fields = ["组织","银行","账号","币种","交易日期","收入","支出","当前余额", 
                           "用途","对方户名","对方账号","交易行名","来源","备注","业务类型","资金系统单据号"]
            abc = abc[need_fields]
        
            strip_fields = ["组织","账号","币种","用途","对方户名","对方账号","备注","业务类型"]
            abc.loc[:,strip_fields] = abc[strip_fields].apply(lambda s: s.str.strip().str.replace('[ （）()]',''))
        
        abc.insert(0,'NC索引',None)
        abc.insert(0,'对账一致',None)
        abc.reset_index(inplace=True)
        abc.sort_values(['index'])
        abc.drop(['index'],axis=1,inplace=True)
        
        num_fields = ['收入','支出','当前余额']
        abc.loc[:,num_fields] = abc[num_fields].apply(lambda s: s.replace({'-':None}).astype(np.float64))
        
        return abc


# 对账规则

class CheckABC(object):
    def __init__(self,nc_abc,abc,nc_file_name,abc_file_name,save_path=None):
        self.nc_abc = nc_abc
        self.abc = abc
        self.nc_file_name = nc_file_name
        self.abc_file_name = abc_file_name
        self.save_path = save_path

    # income items
    def rec_firmloans(self):  
        '''
        eg:
            收到眉山市宏大建设投资有限责任公司借款

        rule:
            1. 借贷金额相同
            2. 银行——对方户名：眉山市宏大建设投资有限责任公司
            3. 银行——交易用途：股东借款. 【借款】
        '''
        regex_rec_firmloans = re.compile('.*收.*公司.*借款')
        is_rec_firmloans = self.nc_abc['摘要'].str.match(regex_rec_firmloans)
        nc_rec_firmloans = self.nc_abc[is_rec_firmloans]
        
        for nc_idx in nc_rec_firmloans.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            abc_rec_firmloans = self.abc[(cond1)]

            for idx in abc_rec_firmloans.index:
                otherside_cond = (abc_rec_firmloans.loc[idx,'对方户名'] in self.nc_abc.loc[nc_idx,'摘要'])
                purpose_cond = ("借款" in abc_rec_firmloans.loc[idx,'用途'])
                if otherside_cond and purpose_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx 

    def rec_pos(self):
        '''
        POS到账
        eg:
            2019-09-03  6093pos到账
        
        rule:
            1. 借贷金额相同
            2. 交易日期相同
            3. 银行——用途：汇总转入239980.00,转出0.00 【资金系统表请注明POS字样】
        '''
        regex_pos = re.compile(r'.*\d+pos到账')
        is_pos = self.nc_abc['摘要'].str.match(regex_pos)
        nc_pos = self.nc_abc[is_pos]
        
        for nc_idx in nc_pos.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期'])
            abc_pos = self.abc[(cond1&cond2)]
            for idx in abc_pos.index:
                purpose_cond = ("汇总转入" in abc_pos.loc[idx,'用途'])
                if  purpose_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx   

        regex_pos = re.compile(r'\d+-\d+POS到账.*|\d+-\d+pos到账.*')
        is_pos = self.nc_abc['摘要'].str.match(regex_pos)
        nc_pos = self.nc_abc[is_pos]
        
        for nc_idx in nc_pos.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            abc_pos = self.abc[(cond1)]
            for idx in abc_pos.index:
                note_cond = re.findall(r'\d+-\d+',str(abc_pos.loc[idx,'用途']))
                substract_cond = re.findall(r'\d+-\d+',self.nc_abc.loc[nc_idx,'摘要'])
                if  note_cond==substract_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx

    def rec_register_capital(self):
        '''
        eg: 
        收到眉山市宏大建设投资有限责任公司缴纳眉山川瑞达注册资本金（眉发展45部分）
    
        rule:
            1. 借贷金额相同
            2. 银行——交易用途：实缴注册资本金.
            3. 银行——对方户名: 眉山市宏大建设投资有限责任公司
        '''
        regex_rec_register_capital = re.compile('.*收.*公司.*注册资本金.*')
        is_rec_register_capital = self.nc_abc['摘要'].str.match(regex_rec_register_capital)
        nc_rec_register_capital = self.nc_abc[is_rec_register_capital]
        
        for nc_idx in nc_rec_register_capital.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            abc_rec_register_capital = self.abc[(cond1)]

            for idx in abc_rec_register_capital.index:
                otherside_cond = (abc_rec_register_capital.loc[idx,'对方户名'] in self.nc_abc.loc[nc_idx,'摘要'])
                purpose_cond = ("注册资本金" in abc_rec_register_capital.loc[idx,'用途'])
                if otherside_cond and purpose_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx        


    def rec_mortgage(self):
        '''
        收取银行按揭
        eg：2019-08-01收何国强;毛碧英[眉山]蘭台府-蘭台府一期-12-1703银行按揭
        
        rule:
        1. NC<->银行：<br>
            借方<->收入金额<br>
        2. 交易时间相同
        2. 银行——对方户名：何国强
        '''
        regex_mortgage = re.compile(r'.*收.*银行按揭$')
        is_mortgage = self.nc_abc['摘要'].str.match(regex_mortgage)
        nc_mortgage = self.nc_abc[is_mortgage]
        
        for nc_idx in nc_mortgage.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) #交易日期相同
            abc_mortgage = self.abc[(cond1&cond2)]

            for idx in abc_mortgage.index:
                if abc_mortgage.loc[idx,'对方户名'] in self.nc_abc.loc[nc_idx,'摘要']: # 对方户名为 nc摘要中的姓名
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx                    
        
    def rec_pfund(self):
        '''
        收取公积金
        eg:  2019-08-02收向矜玫;李欣[眉山]蘭台府-蘭台府一期-10-1304公积金 <br>
        
        rule1: 
        >逐笔比对
        
        1. NC<->银行：<br>
            借方<->收入金额<br>
        2. 交易时间相同
        3. 银行——对方户名：李欣
        
        rule2:
        >银行为汇总数，nc中为多笔金额
        
        1. 将nc中的公积金进行汇总
        2. 银行——对方户名：个人住房公积金委托贷款放款资金待结算款项专户
        3. 银行——交易用途：公积金放款. 【注意.号,有些没有】
        4. 银行金额=nc汇总金额
        '''

        # rule1
        regex_pfund = re.compile(r'.*收.*公积金$')
        is_pfund = self.nc_abc['摘要'].str.match(regex_pfund)
        nc_pfund = self.nc_abc[is_pfund]

        for nc_idx in nc_pfund.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) #交易日期相同
            abc_pfund = self.abc[(cond1&cond2)]

            for idx in abc_pfund.index:
                if abc_pfund.loc[idx,'对方户名'] in self.nc_abc.loc[nc_idx,'摘要']: # 对方单位为 nc摘要中的姓名
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx                    

        # rule2
        total_pfund = nc_pfund['借方'].sum()
        amount_cond = (self.abc['收入']==total_pfund) #借贷金额相同
        abc_pfund = self.abc[amount_cond]
        
        for idx in abc_pfund.index:
            payer_cond = (abc_pfund.loc[idx,'对方户名']=="个人住房公积金委托贷款放款资金待结算款项专户")
            purpose_cond = (abc_pfund.loc[idx,'用途'].startswith("公积金放款"))
            if  payer_cond and purpose_cond:
                self.nc_abc.loc[nc_pfund.index,'对账一致'] = 'yes'
                self.abc.loc[idx,'对账一致'] = 'yes'
                self.nc_abc.loc[nc_pfund.index,'银行索引'] = idx
                self.abc.loc[idx,'NC索引'] = ';'.join(map(str,nc_pfund.index.values))


    def rec_group(self):
        '''
        收集团往来款
        eg:  2019-08-07收集团往来款
            2019-08-19收领地集团股份有限公司往来款
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——对方户名：领地集团股份有限公司    
           银行——交易用途：资金池下拨-CC00000E2T.
        '''
        regex_rec_group = re.compile(r'.*收.*集团.*往来款')
        is_rec_group = (self.nc_abc['摘要'].str.match(regex_rec_group))
        nc_rec_group = self.nc_abc[is_rec_group]
        
        for nc_idx in nc_rec_group.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) #交易时间相同
            abc_rec_group = self.abc[(cond1 & cond2)]

            for idx in abc_rec_group.index:
                otherside_cond = (abc_rec_group.loc[idx,"对方户名"].startswith('领地集团股份有限公司'))
                if otherside_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx

    def rec_firmpfund(self):
        '''
        收公司代缴社保公积金/代买社保款
        eg: <br>
        收新疆领地代缴社保公积金往来款（郭峰）<br>
        收乌鲁木齐凯悦代买社保款<br>
        收新疆兆龙诚祥代买社保款<br>
        
        rule:
        1. 借贷金额相同
        2. 银行——对方户名：
            * 新疆领地房地产开发有限公司
            * 乌鲁木齐领地凯悦房地产开发有限公司
            * 新疆兆龙诚祥房地产开发有限公司
        
        >公司名不明晰，无法自动匹对
        '''        
        regex_rec_firmpfund = re.compile(r'收.*代缴社保公积金.*|收.*代买社保款.*')
        is_rec_firmpfund = (self.nc_abc['摘要'].str.match(regex_rec_firmpfund))
        nc_rec_firmpfund = self.nc_abc[is_rec_firmpfund]
        
        for nc_idx in nc_rec_firmpfund.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            abc_rec_firmpfund = self.abc[(cond1)]

            for idx in abc_rec_firmpfund.index:
                payer_cond = (str(abc_rec_firmpfund.loc[idx,"对方户名"]) in self.nc_abc.loc[nc_idx,'摘要'])
                if payer_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx

    def rec_firmamount(self):
        '''
        eg:
        收广东领地往来款9.2
        > 【公司名称全称】
        
        rule:
            1. 借贷金额相同
            2. 交易时间相同
            3. 银行——对方户名：广东领地房地产开发有限公司
        '''
        regex_rec_firmamount = re.compile(r'.*收.*往来款.*')
        is_rec_firmamount = (self.nc_abc['摘要'].str.match(regex_rec_firmamount))
        nc_rec_firmamount = self.nc_abc[is_rec_firmamount]
        
        for nc_idx in nc_rec_firmamount.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.abc['交易日期'] == self.nc_abc.loc[nc_idx,'交易日期'])
            abc_rec_firmamount = self.abc[(cond1&cond2)]

            for idx in abc_rec_firmamount.index:
                otherside_cond = (str(abc_rec_firmamount.loc[idx,"对方户名"]) in self.nc_abc.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx 


    def rec_buildingamount(self):
        '''
        收楼款/楼款转入
        eg1:2019-08-11收杜玉祥[眉山]蘭台府-蘭台府一期-01-801楼款
        rule1:
        > 逐笔比对
        
        1. 借贷金额相同
        2. 银行——对方单位：杜玉祥
        3. 交易时间相同
        
        eg2: 2019-08-30收薛梅[乐山]领地澜山-一期-4号楼-1-301楼款
        
        rule2:<br>
        > nc为单笔金额,银行为多笔金额
        
        1. 交易时间相同
        2. 银行——对方单位:薛梅
        3. 汇总银行金额
        4. nc金额=汇总银行金额
        
        
        eg3: 2019-08-12[眉山]凯旋国际公馆-凯旋府二期-10号楼-3301熊朝刚楼款转入，新票据A0036062
        rule3:
        
        1. 借贷金额相同
        2. 银行——对方单位：熊朝刚
        3. 交易时间相同 【此例银行时间为 2019-08-11,则匹配不上】
        '''

        regex_rec_buildingamount = re.compile(r'.*收.*楼款.*|.*楼款转入.*')
        is_rec_buildingamount = self.nc_abc['摘要'].str.match(regex_rec_buildingamount)
        nc_rec_buildingamount = self.nc_abc[is_rec_buildingamount]
        
        # rule1
        for nc_idx in nc_rec_buildingamount.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) #交易时间相同
            abc_rec_buildingamount = self.abc[(cond1 & cond2)]

            for idx in abc_rec_buildingamount.index:
                if abc_rec_buildingamount.loc[idx,'对方户名'] in self.nc_abc.loc[nc_idx,'摘要']: # 对方单位为 nc摘要中的姓名
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx                     
        
        # rule2
        for nc_idx in nc_rec_buildingamount.index:
            time_cond = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期'])
            abc_rec_buildingamount = self.abc[time_cond]
            abc_idxs = []
            for idx in abc_rec_buildingamount.index:
                if abc_rec_buildingamount.loc[idx,'对方户名'] in self.nc_abc.loc[nc_idx,'摘要']:
                    abc_idxs.append(idx)
            if self.abc.loc[abc_idxs,'收入'].sum() == self.nc_abc.loc[nc_idx,'借方']:
                self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                self.abc.loc[abc_idxs,'对账一致'] = 'yes'
                self.nc_abc.loc[nc_idx,'银行索引'] = ';'.join(map(str,abc_idxs))
                self.abc.loc[abc_idxs,'NC索引'] = nc_idx  


    def rec_return_loans(self):
        '''
        eg:
        2019-09-05收到杨荣炜归还借款
        收到liangchao-梁超归还F0403-因公临时借款

        rule:
            1. 借贷金额相同
            2. 交易时间相同
            3. 银行——对方户名：杨荣炜
        '''
        regex_rec_return_loans = re.compile(r'.*收到.*归还.*借款')
        is_rec_return_loans = self.nc_abc['摘要'].str.match(regex_rec_return_loans)
        nc_rec_return_loans = self.nc_abc[is_rec_return_loans]

        for nc_idx in nc_rec_return_loans.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) #交易时间相同
            if str(self.nc_abc.loc[nc_idx,'交易日期'])=='NaT':
                abc_rec_return_loans = self.abc[cond1]
            else:
                abc_rec_return_loans = self.abc[(cond1 & cond2)]

            for idx in abc_rec_return_loans.index:
                otherside_cond = (abc_rec_return_loans.loc[idx,"对方户名"] in self.nc_abc.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx        


    def rec_bidbond(self):
        '''
        收投标保证金
        eg：
            2019-09-05 收四川创佳暖通有限公司投标保证金

        
        rule:
            1.借贷金额相同
            2.交易时间相同
            3.银行——对方户名：四川创佳暖通设备有限公司 
        '''
        regex_rec_bidbond = re.compile(r'.*收.*投标保证金')
        is_rec_bidbond = (self.nc_abc['摘要'].str.match(regex_rec_bidbond))
        nc_rec_bidbond = self.nc_abc[is_rec_bidbond]
        
        for nc_idx in nc_rec_bidbond.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期'])
            abc_rec_bidbond = self.abc[(cond1&cond2)]

            for idx in abc_rec_bidbond.index:
                otherside_cond = (str(abc_rec_bidbond.loc[idx,"对方户名"]) in self.nc_abc.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx



    def pay_group(self):
        '''
        付集团往来款
        eg: 2019-08-19付集团往来款
            2019-08-19付领地集团股份有限公司往来款
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——对方户名：领地集团股份有限公司
        4. 银行——交易用途：资金池归集-CC00000F5P.
        '''
        regex_pay_group = re.compile(r'.*付.*集团.*往来款')
        is_pay_group = self.nc_abc['摘要'].str.match(regex_pay_group)
        nc_pay_group = self.nc_abc[is_pay_group]
        
        for nc_idx in nc_pay_group.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) #交易时间相同
            abc_pay_group = self.abc[(cond1 & cond2)]
        #     print("---------------------------\n",abc_pay_group) 
            for idx in abc_pay_group.index:
                otherside_cond = (abc_pay_group.loc[idx,"对方户名"].startswith('领地集团股份有限公司'))
                if otherside_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx                    
                    
    
    def save_rfund(self):
        '''
        存监管资金
         eg: 8.16农行7857到建行0390监管资金<br>
         rule:
         1. 借贷金额相同
         2. 交易时间相同
         3. 银行——交易用途：往来款-存入监管资金-CC00000EZD.
        '''
        regex_rfund = re.compile(r'.*行\d{4}到.*行\d{4}.*监管资金$')
        is_rfund = (self.nc_abc['摘要'].str.match(regex_rfund))
        nc_rfund = self.nc_abc[is_rfund]
        
        for nc_idx in nc_rfund.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) #交易时间相同
            abc_rfund = self.abc[(cond1 & cond2)]

            for idx in abc_rfund.index:
                purpose_cond = ('存入监管资金' in  abc_rfund.loc[idx,"用途"])
                if purpose_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx                    
    
                    
        
    def pay_pending(self):
        '''
        退待退款项
        eg: 2019-08-06退郑文林[眉山]凯旋国际公馆-凯旋府二期-30号楼-1-602待退款项
        
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——对方户名：郑文林
        '''
        regex_pay_pending = re.compile(r'.*退.*待退款项.*|.*退.*[预违]约金.*|.*退.*楼款.*')
        is_pay_pending = (self.nc_abc['摘要'].str.match(regex_pay_pending))
        nc_pay_pending = self.nc_abc[is_pay_pending]
        
        for nc_idx in nc_pay_pending.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) #交易时间相同
            abc_pay_pending = self.abc[(cond1 & cond2)]

            for idx in abc_pay_pending.index:
                receiver_cond = (abc_pay_pending.loc[idx,"对方户名"] in self.nc_abc.loc[nc_idx,'摘要'])
                if receiver_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx


    def pay_salary(self):
        '''
        计发工资
        eg: 计发7月工资/计发食堂员工7月工资
        
        ruel1:
            > 逐笔比对
            1. 借贷金额相同
            2. 银行——交易用途：发工资. 【注意有些开头有空格，结尾有.号】
            3. 交易时间相同 【没有】
        
        rule2： 
        
            > nc为汇总数，可能是多笔汇总，银行是多笔金额 【需要双边汇总,汇总前无法通过金额进行匹配】
        
            1. 汇总nc工资数：贷方
            2. 银行——交易用途：发工资./工资-CC00000F7L. 【注意有些开头有空格，结尾有.号】
            3. 汇总银行支出金额
            4. nc汇总数=银行汇总金额
        '''

        regex_pay_salary = re.compile(r'.*发.*月工资.*')
        is_pay_salary = self.nc_abc['摘要'].str.match(regex_pay_salary)
        nc_pay_salary = self.nc_abc[is_pay_salary]        
        
        #rule1
        for nc_idx in nc_pay_salary.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            abc_pay_salary = self.abc[cond1]
            for idx in abc_pay_salary.index:
                purpose_cond = ("工资" in self.abc.loc[idx,'用途'])
                if purpose_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx                  

        # rule2
        salary_cond = (self.abc['用途'].astype(str).str.contains('工资[^服务手续费]'))
        # print('salary_cond:',salary_cond)
        abc_pay_salary = self.abc[salary_cond]
        
        if nc_pay_salary['贷方'].sum()==abc_pay_salary['支出'].sum():
            self.nc_abc.loc[nc_pay_salary.index,'对账一致'] = 'yes'
            self.abc.loc[abc_pay_salary.index,'对账一致'] = 'yes'
            self.nc_abc.loc[nc_pay_salary.index,'银行索引'] = ';'.join(map(str,abc_pay_salary.index.values))
            self.abc.loc[abc_pay_salary.index,'NC索引'] = ';'.join(map(str,nc_pay_salary.index.values))

    def pay_refund(self):
        '''
        同时退预约金多户
        eg: 
        
        nc——
        退预约金4户（袁佳霖、龚喜梅、冷志云、袁锦）<br>
        bank——
        ![image.png](attachment:image.png)
        
        rule:
        1. 银行——对方户名：袁佳霖/龚喜梅/冷志云/袁锦
        2. 汇总银行支出金额 — 汇总银行收入金额
        4. 2=nc贷方金额
        '''
        
        regex_pay_refund = re.compile(r'.*退预约金\d+户')
        is_pay_refund = self.nc_abc['摘要'].str.match(regex_pay_refund)
        nc_pay_refund = self.nc_abc[is_pay_refund]
        
        for nc_idx in nc_pay_refund.index:
            abc_idxs = []
            for idx in self.abc.index:
                if str(self.abc.loc[idx,'对方户名']) in self.nc_abc.loc[nc_idx,'摘要']: # 对方户名可能为空 np.nan is float type
                    abc_idxs.append(idx)
            abc_pay_refund = self.abc.loc[abc_idxs] #在银行中找出对应账目
            pay_sum = abc_pay_refund['支出'].sum() #汇总支出
            rec_sum = abc_pay_refund['收入'].sum() #汇总收入
            if ((pay_sum-rec_sum) == self.nc_abc.loc[nc_idx,'贷方']):
                self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                self.abc.loc[abc_idxs,'对账一致'] = 'yes'
                self.nc_abc.loc[nc_idx,'银行索引'] = ';'.join(map(str,abc_idxs))
                self.abc.loc[abc_idxs,'NC索引'] = nc_idx                                        
    
    def pay_certificate_fee(self):
        '''
        退办证费
        eg: <br>
        2019-08-21退刘睿;母琼英[眉山]凯旋国际公馆-一期-5-1401房产证-工本费 <br>
        2019-08-21退刘睿;母琼英[眉山]凯旋国际公馆-一期-5-1401房产证-印花税 <br>
        2019-08-21退刘睿;母琼英[眉山]凯旋国际公馆-一期-5-1401国土证-测绘费 <br>
        2019-08-21退刘睿;母琼英[眉山]凯旋国际公馆-一期-5-1401国土证-工本费 <br>
        2019-08-21退刘睿;母琼英[眉山]凯旋国际公馆-一期-5-1401国土证-印花税 <br>
        2019-08-21退刘睿;母琼英[眉山]凯旋国际公馆-一期-5-1401他项权证费 <br>
        2019-08-21退刘睿;母琼英[眉山]凯旋国际公馆-一期-5-1401契税 <br>
        
        rule:
        > nc<->银行:双边汇总
        
        1. 汇总nc贷方金额
        2. 银行——交易时间相同
        3. 银行——交易用途：退办证费-CC00000DW8.<br>
            银行——对方用户：刘睿
        4. 汇总银行金额
        5. 汇总nc金额等于汇总银行金额
        '''
        regex_certificate_fee = re.compile(r'.*退.*工本费$|.*退.*印花税$|.*退.*测绘费$|.*退.*他项权证费$|.*退.*契税$')
        is_certificate_fee = (self.nc_abc['摘要'].str.match(regex_certificate_fee))
        nc_certificate_fee = self.nc_abc[is_certificate_fee]
        
        
        # group
        persons = nc_certificate_fee['摘要'].str.findall(re.compile(r'.*(退.*期).*')) #['退赵晓明;刘宏眉[眉山]凯旋国际公馆-三期']
        nc_certificate_fee['persons'] = [i[0] for i in persons]
        
        nc_certificate_fee_sum = nc_certificate_fee.groupby(['交易日期','persons'])['贷方'].sum().reset_index().rename(columns={'贷方':"贷方和"})
        
        for sum_idx in nc_certificate_fee_sum.index:
            abc_idxs = []
            for idx in self.abc.index:
                cond1 = (self.abc.loc[idx,'交易日期'] == nc_certificate_fee_sum.loc[sum_idx,'交易日期']) #
                cond2 = (self.abc.loc[idx,'用途'].strip().startswith("退办证费"))
                cond3 = (str(self.abc.loc[idx,'对方户名']) in nc_certificate_fee_sum.loc[sum_idx,'persons'])
                if cond1 and cond2 and cond3:
                    abc_idxs.append(idx)

            abc_certificate_fee_sum = self.abc.loc[abc_idxs]['支出'].sum()
            if abc_certificate_fee_sum==nc_certificate_fee_sum.loc[sum_idx,'贷方和']:
                idx_cond1 = (nc_certificate_fee['交易日期']==nc_certificate_fee_sum.loc[sum_idx,'交易日期'])
                idx_cond2 = (nc_certificate_fee['persons']==nc_certificate_fee_sum.loc[sum_idx,'persons'])
                nc_idxs = nc_certificate_fee[(idx_cond1 & idx_cond2)].index
                
                self.nc_abc.loc[nc_idxs,'对账一致'] = 'yes'
                self.abc.loc[abc_idxs,'对账一致'] = 'yes'
                self.nc_abc.loc[nc_idxs,'银行索引'] = ';'.join(map(str,abc_idxs))
                self.abc.loc[abc_idxs,'NC索引'] = ';'.join(map(str,nc_idxs.values))

    def pay_loans(self):
        '''
        支付借款/给借款
        eg: 
            支付lifei-李菲借F0403-因公临时借款
            2019-09-03给杨荣炜的借款 【资金系统】
        
        rule:
            1. 借贷金额相同
            2. 银行——对方户名：李菲
            3. 银行——交易用途: 借款申请单付款-CC00000E1B.【U】
            4. 交易时间相同 【资金系统】
        '''
        # u
        regex_pay_loans = re.compile(r'支付.*借.*借款|.*给.*的借款')
        is_pay_loans = (self.nc_abc['摘要'].str.match(regex_pay_loans))
        nc_pay_loans = self.nc_abc[is_pay_loans]
        
        for nc_idx in nc_pay_loans.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            abc_pay_loans = self.abc[(cond1)]
            for idx in abc_pay_loans.index:
                # purpose_cond = (abc_pay_loans.loc[idx,'用途'].startswith("借款申请单"))
                receiver_cond = (abc_pay_loans.loc[idx,"对方户名"] in self.nc_abc.loc[nc_idx,'摘要'])
                if receiver_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx

        # cs
        for nc_idx in nc_pay_loans.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) #交易时间相同
            abc_pay_loans = self.abc[(cond1&cond2)]
            for idx in abc_pay_loans.index:
                otherside_cond = (abc_pay_loans.loc[idx,"对方户名"] in self.nc_abc.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx  
    
    def pay_reimburse(self):
        '''
        支付报销款
        eg: 支付liujie02-刘洁报销F010102-快递费款
            支付16010946-上海晨光科力普办公用品有限公司报销F010101-办公用品款
            支付wanglei-王磊报销F010605-其他费用款BX-190903-000090
        
        rule:
        1. 借贷金额相同
        2. 银行——对方户名：刘洁/上海晨光科力普办公用品有限公司/王磊
        3. 银行——用途：员工报销单付款-CC00000H35
        4. <del>交易时间相同</del>
        '''
        regex_pay_reimburse = re.compile(r'支付.*报销.*款.*')
        is_pay_reimburse = (self.nc_abc['摘要'].str.match(regex_pay_reimburse))
        nc_pay_reimburse = self.nc_abc[is_pay_reimburse]
        
        for nc_idx in nc_pay_reimburse.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            abc_pay_reimburse = self.abc[(cond1)]

            for idx in abc_pay_reimburse.index:
                otherside_cond = (abc_pay_reimburse.loc[idx,"对方户名"] in self.nc_abc.loc[nc_idx,'摘要'])
                purpose_cond = ("报销" in abc_pay_reimburse.loc[idx,'用途'])
                if otherside_cond or purpose_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx              
        
    def pay_interest(self):
        '''
        归还利息
        eg: 8.7归还利息
        
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——交易用途：归还利息-CC00000E2V.
        '''
        regex_pay_interest = re.compile(r'.*归还利息$')
        is_pay_interest = (self.nc_abc['摘要'].str.match(regex_pay_interest))
        nc_pay_interest = self.nc_abc[is_pay_interest]
        
        for nc_idx in nc_pay_interest.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) #交易时间相同
            abc_pay_interest = self.abc[(cond1 & cond2)]

            for idx in abc_pay_interest.index:
                purpose_cond = ('归还利息' in  abc_pay_interest.loc[idx,"用途"])
                if purpose_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx                    
        
    def pay_flatcost(self):
        '''
        工本费请款
        eg:<br>
        nc——
        
        |银行账户名称|  凭证号|    摘要| 对方科目|   借方| 贷方|
        |---|---|---|---|---|---|
        |农行眉山市分行7857| 记-0352| 李晓娟请款[眉山]凯旋国际公馆-一期5房产证-工本费MS2019089264| 1|  0   | 80|
        |农行眉山市分行7857| 记-0352| 李晓娟请款[眉山]凯旋国际公馆-一期1车位房产证-工本费MS2019089264|    1| 0   | 160|
        |农行眉山市分行7857| 记-0352| 李晓娟请款[眉山]凯旋国际公馆-一期2房产证-工本费MS2019089264| 1|  0   | 320.00|
        |农行眉山市分行7857| 记-0352| 李晓娟请款[眉山]凯旋国际公馆-一期6房产证-工本费MS2019089264| 1|  0   | 80|
        |农行眉山市分行7857| 记-0352| 李晓娟请款[眉山]凯旋国际公馆-一期车位2房产证-工本费MS2019089264|   1|  0   | 320|
        |农行眉山市分行7857| 记-0352| 李晓娟请款[眉山]凯旋国际公馆-一期车位房产证-工本费MS2019089264|    1|  0   | 160.00|
        |农行眉山市分行7857| 记-0352| 李晓娟请款[眉山]凯旋国际公馆-一期7房产证-工本费MS2019089264| 1|  0   | 80.00|
        |农行眉山市分行7857| 记-0352| 李晓娟请款[眉山]凯旋国际公馆-一期4房产证-工本费MS2019089264| 1|  0   | 80.00|
        |农行眉山市分行7857| 记-0352| 李晓娟请款[眉山]凯旋国际公馆-一期3房产证-工本费MS2019089264| 1|  0   | 80|
        |农行眉山市分行7857| 记-0352| 李晓娟请款[眉山]凯旋国际公馆-三期21房产证-工本费MS2019089265|    1|  0   | 160.00|
        
        
        bank——
        
        |交易时间|    收入金额|   支出金额|   账户余额|   交易行名|   对方省市|   对方账号|   对方户名|   交易用途|
        |---|---|---|---|---|---|---|---|---|
        |20190815 11:11:56|   0.00|   160.00  |1007414.55 |全行资金清算专属行部 |四川省    |6228484099249704477    |李晓娟    |退办证费-CC00000EU8.|
        |20190826 16:47:20|   0.00|   1,360.00    |60335473.81    |全行资金清算专属行部 |四川省    |6228484099249704477    |李晓娟    |工本费-CC00000FIZ.|
        
        rule:
        > nc<->银行:双边汇总
        
        1. 汇总nc贷方金额
        2. 银行——对方用户：李晓娟
        3. 汇总银行金额
        4. 汇总nc金额等于汇总银行金额
        '''
        regex_pay_flatcost = re.compile('.*请款.*工本费[A-Za-z0-9]+$')
        is_pay_flatcost = (self.nc_abc['摘要'].str.match(regex_pay_flatcost))
        nc_pay_flatcost = self.nc_abc[is_pay_flatcost]
        
        #groupby
        persons = nc_pay_flatcost['摘要'].str.findall(re.compile('(.*请款).*'))
        nc_pay_flatcost['persons'] = [i[0] for i in persons]  
        nc_pay_flatcost_sum = nc_pay_flatcost.groupby(['persons'])['贷方'].sum().reset_index().rename(columns={'贷方':"贷方和"})

        for sum_idx in nc_pay_flatcost_sum.index:
            abc_idxs = []
            for idx in self.abc.index:
                cond1 = (str(self.abc.loc[idx,'对方户名']) in nc_pay_flatcost_sum.loc[sum_idx,'persons'])
                if cond1:
                    abc_idxs.append(idx)
        
            abc_pay_flatcost_sum = self.abc.loc[abc_idxs]['支出'].sum()
            if abc_pay_flatcost_sum==nc_pay_flatcost_sum.loc[sum_idx,'贷方和']:
                idx_cond1 = (nc_pay_flatcost['persons']==nc_pay_flatcost_sum.loc[sum_idx,'persons'])
                nc_idxs = nc_pay_flatcost[(idx_cond1)].index
                
                self.nc_abc.loc[nc_idxs,'对账一致'] = 'yes'
                self.abc.loc[abc_idxs,'对账一致'] = 'yes'
                self.nc_abc.loc[nc_idxs,'银行索引'] = ';'.join(map(str,abc_idxs))
                self.abc.loc[abc_idxs,'NC索引'] = ';'.join(map(str,nc_idxs.values))              
    
    def prepay_firmamount(self):
        '''
        预付公司款项/支付预付款
        eg: <br>
            预付1020304143-中国石化销售股份有限公司四川眉山石油分公司F010601-油费款 
            支付惠民凯旋府一批次自来水安装工程合同（高区加压）预付款
            预付1010101-中国石油天然气股份有限公司四川销售成品油分公司F0708-董事会费-汽车费用款GYSYFK-190902-000282
            预付1010212-四川省商会F010113-协会会费款GYSYFK-190905-000414
        rule:
        1. 借贷金额相同
        2. 银行——对方户名：中国石化销售股份有限公司四川眉山石油分公司
                          眉山市惠民供排水设备安装有限公司
                          中国石油天然气股份有限公司四川销售成品油分公司
                          四川省商会

        > 后者因nc摘要公司名不明晰，就无法匹对上
        '''
        
        regex_prepay_firmamount = re.compile(r'预付.*[公司商会].*款$|支付.*公司.*预付款$|预付.*[公司商会].*款\w.*|支付.*公司.*预付款\w.*')
        is_prepay_firmamount = (self.nc_abc['摘要'].str.match(regex_prepay_firmamount))
        nc_prepay_firmamount = self.nc_abc[is_prepay_firmamount]
        
        for nc_idx in nc_prepay_firmamount.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            abc_prepay_firmamount = self.abc[(cond1)]

            for idx in abc_prepay_firmamount.index:
                receiver_cond = (str(abc_prepay_firmamount.loc[idx,"对方户名"]) in self.nc_abc.loc[nc_idx,'摘要'])
                if receiver_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx                    
    
    
    def pay_fall(self):
        '''
        摔伤赔付支出
        eg: 摔伤赔付支出
        
        rule:
        1. 借贷金额相同
        2. 银行——对方户名：黄勤 //发挥不了作用,如果摘要注明赔付给谁就很完美<br>
           银行——交易用途：赔付款-CC00000EPR.
        '''
        regex_pay_fall = re.compile(r'.*摔伤赔付支出.*')
        is_pay_fall = (self.nc_abc['摘要'].str.match(regex_pay_fall))
        nc_pay_fall = self.nc_abc[is_pay_fall]
        
        for nc_idx in nc_pay_fall.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            abc_pay_fall = self.abc[(cond1)]

            for idx in abc_pay_fall.index:
        #         receiver_cond = (str(abc_pay_fall.loc[idx,"对方户名"]) in self.nc_abc.loc[nc_idx,'摘要'])
                purpose_cond = (abc_pay_fall.loc[idx,'用途'].startswith('赔付款'))
                if purpose_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx                    
    
    def pay_progressamount(self):
        '''
        支付合同进度款
        eg: 支付中亚建业建设工程有限公司领地凯旋府三期二批次土建工程施工总承包合同进度款
            支付四川中城易建筑工程有限公司溪山蘭台项目土石方工程施工合同进度款YH[2019]006

        rule:
        1. 借贷金额相同
        2. 银行——对方户名：中亚建业建设工程有限公司/四川中城易建筑工程有限公司
        '''
        regex_progress_payment = re.compile(r'支付.*进度款$|支付.*进度款\w.*')
        is_progress_payment = (self.nc_abc['摘要'].str.match(regex_progress_payment))
        nc_progress_payment = self.nc_abc[is_progress_payment]
        
        for nc_idx in nc_progress_payment.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            abc_progress_payment = self.abc[(cond1)]
            
            for idx in abc_progress_payment.index:
                receiver_cond = (str(abc_progress_payment.loc[idx,"对方户名"]) in self.nc_abc.loc[nc_idx,'摘要'])
                if receiver_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx                    
    
    def pay_ssfund(self):
        '''
        付员工社保公积金
        eg: <br>
        nc——
        
        |摘要|  对方科目|   借方| 贷方|
        |---|---|---|---|
        |付8月员工社保公积金|  1|      40,846.27|
        |付8月员工社保公积金|  1|      76,318.09|
        |多交医保下月抵扣|    1|      15,600.00|
        
        bank——
        
        |收入金额 |支出金额   |交易行名 |对方户名 |交易用途|
        |---|---|---|---|---|
        |0.00 |41,225.84  |中国农业银行股份有限公司四川省分行清算中心      |眉山市医疗保障事务中心    |社会保险费-CC00000F7M.|
        |0.00 |37,818.88  |中国农业银行股份有限公司四川省分行清算中心      |眉山市住房公积金管理中心   |公积金 P1908129825-CC00000F7N.|
        |0.00 |54,551.64  |中国农业银行股份有限公司四川省分行清算中心      |眉山市社会保险事务中心    |社会保险费-CC00000F7O.|
        |37,818.88    |0.00   |中国农业银行股份有限公司四川省分行清算中心      |眉山市住房公积金管理中心   |TS单位转款错误，申请退款.|
        |0.00 |36,986.88  |中国农业银行股份有限公司四川省分行清算中心      |眉山市住房公积金管理中心   |公积金 P1908129825-CC00000FD8.|
        
        rule:
        > nc<->银行双边汇总
        
        1. 汇总nc贷方金额
        2. 银行——对方户名：眉山市医疗保障事务中心/眉山市住房公积金管理中心/眉山市社会保险事务中心
        3. 汇总银行支出金额-汇总银行收入金额
        4. 1=3
        '''

        regex_pay_ssfund = re.compile(r'付.*员工社保公积金|多交[医社]保下月抵扣') # social security fund
        is_pay_ssfund = (self.nc_abc['摘要'].str.match(regex_pay_ssfund))
        nc_pay_ssfund = self.nc_abc[is_pay_ssfund]
        
        cond1 = (self.abc['对方户名'] == "眉山市医疗保障事务中心")
        cond2 = (self.abc['对方户名'] == "眉山市住房公积金管理中心")
        cond3 = (self.abc['对方户名']=="眉山市社会保险事务中心")
        
        abc_pay_ssfund = self.abc[(cond1|cond2|cond3)]
        
        nc_pay_ssfund_sum = nc_pay_ssfund['贷方'].sum()
        abc_pay_ssfund_sum = abc_pay_ssfund['支出'].sum()-abc_pay_ssfund['收入'].sum()
        
        if nc_pay_ssfund_sum == abc_pay_ssfund_sum:
            self.nc_abc.loc[nc_pay_ssfund.index,'对账一致'] = 'yes'
            self.abc.loc[abc_pay_ssfund.index,'对账一致'] = 'yes'
            self.nc_abc.loc[nc_pay_ssfund,'银行索引'] = ';'.join(map(str,abc_pay_ssfund.index.values))
            self.abc.loc[abc_pay_ssfund,'NC索引'] = ';'.join(map(str,nc_pay_ssfund.index.values))

    def pay_bankfee(self):
        '''
        eg:
        8.19农行1277手续费
        
        rule:
            1. 借贷金额相同
            2. 交易时间相同
            3. 银行——交易用途: 付1277账户本金2607.43日志号280708576手续费（050273）.   
        '''
        regex_pay_bankfee = re.compile(r'.*行.*手续费')
        is_pay_bankfee = self.nc_abc['摘要'].str.match(regex_pay_bankfee)
        nc_pay_bankfee = self.nc_abc[is_pay_bankfee]
        # print('nc_pay_bankfee:',nc_pay_bankfee)

        for nc_idx in nc_pay_bankfee.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期'])
            abc_pay_bankfee = self.abc[(cond1 & cond2)]
            # print("abc_pay_bankfee:",abc_pay_bankfee)

            for idx in abc_pay_bankfee.index:
                if '手续费' in abc_pay_bankfee.loc[idx,'用途']: # 银行摘要含 '手续费'
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx

    def pay_land(self):
        '''
        eg:
            付眉山市自然交易资源局Ｓ－６－１号土地款土地款

        rule:
            1. 借贷金额相同
            2. 银行——交易用途：Ｓ－６－１号土地款.  
            3. 银行——对方户名: 眉山市财政非税收入专户
        '''
        regex_pay_land = re.compile('付.*土地款$')
        is_pay_land = self.nc_abc['摘要'].str.match(regex_pay_land)
        nc_pay_land = self.nc_abc[is_pay_land]
        
        for nc_idx in nc_pay_land.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            abc_pay_land = self.abc[(cond1)]

            for idx in abc_pay_land.index:
                otherside_cond = (abc_pay_land.loc[idx,'对方户名'].endswith("财政非税收入专户"))
                purpose_cond = ("土地款" in abc_pay_land.loc[idx,'用途'])
                if otherside_cond and purpose_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx        


    def pay_firmamount(self):
        '''
        支付公司往来款
        eg:
            支付西藏瑞鼎商贸往来款9.5
            付眉山分公司往来款9.6
            2019-09-06支付领地集团股份有限公司乐山分公司往来款
        
        rule:
            1. 借贷金额相同
            2. 交易时间相同
            3. 银行——对方户名：西藏瑞鼎商贸有限公司/领地集团股份有限公司眉山分公司/乐山领地房地产开发有限公司
        '''
        
        regex_pay_firmamount = re.compile(r'.*付.*公司.*往来款.*')
        is_pay_firmamount = (self.nc_abc['摘要'].str.match(regex_pay_firmamount))
        nc_pay_firmamount = self.nc_abc[is_pay_firmamount]
        
        for nc_idx in nc_pay_firmamount.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期'])
            abc_pay_firmamount = self.abc[(cond1&cond2)]

            for idx in abc_pay_firmamount.index:
                otherside_cond = (str(abc_pay_firmamount.loc[idx,"对方户名"]) in self.nc_abc.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx


    def pay_bidbond(self):
        '''
        退投标保证金
        eg：
            退四川创佳暖通有限公司投标保证金
        >  【差了两个字】
        
        rule:
            1.借贷金额相同
            2.银行——对方户名：四川创佳暖通设备有限公司 
            3.银行——交易附言：退保证金-CC00000GBH.
        '''
        regex_pay_bidbond = re.compile(r'.*退.*投标保证金')
        is_pay_bidbond = (self.nc_abc['摘要'].str.match(regex_pay_bidbond))
        nc_pay_bidbond = self.nc_abc[is_pay_bidbond]
        
        for nc_idx in nc_pay_bidbond.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            abc_pay_bidbond = self.abc[(cond1)]

            for idx in abc_pay_bidbond.index:
                otherside_cond = (str(abc_pay_bidbond.loc[idx,"对方户名"]) in self.nc_abc.loc[nc_idx,'摘要'])
                substract_cond = ("保证金" in abc_pay_bidbond.loc[idx,'用途'])
                if otherside_cond and substract_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx

        for nc_idx in nc_pay_bidbond.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期'])
            abc_pay_bidbond = self.abc[(cond1&cond2)]

            for idx in abc_pay_bidbond.index:
                otherside_cond = (str(abc_pay_bidbond.loc[idx,"对方户名"]) in self.nc_abc.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx

    def pay_taxes(self):
        '''
        扣税
        eg:
            9.11 9月扣税
            2019-09-16交代扣个税
        
        rule:
            1. 借贷金额相同
            2. 交易时间相同
            3. 银行——用途：实时扣税请求（３００１）. 
                  ——对方户名：国家金库南充市顺庆区支库
        '''

        regex_pay_taxes = re.compile(r'.*月扣税.*|.*[扣]个税.*')
        is_pay_taxes = self.nc_abc['摘要'].str.match(regex_pay_taxes)
        nc_pay_taxes = self.nc_abc[is_pay_taxes]
        
        for nc_idx in nc_pay_taxes.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) # 交易时间相同
            abc_pay_taxes = self.abc[(cond1&cond2)]

            for idx in abc_pay_taxes.index:
                purpose_cond = (abc_pay_taxes.loc[idx,'用途'].startswith("实时扣税请求"))
                otherside_cond = (abc_pay_taxes.loc[idx,'对方户名'].startswith('国家金库'))
                if purpose_cond or otherside_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx


    def deal_laowang(self):
        '''
        处理王镜淇
        eg: 2019-08-05付王镜淇往来款
        
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——对方户名：王镜淇
        '''
        is_laowang = (self.nc_abc['摘要'].str.contains('王镜淇'))
        nc_laowang = self.nc_abc[is_laowang]
        
        for nc_idx in nc_laowang.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) #交易时间相同
            abc_laowang = self.abc[(cond1 & cond2)]

            for idx in abc_laowang.index:
                receiver_cond = (abc_laowang.loc[idx,"对方户名"] in self.nc_abc.loc[nc_idx,'摘要'])
                if receiver_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx                    
    
        for nc_idx in nc_laowang.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) #交易时间相同
            abc_laowang = self.abc[(cond1 & cond2)]

            for idx in abc_laowang.index:
                receiver_cond = (abc_laowang.loc[idx,"对方户名"] in self.nc_abc.loc[nc_idx,'摘要'])
                if receiver_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx


    def capital_pool(self):
        '''
        资金池归集——现有规则在金额相同时可能和付集团往来款匹配相交叉
        eg:资金池归集
        rule:
        1. 借贷金额相同 【NC<->银行：贷<->借】
        2. 银行——对方户名：领地集团股份有限公司
        3. 银行——交易用途：资金池归集-CC00000DKN.
        
        > 没有更好的规则，依赖金额的差异性；与付集团往来款基本相同,但集团往来款有时间字段进行约束。

        eg2:
        资金池归集收款

        rule2:
            1. 借贷金额相同 【NC<->银行：借<->贷】
            2. 银行——交易附言：资金池归集-CC00000G9O.
            3. 银行——对方户名：攀枝花领悦房地产开发有限公司【备用】

        eg3:
        资金池下拨

        rule3:
        1. 借贷金额相同
        2. 银行——交易附言：资金池下拨-CC00000G7S.
        3. 银行——对方户名：新疆兆龙诚祥房地产开发有限公司
        '''       
        is_capital_pool = (self.nc_abc['摘要'].str.strip().str.startswith('资金池归集'))
        nc_capital_pool = self.nc_abc[is_capital_pool]
        
        # rule1
        for nc_idx in nc_capital_pool.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            abc_capital_pool = self.abc[cond1]

            for idx in abc_capital_pool.index:
                purpose_cond = ('资金池归集' in  abc_capital_pool.loc[idx,"用途"])
                receiver_cond = (abc_capital_pool.loc[idx,"对方户名"].startswith('领地集团股份有限公司'))
                if purpose_cond and receiver_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx

        # rule2
        for nc_idx in nc_capital_pool.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            abc_capital_pool = self.abc[cond1]

            for idx in abc_capital_pool.index:
                purpose_cond = ('资金池归集' in  abc_capital_pool.loc[idx,"用途"])
                # receiver_cond = (abc_capital_pool.loc[idx,"对方户名"].startswith('领地集团股份有限公司'))
                if purpose_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx

        # rule3
        is_capital_pool_down = (self.nc_abc['摘要'].str.strip().str.startswith('资金池下拨'))
        nc_capital_pool_down = self.nc_abc[is_capital_pool_down]
        
        for nc_idx in nc_capital_pool_down.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            abc_capital_pool_down = self.abc[cond1]

            for idx in abc_capital_pool_down.index:
                purpose_cond = ('资金池下拨' in  abc_capital_pool_down.loc[idx,"用途"])
                # receiver_cond = (abc_capital_pool_down.loc[idx,"对方户名"].startswith('领地集团股份有限公司'))
                if purpose_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx

    def bank_transfer(self):
        '''
        跨行转账
        eg: 8.14中行6569到农行7857 <br>
        
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——交易行名：中国农业银行股份有限公司四川省分行清算中心
        '''
        regex_bank_transfer = re.compile(r'.*行\d{4}到.*行\d{4}$')
        is_bank_transfer = self.nc_abc['摘要'].str.match(regex_bank_transfer)
        nc_bank_transfer = self.nc_abc[is_bank_transfer]
        
        for nc_idx in nc_bank_transfer.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) #交易时间相同
            abc_bank_transfer = self.abc[(cond1 & cond2)]

            for idx in abc_bank_transfer.index:
                bank_cond = (abc_bank_transfer.loc[idx,"交易行名"].startswith('中国农业银行股份有限公司'))
                if bank_cond:
                    self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                    self.abc.loc[idx,'对账一致'] = 'yes'
                    self.nc_abc.loc[nc_idx,'银行索引'] = idx
                    self.abc.loc[idx,'NC索引'] = nc_idx

    def inner_transfer(self):
        '''
        内部转款
        eg:
        内部转账（10482~9037）
        9.4内部往来建行1260-农行9157
        2019-09-11内部转款华西0087-农行9157
        2019-09-20内部转款0087-9157

        
        rule:
            1. 借贷金额相同
            2. 交易时间相同
            3. 银行——账号：22432001040009157
            4. 银行——对方账号：2301170000000087
            3. 银行——交易附言: 往来款-CC00000GEL.【无时间时采用】

        '''
        regex_inner_transfer = re.compile(r'.*内部[转账帐款往来].*')
        is_inner_transfer = self.nc_abc['摘要'].str.match(regex_inner_transfer)
        nc_inner_transfer = self.nc_abc[is_inner_transfer]
        
        # rule1
        for nc_idx in nc_inner_transfer.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) # 交易时间相同
            abc_inner_transfer = self.abc[(cond1 & cond2)]
 
            for idx in abc_inner_transfer.index:
                bank_number = re.findall(r'(\d{4})-[^\d{2}].*(\d{4})', self.nc_abc.loc[nc_idx, '摘要'])  # [('10482', '9037')]
                if bank_number == []:
                    bank_number = re.findall(r'(\d{4})[-~—](\d{4})', self.nc_abc.loc[nc_idx, '摘要'])
                # print('1------:',bank_number)
                try:
                    ourside_cond1 = (str(abc_inner_transfer.loc[idx,"账号"]).endswith(bank_number[0][0]))
                    otherside_cond1 = (str(abc_inner_transfer.loc[idx,"对方账号"]).endswith(bank_number[0][1]))

                    ourside_cond2 = (str(abc_inner_transfer.loc[idx,"账号"]).endswith(bank_number[0][1]))
                    otherside_cond2 = (str(abc_inner_transfer.loc[idx,"对方账号"]).endswith(bank_number[0][0]))

                    if (ourside_cond1 and otherside_cond1) or (ourside_cond2 and otherside_cond2):
                        self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                        self.abc.loc[idx,'对账一致'] = 'yes'
                        self.nc_abc.loc[nc_idx,'银行索引'] = idx
                        self.abc.loc[idx,'NC索引'] = nc_idx
                except IndexError:
                    pass

        # rule1_
        for nc_idx in nc_inner_transfer.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.abc['交易日期']==self.nc_abc.loc[nc_idx,'交易日期']) # 交易时间相同            
            abc_inner_transfer = self.abc[(cond1&cond2)]

            for idx in abc_inner_transfer.index:
                bank_number = re.findall( r'(\d{4})-[^\d{2}].*(\d{4})', self.nc_abc.loc[nc_idx, '摘要'])  # [('10482', '9037')]
                if bank_number == []:
                    bank_number = re.findall(r'(\d{4})[-~—](\d{4})', self.nc_abc.loc[nc_idx, '摘要'])
                # print('2------:', bank_number)
                try:
                    ourside_cond1 = (str(abc_inner_transfer.loc[idx,"账号"]).endswith(bank_number[0][0]))
                    otherside_cond1 = (str(abc_inner_transfer.loc[idx,"对方账号"]).endswith(bank_number[0][1]))

                    ourside_cond2 = (str(abc_inner_transfer.loc[idx,"账号"]).endswith(bank_number[0][1]))
                    otherside_cond2 = (str(abc_inner_transfer.loc[idx,"对方账号"]).endswith(bank_number[0][0]))

                    if (ourside_cond1 and otherside_cond1) or (ourside_cond2 and otherside_cond2):
                        self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                        self.abc.loc[idx,'对账一致'] = 'yes'
                        self.nc_abc.loc[nc_idx,'银行索引'] = idx
                        self.abc.loc[idx,'NC索引'] = nc_idx
                except IndexError:
                    pass

        # rule2:无时间                    
        for nc_idx in nc_inner_transfer.index:
            cond1 = (self.abc['收入']==self.nc_abc.loc[nc_idx,'借方']) #借贷金额相同    
            cond2 = (self.abc['用途'].str.contains('往来款'))
            abc_inner_transfer = self.abc[(cond1&cond2)]

            for idx in abc_inner_transfer.index:
                bank_number = re.findall(r'(\d{4})-[^\d{2}].*(\d{4})', self.nc_abc.loc[nc_idx, '摘要'])  # [('10482', '9037')]
                if bank_number == []:
                    bank_number = re.findall(r'(\d{4})[-~—](\d{4})', self.nc_abc.loc[nc_idx, '摘要'])
                # print('3------:', bank_number)
                try:
                    ourside_cond1 = (str(abc_inner_transfer.loc[idx,"账号"]).endswith(bank_number[0][0]))
                    otherside_cond1 = (str(abc_inner_transfer.loc[idx,"对方账号"]).endswith(bank_number[0][1]))

                    ourside_cond2 = (str(abc_inner_transfer.loc[idx,"账号"]).endswith(bank_number[0][1]))
                    otherside_cond2 = (str(abc_inner_transfer.loc[idx,"对方账号"]).endswith(bank_number[0][0]))

                    if (ourside_cond1 and otherside_cond1) or (ourside_cond2 and otherside_cond2):
                        self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                        self.abc.loc[idx,'对账一致'] = 'yes'
                        self.nc_abc.loc[nc_idx,'银行索引'] = idx
                        self.abc.loc[idx,'NC索引'] = nc_idx
                except IndexError:
                    pass                       

        # rule2_:无时间                    
        for nc_idx in nc_inner_transfer.index:
            cond1 = (self.abc['支出']==self.nc_abc.loc[nc_idx,'贷方']) #借贷金额相同    
            cond2 = (self.abc['用途'].str.contains('往来款'))
            abc_inner_transfer = self.abc[(cond1&cond2)]

            for idx in abc_inner_transfer.index:
                bank_number = re.findall(r'(\d{4})-[^\d{2}].*(\d{4})', self.nc_abc.loc[nc_idx, '摘要'])  # [('10482', '9037')]
                if bank_number == []:
                    bank_number = re.findall(r'(\d{4})[-~—](\d{4})', self.nc_abc.loc[nc_idx, '摘要'])
                # print('4------:', bank_number)
                try:
                    ourside_cond1 = (str(abc_inner_transfer.loc[idx,"账号"]).endswith(bank_number[0][0]))
                    otherside_cond1 = (str(abc_inner_transfer.loc[idx,"对方账号"]).endswith(bank_number[0][1]))

                    ourside_cond2 = (str(abc_inner_transfer.loc[idx,"账号"]).endswith(bank_number[0][1]))
                    otherside_cond2 = (str(abc_inner_transfer.loc[idx,"对方账号"]).endswith(bank_number[0][0]))

                    if (ourside_cond1 and otherside_cond1) or (ourside_cond2 and otherside_cond2):
                        self.nc_abc.loc[nc_idx,'对账一致'] = 'yes'
                        self.abc.loc[idx,'对账一致'] = 'yes'
                        self.nc_abc.loc[nc_idx,'银行索引'] = idx
                        self.abc.loc[idx,'NC索引'] = nc_idx
                except IndexError:
                    pass  

    def export_excel(self):

        nc_rows_counts = self.nc_abc['对账一致'].value_counts(dropna=False)
        abc_rows_counts = self.abc['对账一致'].value_counts(dropna=False)

        try:
            nc_yes_rows = nc_rows_counts['yes']
        except KeyError:
            nc_yes_rows = 0
        nc_notmatch_rows = nc_rows_counts.sum()-nc_yes_rows

        try:
            abc_yes_rows = abc_rows_counts['yes']
        except KeyError:
            abc_yes_rows = 0
        abc_notmatch_rows = abc_rows_counts.sum()-abc_yes_rows

        print('\n')
        print("+--------------------------------------------------+")
        print("¦                  RESULTS                         ¦")
        print("+--------------------------------------------------+")
        print("¦ EXCEL    ¦       NC_ABC     ¦         ABC        ¦")
        print("+--------------------------------------------------+")
        print("¦ TOTAL    ¦{0:^18}¦{1:^20}¦".format(nc_rows_counts.sum(),abc_rows_counts.sum()))
        print("+--------------------------------------------------+")
        print("¦ MATCH    ¦{0:^18}¦{1:^20}¦".format(nc_yes_rows,abc_yes_rows))
        print("+--------------------------------------------------+")
        print("¦ NOTMATCH ¦{0:^18}¦{1:^20}¦".format(nc_notmatch_rows,abc_notmatch_rows))
        print("+--------------------------------------------------+")
        print('\n')


        self.nc_abc['交易日期'] = self.nc_abc['交易日期'].astype(str).str.slice(0,10)
        self.abc['交易日期'] = self.abc['交易日期'].astype(str).str.slice(0,10)

        
        save_file = self.save_path + '\\' + self.nc_file_name + '+' + self.abc_file_name + '.xlsx'
        print("结果保存至:\n\t%s\n" %(save_file))
        # self.nc_abc.to_excel(self.save_path + '/nc_abc.xlsx')
        # self.abc.to_excel(self.save_path + '/abc.xlsx')
        writer = pd.ExcelWriter(save_file,engine='xlsxwriter')
        self.nc_abc.to_excel(writer,sheet_name=self.nc_file_name,startrow=1,startcol=1,header=False,index=False)
        self.abc.to_excel(writer,sheet_name=self.abc_file_name,startrow=1,startcol=1,header=False,index=False)
        
        workbook = writer.book
        nc_sheet = writer.sheets[self.nc_file_name]
        abc_sheet = writer.sheets[self.abc_file_name]

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
        
        nc_rows,nc_cols = self.nc_abc.shape
        for i in range(nc_rows+5):
            nc_sheet.set_row(i,22,cell_format)

        yes_index = self.nc_abc[self.nc_abc['对账一致']=='yes'].index+1
        for i in yes_index:
            nc_sheet.set_row(i,22,yes_format)

        # col format
        nc_sheet.set_column(0,nc_cols+5,22)

        nc_sheet.write_row('B1',self.nc_abc.columns,header_format)
        nc_sheet.write_column('A2',self.nc_abc.index,header_format)
        nc_sheet.freeze_panes(1,1)
        nc_sheet.set_tab_color('#FF9900')

        #abc
        # row format
        abc_rows,abc_cols = self.abc.shape
        for i in range(abc_rows+5):
            abc_sheet.set_row(i,22,cell_format)

        yes_index = self.abc[self.abc['对账一致']=='yes'].index+1
        for i in yes_index:
            abc_sheet.set_row(i,22,yes_format)

        # col format
        abc_sheet.set_column(0,abc_cols+5,22)

        abc_sheet.write_row('B1',self.abc.columns,header_format)
        abc_sheet.write_column('A2',self.abc.index,header_format)
        abc_sheet.freeze_panes(1,1)
        abc_sheet.set_tab_color('#FF9900')

        writer.save()

    def doall(self):
        self.rec_firmloans()
        self.rec_pos()
        self.rec_register_capital()
        self.rec_mortgage()
        self.rec_pfund()
        self.rec_group()
        self.rec_firmpfund()
        self.rec_firmamount()
        self.rec_buildingamount()
        self.rec_return_loans()
        self.rec_bidbond()

        self.pay_group()
        self.save_rfund()
        self.pay_pending()
        self.pay_salary()
        self.pay_refund()
        self.pay_certificate_fee()
        self.pay_loans()
        self.pay_reimburse()
        self.pay_interest()
        self.pay_flatcost()
        self.prepay_firmamount()
        self.pay_fall()
        self.pay_progressamount()
        self.pay_ssfund()
        self.pay_bankfee()
        self.pay_land()
        self.pay_firmamount()
        self.pay_bidbond()
        self.pay_taxes()
        self.deal_laowang()
        self.capital_pool()
        self.bank_transfer()
        self.inner_transfer()
        self.export_excel()


    def __call__(self):
        return self.doall()
