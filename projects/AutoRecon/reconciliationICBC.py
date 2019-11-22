#!/usr/bin/env python
# coding: utf-8
# 工行对账
import pandas as pd
import numpy as np
import re


# nc_path =  "D:/Leadingworks/totalAccounts/对账规则/NCTEST.xlsx"
# bank_path =  "D:/Leadingworks/totalAccounts/对账规则/ICBCTEST.xlsx"

# 整理NC表
class DealExcelICBC(object):
    def __init__(self,nc_path,bank_path):
        self.nc_path = nc_path
        self.bank_path = bank_path

    def dealNC(self):
        # read
        nc_icbc = pd.read_excel(self.nc_path,header=None)
        nc_icbc = nc_icbc.dropna(how='all')

        # deal year/head/tail
        year = nc_icbc.iloc[0,0]
        init_period = nc_icbc.iloc[2,:] # 暂时保存期初行
        month_year_sum = nc_icbc.tail(2) # 暂时保存本月及本年累计行

        # drop useless rows
        nc_icbc.columns = nc_icbc.iloc[1,:] 
        nc_icbc = nc_icbc.drop([0,1,2]) 
        nc_icbc = nc_icbc.head(len(nc_icbc)-2)

        time = str(year) + '-' + nc_icbc['月'].astype(str) + '-' + nc_icbc['日'].astype(str)
        nc_icbc.insert(0,'日期',pd.to_datetime(time,format='%Y-%m-%d').astype(str).str.slice(0,10))

        nc_icbc.reset_index(drop=True,inplace=True)

        # 提取交易时间
        time_pattern1 = re.compile(r'\d{4}-\d+-\d+')
        time_pattern2 = re.compile(r'\d{4}\.\d+\.\d+')
        time_pattern3 = re.compile(r'\d+\.\d+')

        transac_time = nc_icbc['摘要'].copy()
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

        # print(transac_time)
        nc_icbc.insert(6,'交易日期',transac_time)
        nc_icbc['交易日期']=pd.to_datetime(transac_time,format='%Y-%m-%d')

        # 生成对账标记
        nc_icbc.insert(0,'银行索引',None)
        nc_icbc.insert(0,'对账一致',None)

        # 转换字段类型
        nc_icbc.columns = list(map(lambda x: str(x).strip(),nc_icbc.columns))
        nc_icbc.loc[:,['银行账户名称','摘要']] = nc_icbc[['银行账户名称','摘要']].apply(lambda s: s.str.strip().str.replace('[ （）()]',''))
        nc_icbc.loc[:,['借方','贷方','余额']] = nc_icbc[['借方','贷方','余额']].apply(lambda s: s.astype(np.float64))

        nc_icbc.drop(['月','日'],axis=1,inplace=True)

        return nc_icbc

    def dealBANK(self):
        # read
        icbc = pd.read_excel(self.bank_path,header=None)
        icbc = icbc.dropna(how='all')

        if icbc.iloc[0,0]=='组织':
            icbc.columns = icbc.loc[0,:]
            icbc = icbc.drop(0)

            need_fields = ["组织","银行","账号","对方账号","币种","交易日期","收入","支出","当前余额",  
                           "用途","对方户名","对方行号","备注","附言","回单个性化信息","来源","业务类型","资金系统单据号",]
            for col in need_fields:
                if col not in icbc.columns:
                    icbc[col] = None
            icbc['交易日期'] = pd.to_datetime(icbc['交易日期'])

            strip_fields = ["组织","账号","币种","用途","对方户名","备注","业务类型"]
            icbc.loc[:,strip_fields] = icbc[strip_fields].apply(lambda s: s.str.strip().str.replace('[ （）()]','')) 

        else:
            # drop useless rows
            for row in icbc.index:
                for col in icbc.columns:
                    if str(icbc.loc[row,col]).strip()=='交易时间':
                        header_row = row
            #             print(header_row)
                        break
            icbc.columns = icbc.loc[header_row,:]
            icbc = icbc.loc[header_row+1:,:]
            
            
            # transform columns
            icbc.columns = list(map(lambda x: str(x).strip(),icbc.columns))

            if "本方账号" not in icbc.columns:
                icbc['本方账号'] = None
            if "余额" not in icbc.columns:
                icbc['余额'] = None

            rename_dict = {
                "本方账号":"账号",
                "交易时间": "交易日期",
                "贷方发生额": "收入", 
                "借方发生额": "支出",
                "转入金额": "收入",
                "转出金额": "支出",
                "对方单位": "对方户名",
                "对方单位名称": "对方户名",
                "余额":"当前余额",
                "用途":"备注",
                "摘要":"用途",
            }
            icbc.rename(columns=rename_dict,inplace=True)

            icbc['交易日期'] = pd.to_datetime(icbc['交易日期'].str.slice(0,10),format="%Y-%m-%d")

            icbc["银行"] = 'ICBC-工商银行'
            icbc["来源"] = 'U-ICBC'
            icbc['币种'] = 'CNY-人民币'
            icbc['业务类型'] = None
            icbc['资金系统单据号'] = None
            icbc['组织'] = None

            # try:
            #     icbc.loc[:,'备注'] = icbc[['用途_ICBC','附言','回单个性化信息']].fillna('').sum(1)
            # except KeyError:
            #     icbc.loc[:,'备注'] = icbc[['用途_ICBC','个性化信息']].fillna('').sum(1)

            # drop useless columns           
            need_fields = ["组织","银行","账号","对方账号","币种","交易日期","收入","支出","当前余额", "用途",
            "对方户名","对方行号","备注","附言","个性化信息","回单个性化信息","来源","业务类型","资金系统单据号",]
            for col in need_fields:
                if col not in icbc.columns:
                    icbc[col] = None
            icbc = icbc[need_fields]            

            # strip and transform type
            strip_fields = ["组织","账号","币种","用途","对方户名","备注","业务类型"]
            icbc.loc[:,strip_fields] = icbc[strip_fields].apply(lambda s: s.str.strip().str.replace('[ （）()]',''))

        icbc.insert(0,"NC索引",None)
        icbc.insert(0,'对账一致',None)
        icbc.reset_index(inplace=True)
        icbc.sort_values(['index'])
        icbc.drop(['index'],axis=1,inplace=True)
        
        num_fields = ['收入','支出','当前余额']
        icbc.loc[:,num_fields] = icbc[num_fields].apply(lambda s: s.replace({'-':None}).str.replace(',','').astype(np.float64))

        return icbc

# 对账规则

class CheckICBC(object):
    def __init__(self,nc_icbc,icbc,nc_file_name,icbc_file_name,save_path=None):
        self.nc_icbc = nc_icbc
        self.icbc = icbc
        self.nc_file_name = nc_file_name
        self.icbc_file_name = icbc_file_name
        self.save_path = save_path
   

    # income items 
    def rec_mortgage(self):
        '''
        收取银行按揭
        eg：2019-08-01收刘文强[眉山]蘭台府-蘭台府一期-12-603银行按揭<br>
        
        rule:<br>
        
        1. NC<->银行：借贷金额相同
        2. 交易时间相同
        3. 银行——对方单位: 刘文强
        '''
        regex_mortgage = re.compile(r'.*收.*银行按揭$')
        is_mortgage = self.nc_icbc['摘要'].str.match(regex_mortgage)
        nc_mortgage = self.nc_icbc[is_mortgage]

        for nc_idx in nc_mortgage.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']== self.nc_icbc.loc[nc_idx,'交易日期']) #交易时间相同
            icbc_mortgage = self.icbc[(cond1 & cond2)]
        
            for idx in icbc_mortgage.index:
                if icbc_mortgage.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要']: # 对方单位为 nc摘要中的姓名
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx 
    
    def rec_pfund(self):
        '''
        收取公积金
        eg: 2019-08-02收管齐意[眉山]蘭台府-蘭台府一期-01-1004公积金
        rule1: 
        > 逐笔比对
        
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——对方单位名称：姓名/个人住房公积金委托贷款资金-个人住房公积金委托贷款资金
        
        rule2:
        > nc中为多笔金额，工行中为汇总数
        
        1. 汇总NC中收取的公积金
        2. 交易时间相同
        3. 银行——对方单位: 个人住房公积金委托贷款资金-个人住房公积金委托贷款资金
        4. NC汇总数=银行金额
        '''
        # rule1
        regex_pfund = re.compile(r'.*收.*公积金$')
        is_pfund = self.nc_icbc['摘要'].str.match(regex_pfund)
        nc_pfund = self.nc_icbc[is_pfund]
        
        for nc_idx in nc_pfund.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']== self.nc_icbc.loc[nc_idx,'交易日期']) #交易时间相同
            icbc_pfund = self.icbc[(cond1 & cond2)]

            for idx in icbc_pfund.index:
                if icbc_pfund.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要']: # 对方单位为 nc摘要中的姓名
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx 
                    
                elif icbc_pfund.loc[idx,'对方户名']=="个人住房公积金委托贷款资金-个人住房公积金委托贷款资金":
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx 

        # rule2
        total_pfund = nc_pfund['借方'].sum()
        
        cond1 = (self.icbc['收入']==total_pfund) #借贷金额相同
        try:
            cond2 = (self.icbc['交易日期']== nc_pfund['交易日期'][0]) #交易时间相同
            icbc_pfund = self.icbc[(cond1&cond2)]
        except (IndexError,KeyError): #nc_pfund 为 empty df
            icbc_pfund = self.icbc[cond1]
            
        for idx in icbc_pfund.index:
            if icbc_pfund.loc[idx,'对方户名']=="个人住房公积金委托贷款资金-个人住房公积金委托贷款资金":
                self.nc_icbc.loc[nc_pfund.index,'对账一致'] = 'yes'
                self.icbc.loc[idx,'对账一致'] = 'yes'
                self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                self.icbc.loc[idx,'NC索引'] = ';'.join(map(str,nc_pfund.index.values))
        
    def rec_buildingamount(self):
        '''
        收楼款/楼款转入
        eg1:2019-08-11收杜玉祥[眉山]蘭台府-蘭台府一期-01-801楼款
        rule1:
        > 逐笔比对
        
        1. 借贷金额相同
        2. 银行——对方单位：杜玉祥
        3. 交易时间相同
        
        <br>
        eg2: 2019-08-30收薛梅[乐山]领地澜山-一期-4号楼-1-301楼款
        
        rule2:
        > nc为单笔金额,银行为多笔金额
        
        1. 交易时间相同
        2. 银行——对方单位:薛梅
        3. 汇总银行金额
        4. nc金额=汇总银行金额
        
        <br>
        eg3: 2019-08-12[眉山]凯旋国际公馆-凯旋府二期-10号楼-3301熊朝刚楼款转入，新票据A0036062
        rule3:
        
        1. 借贷金额相同
        2. 银行——对方单位：熊朝刚
        3. 交易时间相同 【此例银行时间为 2019-08-11,则匹配不上】
        '''

        regex_rec_buildingamount = re.compile(r'.*收.*楼款.*$|.*楼款转入.*')
        is_rec_buildingamount = self.nc_icbc['摘要'].str.match(regex_rec_buildingamount)
        nc_rec_buildingamount = self.nc_icbc[is_rec_buildingamount]
        
        # rule1
        for nc_idx in nc_rec_buildingamount.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期']) #交易时间相同
            icbc_rec_buildingamount = self.icbc[(cond1 & cond2)]

            for idx in icbc_rec_buildingamount.index:
                if icbc_rec_buildingamount.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要']: # 对方单位为 nc摘要中的姓名
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     
        
        # rule2
        for nc_idx in nc_rec_buildingamount.index:
            time_cond = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期'])
            icbc_rec_buildingamount = self.icbc[time_cond]
            icbc_idxs = []
            for idx in icbc_rec_buildingamount.index:
                if icbc_rec_buildingamount.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要']:
                    icbc_idxs.append(idx)
            if self.icbc.loc[icbc_idxs,'收入'].sum() == self.nc_icbc.loc[nc_idx,'借方']:
                self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                self.icbc.loc[icbc_idxs,'对账一致'] = 'yes'
                self.nc_icbc.loc[nc_idx,'银行索引'] = ';'.join(map(str,icbc_idxs))
                self.icbc.loc[icbc_idxs,'NC索引'] = nc_idx                 

    def rec_pos(self):
        '''
        POS到账
        eg:  
        0801-0801POS到账<br>
        2019-08-27 2253pos到账/8.28pos到账
        
        rule1:
        > 没有日期的情况[注意大小写]
        
        1. NC<->银行：借贷金额相同
        2. 银行——摘要：0801-0801费0元 【数字匹配】
        3. 银行——对方单位: 银联商务股份有限公司客户备付金 
    
        rule2:
        > 有日期的情况[注意大小写]
        
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——摘要：0826-0826费0元/0827-0827费0元 【排不上用处了】
        4. 银行——对方单位: 银联商务股份有限公司客户备付金 
        '''
        regex_pos = re.compile(r'.*POS到账',flags=re.I)
        is_pos = self.nc_icbc['摘要'].str.match(regex_pos)
        nc_pos = self.nc_icbc[is_pos]
                     
        # rule1
        for nc_idx in nc_pos.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.icbc['对方户名']=='银联商务股份有限公司客户备付金') # 对方单位名
            icbc_pos = self.icbc[(cond1 & cond2)]

            for idx in icbc_pos.index:
                nc_substract_cond = (re.findall(r'\d+-\d+',self.nc_icbc.loc[nc_idx,'摘要']))
                icbc_substract_cond = (re.findall(r'\d+-\d+',str(icbc_pos.loc[idx,'用途'])))

                if  nc_substract_cond == icbc_substract_cond: 
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     
        
        # rule2
        for nc_idx in nc_pos.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期'])
            icbc_pos = self.icbc[(cond1 & cond2)]
        
            for idx in icbc_pos.index:
                otherside_cond = (self.icbc.loc[idx,'对方户名']=='银联商务股份有限公司客户备付金') # 对方单位名
                if otherside_cond: 
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     
    
    def rec_loans(self):
        '''
        收到归还借款
        eg：收到lifei-李菲归还F0403-因公临时借款
        
        rule：
        1. 借贷金额相同
        2. 银行——对方单位：姓名/公司名
        '''
        regex_rec_loans = re.compile(r'收到.*归还.*借款$|收到.*归还.*借款\w.*')
        is_rec_loans = self.nc_icbc['摘要'].str.match(regex_rec_loans)
        nc_rec_loans = self.nc_icbc[is_rec_loans]
        
        for nc_idx in nc_rec_loans.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
            icbc_rec_loans = self.icbc[cond1]

            for idx in icbc_rec_loans.index:
                otherside_cond = (icbc_rec_loans.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要'])
                if otherside_cond: # 对方单位为 nc摘要中的姓名
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx 

    def rec_deposit(self):
        '''
        收取定金
        eg: 2019-08-19收陈丽彬;沈世荣[眉山]凯旋国际公馆-凯旋府二期-14号楼-2-301定金A0036157<br>
        > 有部分匹配不上，因为摘要的时间和银行的时间不一致,摘要事项不同也无法利用;如遇同名依赖金额的差异性
        
        rule:<br>
        1. 借贷金额相同
        2. <del>交易时间相同</del>
        3. 银行——对方单位：陈丽彬
        '''    
        regex_rec_deposit = re.compile(r'.*收.*定金.*')
        is_rec_deposit = self.nc_icbc['摘要'].str.match(regex_rec_deposit)
        nc_rec_deposit = self.nc_icbc[is_rec_deposit]
        
        for nc_idx in nc_rec_deposit.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
        #     cond2 = (self.icbc['交易时间']==self.nc_icbc.loc[nc_idx,'交易时间']) #交易时间相同
            icbc_rec_deposit = self.icbc[(cond1)]

            for idx in icbc_rec_deposit.index:
                if icbc_rec_deposit.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要']:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def rec_refund(self):
        '''
        收取预约金
        eg: 2019-08-05收周静涵预约金 <br>
        > 有部分匹配不上，因为摘要的时间和银行的时间不一致,摘要事项不同也无法利用;如遇同名依赖金额的差异性
        
        rule1:
        > 逐条比对
        
        1. 借贷金额相同
        2. <del>交易时间相同</del>
        3. 银行——对方单位：周静涵
        
        eg: <br>
        nc——2019-08-16收周雪冰预约金
        
        bank——
        
        |对方单位   |摘要 |       发生额|
        |---|---|---|
        |周雪冰        |车位付款       |50,000.00|
        |周雪冰        |车位款项       |20,157.00|
        |周雪冰        |跨行          |900|
        
        rule2:
        > 汇总比对
        
        1. 银行——对方单位：周雪冰
        2. 汇总银行金额
        3. nc借方金额=2
        '''

        regex_rec_refund = re.compile(r'.*收.*预约金$')
        is_rec_refund = self.nc_icbc['摘要'].str.match(regex_rec_refund)
        nc_rec_refund = self.nc_icbc[is_rec_refund]
        
        # rule1
        for nc_idx in nc_rec_refund.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
        #     cond2 = (icbc['交易时间']==self.nc_icbc.loc[nc_idx,'交易时间']) #交易时间相同
            icbc_rec_refund = self.icbc[(cond1)]

            for idx in icbc_rec_refund.index:
                if icbc_rec_refund.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要']:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

        # rule2
        for nc_idx in nc_rec_refund.index:
            icbc_idxs = []
            for idx in self.icbc.index:
                if str(self.icbc.loc[idx,'对方户名']) in self.nc_icbc.loc[nc_idx,'摘要']:
                    icbc_idxs.append(idx)
            icbc_rec_refund = self.icbc.loc[icbc_idxs]
            icbc_rec_refund_sum = icbc_rec_refund['收入'].sum()

            amount_cond = (icbc_rec_refund_sum==self.nc_icbc.loc[nc_idx,'借方'])
            if amount_cond:
                self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                self.icbc.loc[icbc_idxs,'对账一致'] = 'yes'
                self.nc_icbc.loc[nc_idx,'银行索引'] = ';'.join(map(str,icbc_idxs))
                self.icbc.loc[icbc_idxs,'NC索引'] = nc_idx      

    def rec_prefbond(self):
        '''
        收履约保证金
        eg:收四川万象园林景观工程有限公司三期一批次园林工程履约保证金<br>
        rule:
        1. 借贷金额相同
        2. 银行——摘要：履约保证金
        2_. 交易时间相同
        3. 银行——对方单位: 四川万象园林景观工程有限公司
        '''
        
        regex_rec_perfbond = re.compile(r'.*收.*履约保证金.*')
        is_rec_perfbond = self.nc_icbc['摘要'].str.match(regex_rec_perfbond)
        nc_rec_perfbond = self.nc_icbc[is_rec_perfbond]

        for nc_idx in nc_rec_perfbond.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
            icbc_rec_perfbond = self.icbc[(cond1)]

            for idx in icbc_rec_perfbond.index:
                substract_cond = ('履约保证金' in icbc_rec_perfbond.loc[idx,'用途'])
                otherside_cond = (icbc_rec_perfbond.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要'])
                if substract_cond and otherside_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx

        for nc_idx in nc_rec_perfbond.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期']) #借贷金额相同
            icbc_rec_perfbond = self.icbc[(cond1&cond2)]

            for idx in icbc_rec_perfbond.index:
                otherside_cond = (icbc_rec_perfbond.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                                       

    def rec_group(self):
        '''
        收集团往来款
        eg: 2019-08-14收集团往来款<br>
        rule:
        1. 借贷金额相同
        2. 银行——摘要:资金池下拨-CC00000ET   
        3. 银行——对方单位名称:领地集团股份有限公司
        4. 交易时间相同
        '''
        
        is_rec_group = self.nc_icbc['摘要'].str.contains('收集团往来款')
        nc_rec_group = self.nc_icbc[is_rec_group]

        for nc_idx in nc_rec_group.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期']) #交易时间相同
            icbc_rec_group = self.icbc[(cond1 & cond2)]

            for idx in icbc_rec_group.index:
                purpose_cond = (icbc_rec_group.loc[idx,'用途'].startswith('资金池下拨'))
                otherside_cond = (icbc_rec_group.loc[idx,'对方户名'].startswith('领地集团股份有限公司'))
                if purpose_cond and otherside_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def rec_firmamount(self):
        '''
        收公司往来款
        eg: 2019-08-05收到乐山华汇达往来款
             /8.22收建业往来款
        
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——对方单位：乐山华汇达房地产开发有限公司
        '''
        regex_rec_firmamount = re.compile(r'.*收.*[^集团]往来款')
        is_rec_firmamount = self.nc_icbc['摘要'].str.match(regex_rec_firmamount)
        nc_rec_firmamount = self.nc_icbc[is_rec_firmamount]

        for nc_idx in nc_rec_firmamount.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期']) # 交易时间相同
            icbc_rec_firmamount = self.icbc[(cond1 & cond2)]

            for idx in icbc_rec_firmamount.index:
                payer_cond = (icbc_rec_firmamount.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要']) #对方单位 
                if payer_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx 
    
    # payments
    def save_rfund(self):
        '''
        存监管资金
        eg：2019-08-01工行1862存监管资金
        
        rule:
        1. NC<->银行：贷借金额相同
        2. 交易时间相同
        3. 银行——摘要：监管资金
        '''
        regex_rfund = re.compile(r'.*行.*存.*监管资金') #regulatory fund
        is_rfund = self.nc_icbc['摘要'].str.match(regex_rfund)
        nc_rfund = self.nc_icbc[is_rfund]
        
        for nc_idx in nc_rfund.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期'])
            icbc_rfund = self.icbc[(cond1 & cond2)]

            for idx in icbc_rfund.index:
                if icbc_rfund.loc[idx,'用途'] == '监管资金': # 摘要为 '监管资金'
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def pay_refund(self):
        '''
        退待退款项/预约金
        eg：2019-08-02退徐强[眉山]蘭台府-蘭台府一期-01-1701待退款项<br>
            2019-08-02退周霞;彭东祥预约金 <br>
        > 有部分匹配不上，因为摘要的时间和银行的时间不一致,暂以摘要为约束条件
        
        rule:
        1. 贷借金额相同
        2. <del>交易时间相同</del>
        3. 银行——对方单位：徐强/彭东祥
        4. 银行——摘要：退房款/退预约金/退定金
        '''
        # 摘要
        regex_appointment_refund = re.compile(r'.*退.*待退款项$|.*退.*预约金')
        is_appointment_refund = self.nc_icbc['摘要'].str.match(regex_appointment_refund)
        nc_appointment_refund = self.nc_icbc[is_appointment_refund]
               
        for nc_idx in nc_appointment_refund.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
        #     cond2 = (icbc['交易日期']==nc_icbc.loc[nc_idx,'交易日期']) #交易时间相同
            icbc_appointment_refund = self.icbc[(cond1)]

            for idx in icbc_appointment_refund.index:
                receiver_cond = (icbc_appointment_refund.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要']) # 对方单位为 nc摘要中的姓名
                substract_cond = (re.search('退预约金|退定金|退房款',str(icbc_appointment_refund.loc[idx,'用途'])))
                                  
                if receiver_cond and substract_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     
        
        # 时间
        for nc_idx in nc_appointment_refund.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期']) #交易时间相同
            icbc_appointment_refund = self.icbc[(cond1)]

            for idx in icbc_appointment_refund.index:
                otherside_cond = (icbc_appointment_refund.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要']) # 对方单位为 nc摘要中的姓名
                if otherside_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx        


    def pay_loans(self):
        '''
        支付借款
        eg：<br>
            支付lilin2-李琳借F0402-营销活动借款<br>
            支付wangjq01-王镜淇借F0403-因公临时借款
        
        rule:
        1. 金额相同
        2. 银行—对方单位：李琳/王镜淇
        '''
            
        regex_pay_loans = re.compile(r'支付.*借.*借款$|支付.*借.*借款\w.*')
        is_pay_loans = self.nc_icbc['摘要'].str.match(regex_pay_loans)
        nc_pay_loans = self.nc_icbc[is_pay_loans]
        
        for nc_idx in nc_pay_loans.index:
            cond1 = (self.icbc['支出'] == self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            icbc_pay_loans = self.icbc[(cond1)]

            for idx in icbc_pay_loans.index:
                otherside_cond = (icbc_pay_loans.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要'])
                if otherside_cond: # 对方单位为 nc摘要中的姓名
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def pay_reimburse(self):
        '''
        支付报销款
        eg:<br>
        支付zhanghy-张洪英报销F0108-业务接待费款<br>
        支付1020302013-中国电信股份有限公司眉山分公司报销F030704-其他销售费用-电话费/光纤网络费款<br>
        rule:<br>
        1. 借贷金额相同
        2. 对方单位：张洪英/中国电信股份有限公司眉山分公司
        '''
        regex_pay_reimburse = re.compile(r'支付.*报销.*款$|支付.*报销.*款\w.*')
        is_pay_reimburse = self.nc_icbc['摘要'].str.match(regex_pay_reimburse)
        nc_pay_reimburse = self.nc_icbc[is_pay_reimburse]

        for nc_idx in nc_pay_reimburse.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            icbc_pay_reimburse = self.icbc[cond1]

            for idx in icbc_pay_reimburse.index:
                otherside_cond = (icbc_pay_reimburse.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要'])
                if otherside_cond: # 对方单位为 nc摘要中的姓名/公司
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes' 
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     
    
    def prepay_firmamount(self):
        '''
        预付公司款项/支付公司预付款
        eg:<br>
        预付2910102-成都京东世纪贸易有限公司F030207 -已成交客户回馈款<br>
        预付2910102-成都京东世纪贸易有限公司F020202-生日款<br>
        预付00001043-国网四川省电力公司眉山供电公司F01050203-工程类水电费款<br>
        支付迅达（中国）电梯有限公司乐山领地澜山项目二期电梯采购及安装工程施工合同预付款
        
        rule:
        1. 借贷金额相同
        2. 银行——对方单位：成都京东世纪贸易有限公司/国网四川省电力公司眉山供电公司/迅达（中国）电梯有限公司
        '''
        
        regex_prepay_firm_amount = re.compile(r'预付.*公司.*款|支付.*公司.*预付款')
        is_prepay_firm_amount = self.nc_icbc['摘要'].str.match(regex_prepay_firm_amount)
        nc_prepay_firm_amount = self.nc_icbc[is_prepay_firm_amount]
        
        for nc_idx in nc_prepay_firm_amount.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            icbc_prepay_firm_amount = self.icbc[(cond1)]

            for idx in icbc_prepay_firm_amount.index:
                receiver_cond = icbc_prepay_firm_amount.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要'] # 对方单位是 nc摘要中的公司
                if receiver_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def pay_fee(self):
        '''
        支付手续费
        eg: <br>
        
        nc——
        
        |    摘要  |对方科目 |	借方| 贷方 |
        |---------|---------|-------|-----|
        |2253手续费|	1		|339.56 |     |
        |2253手续费|	1		|9      |     |
        |2253手续费|	1		|2853.40|     |
        
        bank——
        
        |借贷标志 |    摘要       |   发生额 |
        |--------|---------------|---------|
        |借      | 对公收费明细入帐| 9       |
        |借      | 7月手续费      | 2,853.40|
        |借      | 询征函手续费   | 200     |
        
        rule:
        1. 借贷金额相同
        2. 银行——摘要：含"手续费"或为"对公收费明细入账/帐"
        '''   
        is_pay_fee = self.nc_icbc['摘要'].str.contains('[^网银]手续费')
        nc_pay_fee = self.nc_icbc[is_pay_fee]

        for nc_idx in nc_pay_fee.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            icbc_pay_fee = self.icbc[(cond1)]

            for idx in icbc_pay_fee.index:
                substract_cond1 = ('手续费' in str(icbc_pay_fee.loc[idx,'用途']))
                substract_cond2 = (icbc_pay_fee.loc[idx,'用途']=="对公收费明细入账")
                substract_cond3 = (icbc_pay_fee.loc[idx,'用途']=="对公收费明细入帐")
                if (substract_cond1 or substract_cond2 or substract_cond3):
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     
    
    def pay_bankfee(self):
        '''        
        支付网银手续费
        eg：7月企业网银手续费<br>
        rule:<br>
        1. 借贷金额相同
        2. 双方摘要：包含"网银手续费"
        '''
        is_pay_bankfee = self.nc_icbc['摘要'].str.contains('网银手续费')
        nc_pay_bankfee = self.nc_icbc[is_pay_bankfee]
        
        for nc_idx in nc_pay_bankfee.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            icbc_pay_bankfee = self.icbc[(cond1)]

            for idx in icbc_pay_bankfee.index:
                if '网银手续费' in icbc_pay_bankfee.loc[idx,'用途']: # 银行摘要也为 '网银手续费'
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     
    
    def pay_progress_amount(self):
        '''
        支付合同结算款/进度款
        eg:<br>
        支付眉山市鸿泰建筑劳务有限公司领地澜山项目施工围挡制作、安装工程施工合同结算款<br>
        支付乐山城市建设工程技术服务有限公司技术服务合同书（测绘类）进度款
        
        rule:
        1. 借贷金额相同
        2. 银行——对方单位：眉山市鸿泰建筑劳务有限公司/乐山城市建设工程技术服务有限公司
        3. 银行——摘要：工程款 【备用】
        '''        
        
        regex_progress_amount = re.compile(r'支付.*结算款$|支付.*进度款$')
        is_progress_amount = self.nc_icbc['摘要'].str.match(regex_progress_amount)
        nc_progress_amount = self.nc_icbc[is_progress_amount]
        
        for nc_idx in nc_progress_amount.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            icbc_progress_amount = self.icbc[(cond1)]

            for idx in icbc_progress_amount.index:
                receiver_cond = icbc_progress_amount.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要'] # 对方单位是 nc摘要中的公司
                if receiver_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def pay_margin(self):
        '''
        存公积金保证金/支付公积金保证金
        eg: 8.7存工行公积金保证金<br>
        rule:<br>
        1. 借贷金额相同
        2. 银行——"保证金户 眉山华瑞宏大置业有限公司"
        
        <br>
        eg: 支付乐山市住房公积金管理中心公积金保证金 <br>
        rule:<br>
        
        1. 借贷金额相同
        2. 银行——对方单位：乐山市住房公积金管理中心
        '''
        
        regex_pay_margin = re.compile(r'.*存.*公积金保证金$|支付.*公积金保证金')
        is_pay_margin = self.nc_icbc['摘要'].str.match(regex_pay_margin)
        nc_pay_margin = self.nc_icbc[is_pay_margin]
        
        for nc_idx in nc_pay_margin.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            icbc_pay_margin = self.icbc[(cond1)]

            for idx in icbc_pay_margin.index:
                if '保证金户' in icbc_pay_margin.loc[idx,'对方户名']: # 对方单位为 保证金户
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                elif icbc_pay_margin.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要']:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def pay_stafftax(self):
        '''
        ### 缴纳个人所得税
        eg1: 申报7月缴纳个人所得税<br>
        
        rule1:<br>
        1. 借贷金额相等
        2. 银行——摘要：代理国库税收收缴
        
        eg2: 2019-08-13代缴个人所得税
        
        rule2:<br>
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——摘要：代理国库税收收缴
        
        > 由于除了时间,其他规则相同，rule1匹配结果会覆盖rule2 
        '''

        is_pay_stafftax = self.nc_icbc['摘要'].str.contains('缴纳个人所得税|代缴个人所得税')
        nc_pay_stafftax = self.nc_icbc[is_pay_stafftax]
        
        for nc_idx in nc_pay_stafftax.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            icbc_pay_stafftax = self.icbc[(cond1)]

            for idx in icbc_pay_stafftax.index:
                if  icbc_pay_stafftax.loc[idx,'用途']=="代理国库税收收缴": # 摘要为 "代理国库税收收缴"
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def pay_surtax(self):
        '''
        预缴教育费附加/印花税/土地增值税
        eg: 预缴教育费附加所属期7月/缴纳印花税 所属期7月/预缴土地增值税 所属期7月
        
        rule:
        1. 借贷金额相同
        2. <del> 交易时间相同</del>
        3. 银行——摘要：代理国库税收收缴
        
        > 缺乏时间约束，在金额相同时，现有规则会和缴纳个税的匹配结果混淆
        '''

        regex_pay_surtax = re.compile(r'.*预?缴教育费附加.*|.*预?缴纳?印花税.*|.*预?缴土地增值税.*')
        is_pay_surtax = self.nc_icbc['摘要'].str.match(regex_pay_surtax)
        nc_pay_surtax = self.nc_icbc[is_pay_surtax]
        
        for nc_idx in nc_pay_surtax.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
        #     cond3 = (self.icbc['交易时间']==self.nc_icbc.loc[nc_idx,'交易时间']) # 交易时间相同
            icbc_pay_surtax = self.icbc[(cond1)]

            for idx in icbc_pay_surtax.index:
                substract_cond = (icbc_pay_surtax.loc[idx,'用途']=='代理国库税收收缴')  
                if substract_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def pay_stksalary(self):
        '''
        付股东方工资
        eg: 付股东方工资<br>
        rule:<br>
        1. 借贷金额相同
        2. nc-摘要：付股东方工资
        3. 银行-摘要：股东方人员工资
        '''

        is_pay_stksalary = self.nc_icbc['摘要'].str.contains('付股东方工资')
        nc_pay_stksalary = self.nc_icbc[is_pay_stksalary]

        for nc_idx in nc_pay_stksalary.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            icbc_pay_stksalary = self.icbc[(cond1)]

            for idx in icbc_pay_stksalary.index:
                if icbc_pay_stksalary.loc[idx,'用途']=="股东方人员工资": # 银行摘要
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def return_investamount(self):
        '''
        归还投资款
        eg: 2019-08-07归还四川信托投资款
        > 公司名不明晰
        
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——对方单位：四川信托有限公司
        '''
        
        regex_return_investamount = re.compile(r'.*归还.*投资款$')
        is_return_investamount = self.nc_icbc['摘要'].str.match(regex_return_investamount)
        nc_return_investamount = self.nc_icbc[is_return_investamount]
        
        for nc_idx in nc_return_investamount.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期']) # 交易时间相同
            icbc_return_investamount = self.icbc[(cond1 & cond2)]

            for idx in icbc_return_investamount.index:
                receiver_cond = (icbc_return_investamount.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要']) #对方单位 
                if receiver_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def return_stkloans(self):
        '''
        归还股东借款
        eg: 8.22归还眉山市宏大建设借款/8.22归还华瑞借款
        > 公司名不明晰
        
        rule:<br>
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——对方单位：眉山市宏大建设投资有限责任公司/眉山华瑞房地产开发有限公司
        4. 银行——摘要：归还股东借款
        '''

        regex_return_stkloans = re.compile(r'.*归还.*借款.*') #可能包含个人归还借款
        is_return_stkloans = self.nc_icbc['摘要'].str.match(regex_return_stkloans)
        nc_return_stkloans = self.nc_icbc[is_return_stkloans]
        
        for nc_idx in nc_return_stkloans.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期']) # 交易时间相同
            icbc_return_stkloans = self.icbc[(cond1 & cond2)]

            for idx in icbc_return_stkloans.index:
                receiver_cond = (icbc_return_stkloans.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要'])
                substract_cond = (icbc_return_stkloans.loc[idx,'用途']=="归还股东借款")
                if receiver_cond and substract_cond: 
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def return_loans(self):
        '''
        归还公司借款
        eg: 8.22归还眉山市宏大建设借款/8.22归还华瑞借款
        
        rule:<br>
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——对方单位：眉山市宏大建设投资有限责任公司/眉山华瑞房地产开发有限公司
        '''

        regex_return_loans = re.compile(r'.*归还.*公司.*借款.*') #可能包含个人归还借款
        is_return_loans = self.nc_icbc['摘要'].str.match(regex_return_loans)
        nc_return_loans = self.nc_icbc[is_return_loans]
        
        for nc_idx in nc_return_loans.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期']) # 交易时间相同
            icbc_return_loans = self.icbc[(cond1 & cond2)]

            for idx in icbc_return_loans.index:
                otherside_cond = (icbc_return_loans.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx    

    def pay_draft(self):
        '''
        商业汇票解付
        eg: 8.7日商业汇票解付<br>
        rule:<br>
        >  nc中为一天的总额数,银行中为一笔或多笔金额
        
        1. 银行——交易时间：2019-08-07 【同一交易日】
        2. 银行——摘要：
        解付商承26920105/
        解付商承/
        商承0010006226920129/
        商承26920136/
        商承到期26920132/
        商承解付/
        商承解付26920133/
        商承到期/
        货款  解付商承001000/
        托收  解付商承001000/
        商承0010006226920113/
        >【规律是：含"解付商承/商承解付/商承到期/商承+一串数字"】
        3. 汇总银行金额借方等于nc贷方
        '''
        regex_draft = re.compile(r'.*商业汇票解付')
        is_draft = self.nc_icbc['摘要'].str.match(regex_draft)
        nc_draft = self.nc_icbc[is_draft]
        
        for nc_idx in nc_draft.index:
            cond1 =(self.icbc['交易日期']==nc_draft.loc[nc_idx,'交易日期'])
            cond2 = (self.icbc['用途'].str.contains(r"解付商承|商承解付|商承到期|商承\d+"))
            icbc_draft = self.icbc[(cond1&cond2)]

            if icbc_draft['支出'].sum() == nc_draft.loc[nc_idx,'贷方']:
                self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                self.icbc.loc[icbc_draft.index,'对账一致'] = 'yes'
                self.nc_icbc.loc[nc_idx,'银行索引'] = ';'.join(map(str,icbc_draft.index.values))
                self.icbc.loc[icbc_draft.index,'NC索引'] = nc_idx  

    def pay_group(self):
        '''
        付集团往来款
        eg: 8.5工行2671付集团往来款 / 付集团往来款8.13<br>
        rule:
        1. 借贷金额相等
        2. 银行——摘要：往来款
        3. 银行——对方单位名称：领地集团股份有限公司
        4. 交易时间相同
        '''

        is_pay_group = self.nc_icbc['摘要'].str.contains('付集团往来款')
        nc_pay_group = self.nc_icbc[is_pay_group]
        
        for nc_idx in nc_pay_group.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期']) #交易时间相同
            icbc_pay_group = self.icbc[(cond1 & cond2)]
            for idx in icbc_pay_group.index:
                purpose_cond = (icbc_pay_group.loc[idx,'用途']=='往来款')
                otherside_cond = (icbc_pay_group.loc[idx,'对方户名']=='领地集团股份有限公司')
                if purpose_cond and otherside_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def pay_firmamount(self):
        '''
        付公司往来款
        eg: 2019-08-08 支付乐山华汇达往来款
        
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——对方单位：乐山华汇达房地产开发有限公司
        '''  
        regex_pay_firmamount = re.compile(r'.*付.*[^集团]往来款')
        is_pay_firmamount = self.nc_icbc['摘要'].str.match(regex_pay_firmamount)
        nc_pay_firmamount = self.nc_icbc[is_pay_firmamount]
        
        for nc_idx in nc_pay_firmamount.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期']) # 交易时间相同
            icbc_pay_firmamount = self.icbc[(cond1 & cond2)]

            for idx in icbc_pay_firmamount.index:
                payer_cond = (icbc_pay_firmamount.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要']) #对方单位 
                if payer_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def inner_transfer(self):
        pass
        '''
        内部转款
        eg: 2019-08-08内部转款
        > 银行摘要不尽相同，最好注明转款的对方单位，<br>
           目前依赖时间和金额不能保证准确，甚至影响其他交易事项的匹配<br>
           放弃，暂时不作匹配
        
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. <del>银行——对方单位：乐山华瑞房地产开发有限公司</del>
        '''
        # regex_inner_transfer = re.compile(r'.*内部转款')
        # is_inner_transfer = nc_icbc['摘要'].str.match(regex_inner_transfer)
        # nc_inner_transfer = nc_icbc[is_inner_transfer]
        # nc_inner_transfer
        
        # for nc_idx in nc_inner_transfer.index:
        #     cond1 = (icbc['借贷标志']=='贷')
        #     cond2 = (icbc['发生额']==nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
        #     cond3 = (icbc['交易时间']==nc_icbc.loc[nc_idx,'交易时间']) # 交易时间相同
        #     icbc_inner_transfer = icbc[(cond1 & cond2 & cond3)]
        # #     print(icbc_inner_transfer) 
        #     for idx in icbc_inner_transfer.index:
        #         payer_cond = (icbc_inner_transfer.loc[idx,'对方单位'] in nc_icbc.loc[nc_idx,'摘要']) #对方单位 
        #         if payer_cond:
        #             nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
        #             icbc.loc[idx,'对账一致'] = 'yes'

    # income and payments
    def bank_transfer(self):
        '''
        跨行转账
        eg: 8.1工行2671到中行6569<br>
        rule:<br>
        1. 借贷金额相等
        2. 银行——摘要：往来款/往来款＋CC00000DWK 【开头】
        3. 银行——对方单位名称：领地集团股份有限公司/领地集团股份有限公司眉山分公司 【开头】
        4. 交易时间相同【必须加以时间约束，否则可能匹配上：付集团往来款8.26。因为其他条件都相同】
        '''
        
        regex_bank_transfer = re.compile(r'.*行\d{4}到.*行\d{4}$')
        is_bank_transfer = self.nc_icbc['摘要'].str.match(regex_bank_transfer)
        nc_bank_transfer = self.nc_icbc[is_bank_transfer]
        
        for nc_idx in nc_bank_transfer.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期']) #交易时间相同
            icbc_bank_transfer = self.icbc[(cond1 & cond2)]

            for idx in icbc_bank_transfer.index:
                purpose_cond = (icbc_bank_transfer.loc[idx,'用途'].startswith('往来款'))
                otherside_cond = (icbc_bank_transfer.loc[idx,'对方户名'].startswith('领地集团股份有限公司'))
                if  purpose_cond and otherside_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     
        
        for nc_idx in nc_bank_transfer.index:
            cond1 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.icbc['交易日期']==self.nc_icbc.loc[nc_idx,'交易日期']) #交易时间相同
            icbc_bank_transfer = self.icbc[(cond1 & cond2)]

            for idx in icbc_bank_transfer.index:
                purpose_cond = (icbc_bank_transfer.loc[idx,'用途'].startswith('往来款'))
                otherside_cond = (icbc_bank_transfer.loc[idx,'对方户名'].startswith('领地集团股份有限公司'))
                if  purpose_cond and otherside_cond:
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def check_lowang(self):
        '''
        处理王镜淇
        eg:<br>
        支付wangjq01-王镜淇借F0403-因公临时借款<br>
        2019.8.6收到王镜淇款项10-1402<br>
        2019-08-06付王镜淇往来款<br>
        2019-08-13收到王镜淇往来款<br>
        
        rule:
        1. 借贷金额相同
        2. 对方单位: 王镜淇
        '''
        is_laowang = self.nc_icbc['摘要'].str.contains('王镜淇')
        nc_laowang = self.nc_icbc[is_laowang]
        
        for nc_idx in nc_laowang.index:
            cond1 = (self.icbc['收入']==self.nc_icbc.loc[nc_idx,'借方']) #借贷金额相同
            icbc_laowang = self.icbc[(cond1)]
            for idx in icbc_laowang.index:
                otherside_cond = (icbc_laowang.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要'])
                if otherside_cond: # 对方单位为 nc摘要中的姓名
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     
        
        for nc_idx in nc_laowang.index:
            cond2 = (self.icbc['支出']==self.nc_icbc.loc[nc_idx,'贷方']) #借贷金额相同
            icbc_laowang = self.icbc[(cond1)]
            for idx in icbc_laowang.index:
                otherside_cond = (icbc_laowang.loc[idx,'对方户名'] in self.nc_icbc.loc[nc_idx,'摘要'])
                if otherside_cond: # 对方单位为 nc摘要中的姓名
                    self.nc_icbc.loc[nc_idx,'对账一致'] = 'yes'
                    self.icbc.loc[idx,'对账一致'] = 'yes'
                    self.nc_icbc.loc[nc_idx,'银行索引'] = idx
                    self.icbc.loc[idx,'NC索引'] = nc_idx                     

    def export_excel(self):
        nc_rows_counts = self.nc_icbc['对账一致'].value_counts(dropna=False)
        icbc_rows_counts = self.icbc['对账一致'].value_counts(dropna=False)

        try:
            nc_yes_rows = nc_rows_counts['yes']
        except KeyError:
            nc_yes_rows = 0
        nc_notmatch_rows = nc_rows_counts.sum()-nc_yes_rows

        try:
            icbc_yes_rows = icbc_rows_counts['yes']
        except KeyError:
            icbc_yes_rows = 0
        icbc_notmatch_rows = icbc_rows_counts.sum()-icbc_yes_rows
        
        print('\n')
        print("+--------------------------------------------------+")
        print("¦                  RESULTS                         ¦")
        print("+--------------------------------------------------+")
        print("¦ EXCEL    ¦       NC_ICBC    ¦        ICBC        ¦")
        print("+--------------------------------------------------+")
        print("¦ TOTAL    ¦{0:^18}¦{1:^20}¦".format(nc_rows_counts.sum(),icbc_rows_counts.sum()))
        print("+--------------------------------------------------+")
        print("¦ MATCH    ¦{0:^18}¦{1:^20}¦".format(nc_yes_rows,icbc_yes_rows))
        print("+--------------------------------------------------+")
        print("¦ NOTMATCH ¦{0:^18}¦{1:^20}¦".format(nc_notmatch_rows,icbc_notmatch_rows))
        print("+--------------------------------------------------+")
        print('\n')

        self.nc_icbc['交易日期'] = self.nc_icbc['交易日期'].astype(str).str.slice(0,10)
        self.icbc['交易日期'] = self.icbc['交易日期'].astype(str).str.slice(0,10)

        
        save_file = self.save_path + '\\' + self.nc_file_name + '+' + self.icbc_file_name + '.xlsx'
        print("结果保存至:\n\t%s\n" %(save_file))
        # self.nc_icbc.to_excel(self.save_path + '/nc_icbc.xlsx')
        # self.icbc.to_excel(self.save_path + '/icbc.xlsx')
        writer = pd.ExcelWriter(save_file,engine='xlsxwriter')
        self.nc_icbc.to_excel(writer,sheet_name=self.nc_file_name,startrow=1,startcol=1,header=False,index=False)
        self.icbc.to_excel(writer,sheet_name=self.icbc_file_name,startrow=1,startcol=1,header=False,index=False)
        
        workbook = writer.book
        nc_sheet = writer.sheets[self.nc_file_name]
        icbc_sheet = writer.sheets[self.icbc_file_name]

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
        
        nc_rows,nc_cols = self.nc_icbc.shape
        for i in range(nc_rows+5):
            nc_sheet.set_row(i,22,cell_format)

        yes_index = self.nc_icbc[self.nc_icbc['对账一致']=='yes'].index+1
        for i in yes_index:
            nc_sheet.set_row(i,22,yes_format)

        # col format
        nc_sheet.set_column(0,nc_cols+5,22)

        nc_sheet.write_row('B1',self.nc_icbc.columns,header_format)
        nc_sheet.write_column('A2',self.nc_icbc.index,header_format)
        nc_sheet.freeze_panes(1,1)
        nc_sheet.set_tab_color('#FF9900')

        #icbc
        # row format
        icbc_rows,icbc_cols = self.icbc.shape
        for i in range(icbc_rows+5):
            icbc_sheet.set_row(i,22,cell_format)

        yes_index = self.icbc[self.icbc['对账一致']=='yes'].index+1
        for i in yes_index:
            icbc_sheet.set_row(i,22,yes_format)

        # col format
        icbc_sheet.set_column(0,icbc_cols+5,22)

        icbc_sheet.write_row('B1',self.icbc.columns,header_format)
        icbc_sheet.write_column('A2',self.icbc.index,header_format)
        icbc_sheet.freeze_panes(1,1)
        icbc_sheet.set_tab_color('#FF9900')

        writer.save()

    def doall(self):
        self.rec_mortgage()
        self.rec_pfund()
        self.rec_buildingamount()
        self.rec_pos()
        self.rec_loans()
        self.rec_deposit()
        self.rec_refund()
        self.rec_prefbond()
        self.rec_group()
        self.rec_firmamount()
        self.save_rfund()
        self.pay_refund()
        self.pay_loans()
        self.pay_reimburse()
        self.prepay_firmamount()
        self.pay_fee()
        self.pay_bankfee()
        self.pay_progress_amount()
        self.pay_margin()
        self.pay_stafftax()
        self.pay_surtax()
        self.pay_stksalary()
        self.return_loans()
        self.return_investamount()
        self.return_stkloans()
        self.pay_draft()
        self.pay_group()
        self.pay_firmamount()
        self.inner_transfer()
        self.bank_transfer()
        self.check_lowang()
        self.export_excel()

    def __call__(self):
        return self.doall()


# if __name__=='__main__':
#     nc_path = input("请输入NC表路径: ")
#     bank_path = input("请输入银行表路径: ")
#     deal_excel = DealExcelICBC(nc_path=nc_path,bank_path=bank_path,bank_name=None)
#     nc_icbc = deal_excel.dealNC()
#     icbc = deal_excel.dealBANK()

#     check_icbc = CheckICBC(nc_icbc, icbc)
#     check_icbc.doall()