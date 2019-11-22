#!/usr/bin/env python
# coding: utf-8
# 中行对账
import pandas as pd
import numpy as np
import re

# 整理表格
class DealExcelBOC(object):
    def __init__(self,nc_path,bank_path):
        self.nc_path = nc_path
        self.bank_path = bank_path

    def dealNC(self):
        # read
        nc_boc = pd.read_excel(self.nc_path,header=None)
        nc_boc = nc_boc.dropna(how='all')

        # deal year/head/tail
        year = nc_boc.iloc[0,0]
        init_period = nc_boc.iloc[2,:] # 暂时保存期初行
        month_year_sum = nc_boc.tail(2) # 暂时保存本月及本年累计行

        # drop useless rows
        nc_boc.columns = nc_boc.iloc[1,:] 
        nc_boc = nc_boc.drop([0,1,2]) 
        nc_boc = nc_boc.head(len(nc_boc)-2)

        time = str(year) + '-' + nc_boc['月'].astype(str) + '-' + nc_boc['日'].astype(str)
        nc_boc.insert(0,'日期',pd.to_datetime(time,format='%Y-%m-%d').astype(str).str.slice(0,10))

        nc_boc.reset_index(drop=True,inplace=True)

        # 提取交易时间
        time_pattern1 = re.compile(r'\d{4}-\d+-\d+')
        time_pattern2 = re.compile(r'\d{4}\.\d+\.\d+')
        time_pattern3 = re.compile(r'\d+\.\d+')

        transac_time = nc_boc['摘要'].copy()
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

        nc_boc.insert(6,'交易日期',transac_time)
        nc_boc['交易日期']=pd.to_datetime(transac_time,format='%Y-%m-%d')

        # 生成对账标记
        nc_boc.insert(0,"银行索引",'')
        nc_boc.insert(0,'对账一致',None)

        # 转换字段类型
        nc_boc.columns = list(map(lambda x: str(x).strip(),nc_boc.columns))
        nc_boc.loc[:,['银行账户名称','摘要']] = nc_boc[['银行账户名称','摘要']].apply(lambda s: s.str.strip().str.replace('[ （）()]',''))
        nc_boc.loc[:,['借方','贷方','余额']] = nc_boc[['借方','贷方','余额']].apply(lambda s: s.astype(np.float64))

        nc_boc.drop(['月','日'],axis=1,inplace=True)

        return nc_boc

    def dealBANK(self):
        # read
        boc = pd.read_excel(self.bank_path,header=None)
        boc = boc.dropna(how='all')

        if boc.iloc[0,0]=='组织':
            boc.columns = boc.loc[0,:]
            boc = boc.drop(0)

            need_fields = ["组织","银行","账号","币种","交易日期","收入","支出","当前余额", 
                            "用途","对方户名","付款人开户行名","收款人开户行名","交易附言",
                            "用途_原","交易附言", "来源","业务类型","资金系统单据号",]
            for col in need_fields:
                if col not in boc.columns:
                    boc[col] = None

            boc['交易日期'] = pd.to_datetime(boc['交易日期'])

            strip_fields = ["组织","账号","币种","用途","对方户名","备注","业务类型"]
            boc.loc[:,strip_fields] = boc[strip_fields].apply(lambda s: s.str.strip().str.replace('[ （）()]',''))          

        else:
            # drop useless rows
            for row in boc.index:
                for col in boc.columns:
                    if str(boc.loc[row,col]).strip()=='交易日期[ Transaction Date ]':
                        header_row = row
            #             print(header_row)
                        break
            boc.columns = boc.loc[header_row,:]
            boc = boc.loc[header_row+1:,:]
            
            
            # transform columns
            boc.columns = list(map(lambda x: str(x).strip(),boc.columns))

            if "本方账号" not in boc.columns:
                boc['本方账号'] = None
            if "余额" not in boc.columns:
                boc['余额'] = None

            rename_dict = {
                "交易日期[ Transaction Date ]": "交易日期",
                "交易后余额[ After-transaction balance ]":"当前余额",
                "摘要[ Reference ]":"用途",
                "交易类型[ Transaction Type ]":"业务类型",
                "交易货币[ Trade Currency ]":"币种",
                "付款人开户行名[ Payer account bank ]":"付款人开户行名",
                "收款人开户行名[ Beneficiary account bank ]":"收款人开户行名",
                "交易附言[ Remark ]":"交易附言",
                "用途[ Purpose ]":"用途_原",
                "备注[ Remarks ]":"备注",
            }

            boc.rename(columns=rename_dict,inplace=True)
            boc['交易日期'] = pd.to_datetime(boc['交易日期'].str.slice(0,8),format='%Y-%m-%d')

            income = np.where(boc["交易金额[ Trade Amount ]"]>=0,boc["交易金额[ Trade Amount ]"],0)
            payment = np.where(boc["交易金额[ Trade Amount ]"]<=0,boc["交易金额[ Trade Amount ]"].abs(),0)
            our_account = np.where(boc["交易金额[ Trade Amount ]"]<=0,boc["付款人账号[ Debit Account No. ]"],boc["收款人账号[ Payee's Account Number ]"])
            your_account = np.where(boc["交易金额[ Trade Amount ]"]>0,boc["付款人账号[ Debit Account No. ]"],boc["收款人账号[ Payee's Account Number ]"])
            otherside = np.where(boc["交易金额[ Trade Amount ]"]<=0,boc["收款人名称[ Payee's Name ]"],boc["付款人名称[ Payer's Name ]"])
            
            boc['收入'] = income
            boc['支出'] = payment
            boc['账号'] = our_account
            boc['对方账号'] = your_account
            boc['对方户名'] = otherside
            # boc['备注'] = boc[['交易附言[ Remark ]','用途[ Purpose ]']].fillna('').sum(1)
            boc["银行"] = 'BOC-中国银行'
            boc["来源"] = 'U-BOC'
            boc['币种'] = 'CNY-人民币'
            boc['资金系统单据号'] = None
            boc['组织'] = None

            # drop useless columns
            need_fields = ["组织","银行","账号","对方账号","币种","交易日期","收入","支出","当前余额", 
                            "用途","对方户名","付款人开户行名","收款人开户行名","交易附言",
                            "用途_原","交易附言", "来源","业务类型","资金系统单据号",]
            boc = boc[need_fields]
    
            strip_fields = ["组织","账号","对方账号","币种","用途","对方户名","交易附言","业务类型","交易附言","用途_原"]
            boc.loc[:,strip_fields] = boc[strip_fields].apply(lambda s: s.str.strip().str.replace('[ （）()]',''))


        # 对账标记
        boc.insert(0,"NC索引",None)
        boc.insert(0,'对账一致',None)
        boc.reset_index(inplace=True)
        boc.sort_values(['index'])
        boc.drop(['index'],axis=1,inplace=True)     
        
        num_fields = ['收入','支出','当前余额']
        
        for col in num_fields:
            try:
                boc.loc[:,col] = boc[col].replace({'-':None}).astype(np.float64)
            except ValueError:
                boc.loc[:,col] = boc[col].replace({'-':None}).str.replace(',','').astype(np.float64)

        return boc

# 对账规则

class CheckBOC(object):
    def __init__(self,nc_boc,boc,nc_file_name,boc_file_name,save_path=None):
        self.nc_boc = nc_boc
        self.boc = boc
        self.nc_file_name = nc_file_name
        self.boc_file_name = boc_file_name
        self.save_path = save_path

    # income items
    def rec_mortgage(self):
        '''
        收取银行按揭
        eg：2019-08-02收郭代晓;徐学君[眉山]蘭台府-蘭台府一期-10-2301银行按揭
        
        rule:
        1. NC<->银行：借贷金额相同
        2. 交易时间相同
        3. 银行——付款人名称[ Payer's Name ]: 郭代晓
        '''   
        regex_mortgage = re.compile(r'.*收.*银行按揭$')
        is_mortgage = self.nc_boc['摘要'].str.match(regex_mortgage)
        nc_mortgage = self.nc_boc[is_mortgage]

        for nc_idx in nc_mortgage.index:
            cond1 = (self.boc['收入']==self.nc_boc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.boc['交易日期']== self.nc_boc.loc[nc_idx,'交易日期']) #交易时间相同
            boc_mortgage = self.boc[(cond1 & cond2)]

            for idx in boc_mortgage.index:
                if boc_mortgage.loc[idx,"对方户名"] in self.nc_boc.loc[nc_idx,'摘要']: # 对方单位为 nc摘要中的姓名
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx                    
    
    def pos_to_bank(self):
        '''
        POS转银行存款
        eg: 8.1中行POS6569转银行存款
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——付款人名称[ Payer's Name ]：银联商务股份有限公司客户备付金
        4. 银行——交易附言[ Remark ]：0731-0731费0元
        > 3 4 择其一，看哪个更适用，暂用3
        '''
        regex_pos_tobank = re.compile(r'.*中行POS\d+转银行存款')
        is_pos_tobank = self.nc_boc['摘要'].str.match(regex_pos_tobank)
        nc_pos_tobank = self.nc_boc[is_pos_tobank]
        
        for nc_idx in nc_pos_tobank.index:
            cond1 = (self.boc['收入']==self.nc_boc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.boc['交易日期']==self.nc_boc.loc[nc_idx,'交易日期']) #交易时间相同
            boc_pos_tobank = self.boc[(cond1 & cond2)]

            for idx in boc_pos_tobank.index:
                if boc_pos_tobank.loc[idx,"对方户名"]== "银联商务股份有限公司客户备付金":
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx                    
        
    def rec_pos(self):
        '''
        POS到账
        eg: 0808-0808POS到账<br>
        rule:
        1. 借贷金额相同
        2. 银行——付款人名称[ Payer's Name ]：银联商务股份有限公司客户备付金
        3. 银行——交易附言[ Remark ]：0808-0808费0元
        '''
        regex_pos = re.compile(r'\d+-\d+POS到账.*|\d+-\d+pos到账.*')
        is_pos = self.nc_boc['摘要'].str.match(regex_pos)
        nc_pos = self.nc_boc[is_pos]
        
        for nc_idx in nc_pos.index:
            cond1 = (self.boc['收入']==self.nc_boc.loc[nc_idx,'借方']) #借贷金额相同
            boc_pos = self.boc[(cond1)]
            for idx in boc_pos.index:
                note_cond = re.findall(r'\d+-\d+',str(boc_pos.loc[idx,'交易附言']))
                substract_cond = re.findall(r'\d+-\d+',self.nc_boc.loc[nc_idx,'摘要'])
                if  note_cond==substract_cond:
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx                    
    
    def rec_loans(self):
        '''
        收到归还借款
        eg: 收到yangxj-杨欣洁归还F0403-因公临时借款<br>
        rule:
        1. 借贷金额相同
        2. 银行——付款人名称[ Payer's Name ]：杨欣洁
        '''
        regex_rec_loans = re.compile(r'.*收到.*归还.*借款')
        is_rec_loans = self.nc_boc['摘要'].str.match(regex_rec_loans)
        nc_rec_loans = self.nc_boc[is_rec_loans]
        
        for nc_idx in nc_rec_loans.index:
            cond1 = (self.boc['收入']==self.nc_boc.loc[nc_idx,'借方']) #借贷金额相同
            boc_rec_loans = self.boc[(cond1)]
            
            for idx in boc_rec_loans.index:
                if boc_rec_loans.loc[idx,"对方户名"] in self.nc_boc.loc[nc_idx,'摘要']:
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx                    


    def rec_appointment_building(self):
        '''
        收楼款/收定金/收预约金
        eg:
            2019-09-02收郭胜财[乐山]青江蘭台-一期-产权车位-车位1层196定金
            2019-09-04收商永志;刘雨妃[乐山]青江蘭台-一期-2号楼-2002楼款
            2019-09-04收唐松柏;翟鹏群[乐山]青江蘭台-一期-7号楼-2903预约金
        
        rule1:
            1. 借贷金额相同
            2. 交易时间相同
            3. 银行——对方单位:郭胜财/商永志/唐松柏

        rule2:
            > nc为多笔金额，银行为汇总数
            
            1. 交易时间相同【X 差一天】
            2. 银行——对方户名：银联商务股份有限公司客户备付金
            3. 汇总nc金额
            4. 银行金额=nc汇总金额
            5. 银行——用途：0905-0905费0元【1.改用5.作为rule3】
        '''   
        
        # rule1
        regex_appointment_building = re.compile(r'.*收.*定金.*|.*收.*楼款.*|.*收.*预约金.*|.*收.*垫付款.*')
        is_appointment_building = self.nc_boc['摘要'].str.match(regex_appointment_building)
        nc_appointment_building = self.nc_boc[is_appointment_building]

        for nc_idx in nc_appointment_building.index:
            cond1 = (self.boc['收入']==self.nc_boc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.boc['交易日期']== self.nc_boc.loc[nc_idx,'交易日期']) #交易时间相同
            boc_appointment_building = self.boc[(cond1 & cond2)]

            for idx in boc_appointment_building.index:
                if boc_appointment_building.loc[idx,"对方户名"] in self.nc_boc.loc[nc_idx,'摘要']: # 对方单位为 nc摘要中的姓名
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx

        # rule2
        nc_sum_appointment_building = nc_appointment_building.groupby(['交易日期'])['借方'].sum().reset_index().rename(columns={"借方":"借方和"})
        for sum_idx in nc_sum_appointment_building.index:
            time_cond = (self.boc['交易日期']==nc_sum_appointment_building.loc[sum_idx,'交易日期'])
            otherside_cond = (str(self.boc['对方户名']).strip()=="银联商务股份有限公司客户备付金")
            boc_appointment_building = self.boc[(time_cond&otherside_cond)]
            
            for idx in boc_appointment_building.index:
                if boc_appointment_building.loc[idx,'收入'] == nc_sum_appointment_building.loc[sum_idx,'借方和']:
                    idxs_cond = (nc_appointment_building['交易日期']==nc_sum_appointment_building.loc[sum_idx,'交易日期'])
                    nc_idxs = nc_appointment_building[idxs_cond].index
                    
                    self.nc_boc.loc[nc_idxs,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idxs,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = ";".join(map(str,nc_idxs.values))

        # rule3
        nc_sum_appointment_building = nc_appointment_building.groupby(['交易日期'])['借方'].sum().reset_index().rename(columns={"借方":"借方和"})

        for sum_idx in nc_sum_appointment_building.index:
            purpose_cond = (self.boc['用途'].str.match(r'\d{4}-\d{4}费'))
            otherside_cond = (self.boc['对方户名'].str.strip()=="银联商务股份有限公司客户备付金")
            boc_appointment_building = self.boc[(purpose_cond&otherside_cond)]

            for idx in boc_appointment_building.index:
                if boc_appointment_building.loc[idx,'收入'] == nc_sum_appointment_building.loc[sum_idx,'借方和']:
                    idxs_cond = (nc_appointment_building['交易日期']==nc_sum_appointment_building.loc[sum_idx,'交易日期'])
                    nc_idxs = nc_appointment_building[idxs_cond].index
                    
                    self.nc_boc.loc[nc_idxs,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idxs,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = ";".join(map(str,nc_idxs.values))        

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

        资金表：
        eg:
        2019-09-05收高雨蝶[眉山]凯旋国际公馆-凯旋府二期-30号楼-1-1002公积金
    
        rule:
            1.借贷金额相同
            2.银行——用途：高雨蝶个人住房公积金 
            3.银行——对方用户：为空
            '''
        # rule1
        regex_pfund = re.compile(r'.*收.*公积金$')
        is_pfund = self.nc_boc['摘要'].str.match(regex_pfund)
        nc_pfund = self.nc_boc[is_pfund]
        
        for nc_idx in nc_pfund.index:
            cond1 = (self.boc['收入']==self.nc_boc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.boc['交易日期']== self.nc_boc.loc[nc_idx,'交易日期']) #交易时间相同
            boc_pfund = self.boc[(cond1 & cond2)]

            for idx in boc_pfund.index:
                if str(boc_pfund.loc[idx,'对方户名']) in self.nc_boc.loc[nc_idx,'摘要']: # 对方单位为 nc摘要中的姓名
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx 
                    
                elif str(boc_pfund.loc[idx,'对方户名'])=="个人住房公积金委托贷款资金-个人住房公积金委托贷款资金":
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx

                else: # 对方户名为空
                    person_name = re.findall('(.*)个人住房公积金',boc_pfund.loc[idx,'用途'])[0] #['高雨蝶']
                    if person_name in self.nc_boc.loc[nc_idx,'摘要']:
                        self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                        self.boc.loc[idx,'对账一致'] = 'yes'
                        self.nc_boc.loc[nc_idx,'银行索引'] = idx
                        self.boc.loc[idx,'NC索引'] = nc_idx

        # rule2
        total_pfund = nc_pfund['借方'].sum()
        
        cond1 = (self.boc['收入']==total_pfund) #借贷金额相同
        try:
            cond2 = (self.boc['交易日期']== nc_pfund['交易日期'][0]) #交易时间相同
            boc_pfund = self.boc[(cond1&cond2)]
        except (IndexError,KeyError): #nc_pfund 为 empty df
            boc_pfund = self.boc[cond1]
            
        for idx in boc_pfund.index:
            if boc_pfund.loc[idx,'对方户名']=="个人住房公积金委托贷款资金-个人住房公积金委托贷款资金":
                self.nc_boc.loc[nc_pfund.index,'对账一致'] = 'yes'
                self.boc.loc[idx,'对账一致'] = 'yes'
                self.nc_boc.loc[nc_idx,'银行索引'] = idx
                self.boc.loc[idx,'NC索引'] = ';'.join(map(str,nc_pfund.index.values))


    def rec_fee(self):
        '''
        收手续费/代收费用
        eg:
            2019-09-07收赵亮;左雪莲[眉山]凯旋国际公馆-一期-4号楼商业-106附1代收费用
            2019-09-07收赵亮;左雪莲[眉山]凯旋国际公馆-一期-4号楼商业-106附1手续费
        
        rule:
            1. 借贷金额相同
            2. 交易时间相同
            3. 银行——对方户名: 姓名
        '''   
        regex_fee = re.compile(r'.*收.*代收费用|.*收.*手续费')
        is_fee = self.nc_boc['摘要'].str.match(regex_fee)
        nc_fee = self.nc_boc[is_fee]

        for nc_idx in nc_fee.index:
            cond1 = (self.boc['收入']==self.nc_boc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.boc['交易日期']== self.nc_boc.loc[nc_idx,'交易日期']) #交易时间相同
            boc_fee = self.boc[(cond1 & cond2)]

            for idx in boc_fee.index:
                if str(boc_fee.loc[idx,"对方户名"]) in self.nc_boc.loc[nc_idx,'摘要']: # 对方单位为 nc摘要中的姓名
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx 


    def rec_firmamount(self):
        '''
        eg:
            2019-09-07收领地集团股份有限公司往来款
        
        rule:
            1. 借贷金额相同
            2. 交易时间相同
            3. 银行——对方单位：领地集团股份有限公司
        '''
        regex_rec_firmamount = re.compile(r'.*收.*往来款.*')
        is_rec_firmamount = (self.nc_boc['摘要'].str.match(regex_rec_firmamount))
        nc_rec_firmamount = self.nc_boc[is_rec_firmamount]
        
        for nc_idx in nc_rec_firmamount.index:
            cond1 = (self.boc['收入']==self.nc_boc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.boc['交易日期'] == self.nc_boc.loc[nc_idx,'交易日期'])
            boc_rec_firmamount = self.boc[(cond1&cond2)]

            for idx in boc_rec_firmamount.index:
                otherside_cond = (str(boc_rec_firmamount.loc[idx,"对方户名"]) in self.nc_boc.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx 

    # payments
    def prepay_amount(self):
        '''
        支付预付款
        eg:支付奥的斯电梯（中国）有限公司眉山领地．蘭台府商住小区（一期）高层电梯设备采购合同预付款<br>
        rule:<br>
        1. 借贷金额相同
        2. 银行——收款人名称[ Payee's Name ]：奥的斯电梯（中国）有限公司
        '''
        regex_prepayments = re.compile(r'支付.*预付款$')
        is_prepayments = self.nc_boc['摘要'].str.match(regex_prepayments)
        nc_prepayments = self.nc_boc[is_prepayments]
        
        for nc_idx in nc_prepayments.index:
            cond1 = (self.boc['支出']==self.nc_boc.loc[nc_idx,'贷方']) #借贷金额相同
            boc_prepayments = self.boc[(cond1)]

            for idx in boc_prepayments.index:
                if boc_prepayments.loc[idx,"对方户名"] in self.nc_boc.loc[nc_idx,'摘要']: # 对方单位为 nc摘要中的名称
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx                    
        
    def pay_bankfee(self):
        '''
        支付中行手续费
        eg: 8.22中行7014手续费 <br>
        rule1:
        > 逐笔比对
        
        1. 借贷金额相同
        2. 交易时间相同
        2. 银行——付款人开户行名[ Payer account bank ]：中国银行眉山新区支行 【中国银行】<br>
            银行——收款人开户行名[ Beneficiary account bank ]：为空
        
        rule2:
        > 汇总比对，nc/银行各自可能有汇总/分散金额情况
        
        1. nc——摘要：中行手续费
        2. 银行——付款人开户行名[ Payer account bank ]：中国银行眉山新区支行 【中国银行】<br>
           银行——收款人开户行名[ Beneficiary account bank ]：为空
        3. 汇总nc手续费金额=汇总银行金额
        
        弃用rule：
        > 银行——摘要[ Reference ]：转账汇款手续费 【有些摘要不适用】

        eg: 【资金系统】
            1297手续费
        
        rule1:
            > 逐笔比对
        rule2:
            > nc为单笔金额，银行为多笔
            
            1. 银行——用途：询证函、验资证明、开户证明、结算资信证明、工商验资E线通
            2. 银行——对方户名：空
            2. 汇总银行金额
            3. nc金额=银行汇总
        
        支付银行手续费
        eg: 8.7中行6569手续费
            9.5 银行手续费
        rule:
        > 逐笔比对
        > nc是一个总额，银行为多笔金额

        1. 交易时间相同
        2. 银行-摘要：收费/SMSP Service Charge/对公跨行转账汇款手续费
        3. 汇总银行金额等于NC贷方金额
        '''

        regex_pay_bankfee = re.compile(r'.*[中银]行.*手续费$')
        is_pay_bankfee = self.nc_boc['摘要'].str.match(regex_pay_bankfee)
        nc_pay_bankfee = self.nc_boc[is_pay_bankfee]
        
        # rule1: sum
        nc_total_bankfee = nc_pay_bankfee['贷方'].sum()
        payer_cond = self.boc["付款人开户行名"].str.contains('中国银行')
        benef_cond = self.boc["收款人开户行名"].isnull()
        boc_pay_bankfee = self.boc[(payer_cond & benef_cond)]
        boc_total_bankfee = boc_pay_bankfee['支出'].sum()
        
        if nc_total_bankfee==boc_total_bankfee:
            self.nc_boc.loc[nc_pay_bankfee.index,'对账一致'] = 'yes'
            self.boc.loc[boc_pay_bankfee.index,'对账一致'] = 'yes'
            self.nc_boc.loc[nc_pay_bankfee.index,'银行索引'] = ';'.join(map(str,boc_pay_bankfee.index.values))
            self.boc.loc[boc_pay_bankfee.index,'NC索引'] = ';'.join(map(str,nc_pay_bankfee.index.values))

        # rule1_:sum
        for nc_idx in nc_pay_bankfee.index:
            cond1 = (self.boc['交易日期'] ==self.nc_boc.loc[nc_idx, '交易日期'])  # 交易时间相同
            cond2 = (self.boc['用途'].str.contains('收费|ServiceCharge|手续费'))
            boc_pay_bankfee = self.boc[(cond1 & cond2)]

            if boc_pay_bankfee['支出'].sum() == self.nc_boc.loc[nc_idx, '贷方']:
                self.nc_boc.loc[nc_idx, '对账一致'] = 'yes'
                self.boc.loc[boc_pay_bankfee.index, '对账一致'] = 'yes'
                self.nc_boc.loc[nc_idx, '银行索引'] = ';'.join(map(str, boc_pay_bankfee.index.values))
                self.boc.loc[boc_pay_bankfee.index, 'NC索引'] = nc_idx

        # rule2:
        for nc_idx in nc_pay_bankfee.index:
            cond1 = (self.boc['支出'] == self.nc_boc.loc[nc_idx, '贷方'])  # 借贷金额相同
            cond2 = (self.boc['交易日期'] ==self.nc_boc.loc[nc_idx, '交易日期'])  # 交易时间相同
            boc_pay_bankfee = self.boc[(cond1 & cond2)]

            for idx in boc_pay_bankfee.index:
                payer_cond = ('中国银行' in boc_pay_bankfee.loc[idx, "付款人开户行名"])
                benef_cond = (boc_pay_bankfee.loc[idx, "收款人开户行名"] is np.nan)
                purpose_cond1 = ("收费" in boc_pay_bankfee.loc[idx, '用途'])
                purpose_cond2 = ("ServiceCharge" in boc_pay_bankfee.loc[idx, '用途'])
                purpose_cond3 = ("手续费" in boc_pay_bankfee.loc[idx, '用途'])
                
                cond1 = (payer_cond&benef_cond&purpose_cond1)
                cond2 = (payer_cond&benef_cond&purpose_cond2)
                cond3 = (payer_cond&benef_cond&purpose_cond3)

                if cond1 or cond2 or cond3:
                    self.nc_boc.loc[nc_idx, '对账一致'] = 'yes'
                    self.boc.loc[idx, '对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx, '银行索引'] = idx
                    self.boc.loc[idx, 'NC索引'] = nc_idx


        # 资金系统rule1:
        regex_pay_bankfee = re.compile(r'.*\d+手续费$')
        is_pay_bankfee = self.nc_boc['摘要'].str.match(regex_pay_bankfee)
        nc_pay_bankfee = self.nc_boc[is_pay_bankfee]

        for nc_idx in nc_pay_bankfee.index:
            cond1 = (self.boc['用途'].str.startswith("询证函|验资证明|开户证明|结算资信证明|工商验资E线通|收费项目"))
            cond2 = (self.boc["对方户名"].isnull())
            boc_pay_bankfee = self.boc[(cond1&cond2)]

            boc_sum_pay_bankfee = boc_pay_bankfee.groupby(['交易日期'])['支出'].sum().reset_index().rename(columns={'支出':'支出和'})

            for sum_idx in boc_sum_pay_bankfee.index:
                if boc_sum_pay_bankfee.loc[sum_idx,'支出和']==nc_pay_bankfee.loc[nc_idx,'贷方']:
                    boc_idxs_cond = (boc_pay_bankfee['交易日期']==boc_sum_pay_bankfee.loc[sum_idx,'交易日期'])
                    boc_idxs = boc_pay_bankfee[boc_idxs_cond].index

                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[boc_idxs,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = ';'.join(map(str,boc_idxs.values))
                    self.boc.loc[boc_idxs,'NC索引'] = nc_idx 

        # 资金系统rule2:
        for nc_idx in nc_pay_bankfee.index:
            cond1 = (self.boc['支出'] == self.nc_boc.loc[nc_idx, '贷方'])  # 借贷金额相同
            cond2 = (self.boc["对方户名"].isnull())
            boc_pay_bankfee = self.boc[(cond1 & cond2)]

            for idx in boc_pay_bankfee.index:
                purpose_cond = (
                    boc_pay_bankfee.loc[idx, '用途'].startswith("询证函|验资证明|开户证明|结算资信证明|工商验资E线通|收费项目"))
                if purpose_cond:
                    self.nc_boc.loc[nc_idx, '对账一致'] = 'yes'
                    self.boc.loc[idx, '对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx, '银行索引'] = idx
                    self.boc.loc[idx, 'NC索引'] = nc_idx

    def pay_progressamount(self):
        '''
        支付合同进度款
        eg:支付华优建筑设计院有限责任公司成都分公司眉山领地 蘭台府项目人防设计合同进度款<br>
        rule1:<br>
        > 逐笔比对
        
        1. 借贷金额相同
        2. 银行——收款人名称[ Payee's Name ]：华优建筑设计院有限责任公司成都分公司
        
        <br>
        eg: 支付乐山市银河建筑工程有限公司领地凯旋府土石方工程施工合同进度款<br>
        rule2:
        
        > 双边汇总，nc可能为多笔金额，银行也为多笔金额，且只有总数等同
        
        1. 汇总nc贷方金额
        2. 银行——收款人名称[ Payee's Name ]:乐山市银河建筑工程有限公司
        3. 汇总银行金额
        4. nc总额=银行总额
        '''
        
        # rule1：
        regex_progress_payment = re.compile(r'支付.*进度款$')
        is_progress_payment = self.nc_boc['摘要'].str.match(regex_progress_payment)
        nc_progress_payment = self.nc_boc[is_progress_payment]
        
        for nc_idx in nc_progress_payment.index:
            cond1 = (self.boc['支出']==self.nc_boc.loc[nc_idx,'贷方']) #借贷金额相同
            boc_progress_payment = self.boc[(cond1)]

            for idx in boc_progress_payment.index:
                otherside_cond = (boc_progress_payment.loc[idx,"对方户名"] in self.nc_boc.loc[nc_idx,'摘要'])
                if otherside_cond: # 对方单位为 nc摘要中的名称
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    # self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    # self.boc.loc[idx,'NC索引'] = nc_idx
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx
        
        # rule2: 
        nc_sum_progress = nc_progress_payment.groupby('摘要').agg({'贷方':'sum'}).reset_index() #注意摘要不同，分组求和
        nc_sum_progress.rename(columns={'贷方':'贷方和'},inplace=True)

        for sum_idx in nc_sum_progress.index:
            boc_idxs = []
            for idx in self.boc.index:
                if str(self.boc.loc[idx,"对方户名"]) in nc_sum_progress.loc[sum_idx,'摘要']:
                    boc_idxs.append(idx)

        #     print(boc.loc[boc_idxs,'交易金额[ Trade Amount ]'].sum())
        #     print(nc_sum_progress.loc[nc_idx,'贷方和'])
        #     5020382.89
        #     5020382.890000001
            boc_sum_progress = self.boc.loc[boc_idxs]['支出'].sum()
            if np.around(boc_sum_progress,2)==np.around(nc_sum_progress.loc[sum_idx,'贷方和'],2):
                idx_cond1 = (nc_progress_payment['摘要']==nc_sum_progress.loc[sum_idx,'摘要'])
                nc_idxs = nc_progress_payment[(idx_cond1)].index
                
                self.nc_boc.loc[nc_idxs,'对账一致'] = 'yes'
                self.boc.loc[boc_idxs,'对账一致'] = 'yes'
                self.nc_boc.loc[nc_idxs,'银行索引'] = ';'.join(map(str,boc_idxs))
                self.boc.loc[boc_idxs,'NC索引'] = ';'.join(map(str,nc_idxs.values))         

        
    def capital_pool(self):
        '''
        资金池归集——现有规则在金额相同时可能和付集团往来款匹配相交叉
        eg： 资金池归集 <br>
        rule:
        1. 借贷金额相同 
        2. 银行——收款人名称[ Payee's Name ]：领地集团股份有限公司
        2. 银行——用途[ Purpose ]：资金池归集＋CC00000DKO
        > 没有更好的规则，依赖金额的差异性；与付集团往来款基本相同,但集团往来款有时间字段进行约束。
        '''
        is_capital_pool = (self.nc_boc['摘要'].str.strip()=='资金池归集')
        nc_capital_pool = self.nc_boc[is_capital_pool]
        
        for nc_idx in nc_capital_pool.index:
            cond1 = (self.boc['支出']==self.nc_boc.loc[nc_idx,'贷方']) #借贷金额相同
            boc_capital_pool = self.boc[(cond1)]
            for idx in boc_capital_pool.index:
                purpose_cond = ('资金池归集' in  boc_capital_pool.loc[idx,"用途_原"])
                receiver_cond = (boc_capital_pool.loc[idx,"对方户名"].startswith('领地集团股份有限公司'))
                if purpose_cond and receiver_cond:
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx                       
    
    def pay_group(self):
        '''
        付集团往来款
        eg: 2019-08-12付集团往来款<br>
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——收款人名称[ Payee's Name ]：领地集团股份有限公司 【含】
        '''
        regex_pay_group = re.compile(r'.*付集团往来款')
        is_pay_group = self.nc_boc['摘要'].str.match(regex_pay_group)
        nc_pay_group = self.nc_boc[is_pay_group]
        
        for nc_idx in nc_pay_group.index:
            cond1 = (self.boc['支出']==self.nc_boc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.boc['交易日期']==self.nc_boc.loc[nc_idx,'交易日期']) #交易时间相同
            boc_pay_group = self.boc[(cond1 & cond2)]

            for idx in boc_pay_group.index:
                if boc_pay_group.loc[idx,"对方户名"].startswith('领地集团股份有限公司'):
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes' 
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx                           


    def pay_firmamount(self):
        '''
        eg:
            2019-09-07支付领地集团股份有限公司往来款
        
        rule:
            1. 借贷金额相同
            2. 交易时间相同
            3. 银行——对方单位：领地集团股份有限公司
        '''
        regex_pay_firmamount = re.compile(r'.*付.*往来款.*')
        is_pay_firmamount = (self.nc_boc['摘要'].str.match(regex_pay_firmamount))
        nc_pay_firmamount = self.nc_boc[is_pay_firmamount]

        for nc_idx in nc_pay_firmamount.index:
            cond1 = (self.boc['支出']==self.nc_boc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.boc['交易日期'] == self.nc_boc.loc[nc_idx,'交易日期'])
            boc_pay_firmamount = self.boc[(cond1&cond2)]

            for idx in boc_pay_firmamount.index:
                otherside_cond = (str(boc_pay_firmamount.loc[idx,"对方户名"]) in self.nc_boc.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx 

        
    def bank_transfer(self):
        '''
        跨行转账
        eg: 8.26中行7014到工行1862<br>
            8.8中行6569到农行0752监管资金<br>
        rule:<br>
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——摘要:OBSS022843398687GIRO000000000000【没法用】
        4. 银行——付款人开户行名[ Payer account bank ]：中国银行眉山新区支行 【中国银行】<br>
            银行——收款人开户行名[ Beneficiary account bank ]：中国工商银行眉山市分行业务处理中心 【工商银行】
        '''          
        
        regex_bank_transfer = re.compile(r'.*行\d{4}到.*行\d{4}$|.*行\d{4}到.*行\d{4}监管资金$')
        is_bank_transfer = self.nc_boc['摘要'].str.match(regex_bank_transfer)
        nc_bank_transfer = self.nc_boc[is_bank_transfer]
        
        bank_name = {
                    '中行':'中国银行',
                    '工行':'工商银行',
                    '农行':'农业银行',
                    '建行':'建设银行'
        }
        for nc_idx in nc_bank_transfer.index:
            cond1 = (self.boc['支出']==self.nc_boc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.boc['交易日期']== self.nc_boc.loc[nc_idx,'交易日期']) #交易时间相同
            boc_bank_transfer = self.boc[(cond1 & cond2)]

            bank_regex = re.compile(r'\d+\.\d+(.*)\d{4}到(.*)\d{4}')
            from_to = bank_regex.search(self.nc_boc.loc[nc_idx,'摘要']).groups()
            from_bank = from_to[0]
            to_bank = from_to[1]
            for idx in boc_bank_transfer.index:
                from_cond = bank_name.get(from_bank) in boc_bank_transfer.loc[idx,'付款人开户行名'] 
                to_cond = bank_name.get(to_bank) in boc_bank_transfer.loc[idx,'收款人开户行名']
                if from_cond and to_cond: # 跨行起始一致
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx                    
        
        for nc_idx in nc_bank_transfer.index:
            cond1 = (self.boc['收入']==self.nc_boc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.boc['交易日期']== self.nc_boc.loc[nc_idx,'交易日期']) #交易时间相同
            boc_bank_transfer = self.boc[(cond1 & cond2)]

            bank_regex = re.compile(r'\d+\.\d+(.*)\d{4}到(.*)\d{4}')
            from_to = bank_regex.search(self.nc_boc.loc[nc_idx,'摘要']).groups()
            from_bank = from_to[0]
            to_bank = from_to[1]
            for idx in boc_bank_transfer.index:
                from_cond = bank_name.get(from_bank) in boc_bank_transfer.loc[idx,'付款人开户行名'] 
                to_cond = bank_name.get(to_bank) in boc_bank_transfer.loc[idx,'收款人开户行名']
                if from_cond and to_cond: # 跨行起始一致
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx                    
    

    def inner_transfer(self):
        '''
        内部转款
        eg:
        内部转账（10482~9037）
        
        rule:
            1. 借贷金额相同
            2. 银行——对方账号：22910801040009037
            3. 银行——交易附言: 往来款-CC00000GEL.

        eg2:【资金系统】
        2019-09-02内部转款
        rule:
            1. 借贷金额相同
            2. 交易时间相同
            3. 暂无其他可用约束条件
        '''
        regex_inner_transfer = re.compile(r'.*内部转[账帐款].*')
        is_inner_transfer = self.nc_boc['摘要'].str.match(regex_inner_transfer)
        nc_inner_transfer = self.nc_boc[is_inner_transfer]
        
        # rule1
        for nc_idx in nc_inner_transfer.index:
            cond1 = (self.boc['支出']==self.nc_boc.loc[nc_idx,'贷方']) #借贷金额相同
            boc_inner_transfer = self.boc[(cond1)]

            for idx in boc_inner_transfer.index:
                bank_number = re.findall(r'(\d+)[~-——](\d+)',self.nc_boc.loc[nc_idx,'摘要']) #[('10482', '9037')]
                try:
                    otherside_cond = (str(boc_inner_transfer.loc[idx,"对方账号"]).endswith(bank_number[0][1]))
                    substract_cond1 = ("往来款" in boc_inner_transfer.loc[idx,'用途'])
                    substract_cond2 = ("往来款" in boc_inner_transfer.loc[idx,'用途_原'])
                    if (otherside_cond and substract_cond1) or (otherside_cond and substract_cond2):
                        self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                        self.boc.loc[idx,'对账一致'] = 'yes'
                        self.nc_boc.loc[nc_idx,'银行索引'] = idx
                        self.boc.loc[idx,'NC索引'] = nc_idx
                except IndexError:
                    pass

        # rule1_
        for nc_idx in nc_inner_transfer.index:
            cond1 = (self.boc['收入']==self.nc_boc.loc[nc_idx,'借方']) #借贷金额相同
            boc_inner_transfer = self.boc[(cond1)]

            for idx in boc_inner_transfer.index:
                bank_number = re.findall(r'(\d+)[~-——](\d+)',self.nc_boc.loc[nc_idx,'摘要']) #[('10482', '9037')]
                try:
                    otherside_cond = (str(boc_inner_transfer.loc[idx,"对方账号"]).endswith(bank_number[0][1]))
                    substract_cond1 = ("往来款" in boc_inner_transfer.loc[idx,'用途'])
                    substract_cond2 = ("往来款" in boc_inner_transfer.loc[idx,'用途_原'])
                    if (otherside_cond and substract_cond1) or (otherside_cond and substract_cond2):
                        self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                        self.boc.loc[idx,'对账一致'] = 'yes'
                        self.nc_boc.loc[nc_idx,'银行索引'] = idx
                        self.boc.loc[idx,'NC索引'] = nc_idx
                except IndexError:
                    pass

        # # 资金系统汇总情形: 这个和银行手续费有冲突 ！！！
        # nc_inner_transfer_cond = (nc_inner_transfer['贷方'].notnull() & nc_inner_transfer['贷方']!=0. & nc_inner_transfer['贷方'].astype(str).str.strip()!='')
        # for nc_idx in nc_inner_transfer[nc_inner_transfer_cond].index:
        #     boc_sum_cond = (self.boc['支出'].notnull() & self.boc['支出']!=0. & self.boc['支出'].str.strip()!='')
        #     boc_inner_transfer = self.boc[boc_sum_cond]
        #     boc_sum_inner_transfer = boc_inner_transfer.groupby(
        #         ['交易日期', '对方户名'])['支出'].sum().reset_index().rename(columns={'支出': '支出和'})

        #     for sum_idx in boc_sum_inner_transfer.index:
        #         if boc_sum_inner_transfer.loc[sum_idx,'支出和']==nc_inner_transfer.loc[nc_idx,'贷方']:
        #             boc_idxs_cond1 = (boc_inner_transfer['交易日期']== boc_sum_inner_transfer.loc[sum_idx,'交易日期'])
        #             boc_idxs = boc_inner_transfer[(boc_idxs_cond1)].index

        #             self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
        #             self.boc.loc[boc_idxs,'对账一致'] = 'yes'
        #             self.nc_boc.loc[nc_idx,'银行索引'] = ';'.join(map(str,boc_idxs.values))
        #             self.boc.loc[boc_idxs,'NC索引'] = nc_idx

        # # 资金系统汇总情形_:
        # nc_inner_transfer_cond = (nc_inner_transfer['借方'].notnull(
        # ) & nc_inner_transfer['借方'] != 0. & nc_inner_transfer['借方'].astype(str).str.strip() != '')
        # for nc_idx in nc_inner_transfer[nc_inner_transfer_cond].index:
        #     boc_sum_cond = (self.boc['收入'].notnull() & self.boc['收入'] != 0. & self.boc['收入'].str.strip()!='')
        #     boc_inner_transfer = self.boc[boc_sum_cond]
        #     boc_sum_inner_transfer = boc_inner_transfer.groupby(
        #         ['交易日期', '对方户名'])['收入'].sum().reset_index().rename(columns={'收入': '收入和'})

        #     for sum_idx in boc_sum_inner_transfer.index:
        #         if boc_sum_inner_transfer.loc[sum_idx,'收入和']==nc_inner_transfer.loc[nc_idx,'借方']:
        #             boc_idxs_cond1 = (boc_inner_transfer['交易日期']== boc_sum_inner_transfer.loc[sum_idx,'交易日期'])
        #             boc_idxs = boc_inner_transfer[(boc_idxs_cond1)].index

        #             self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
        #             self.boc.loc[boc_idxs,'对账一致'] = 'yes'
        #             self.nc_boc.loc[nc_idx,'银行索引'] = ';'.join(map(str,boc_idxs.values))
        #             self.boc.loc[boc_idxs,'NC索引'] = nc_idx


        # 资金系统rule1
        for nc_idx in nc_inner_transfer.index:
            cond1 = (self.boc['支出']==self.nc_boc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.boc['交易日期']==self.nc_boc.loc[nc_idx,'交易日期']) #交易时间相同
            boc_inner_transfer = self.boc[(cond1&cond2)]

            for idx in boc_inner_transfer.index:
                time_cond = (boc_inner_transfer.loc[idx,'交易日期']==self.nc_boc.loc[nc_idx,'交易日期'])
                if time_cond:
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx

        # 资金系统rule2
        for nc_idx in nc_inner_transfer.index:
            cond1 = (self.boc['收入']==self.nc_boc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.boc['交易日期']==self.nc_boc.loc[nc_idx,'交易日期']) #交易时间相同
            boc_inner_transfer = self.boc[(cond1&cond2)]

            for idx in boc_inner_transfer.index:
                time_cond = (boc_inner_transfer.loc[idx,'交易日期']==self.nc_boc.loc[nc_idx,'交易日期'])
                if time_cond:
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx


    def deal_laowang(self):
        '''
        处理王镜淇
        eg: 8.16收到王镜淇款项/2019-08-20付王镜淇往来款<br>
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——付款人名称[ Payer's Name ]：王镜淇<br>
           银行——收款人名称[ Payee's Name ]：王镜淇
        '''
        is_laowang = self.nc_boc['摘要'].str.contains('王镜淇')
        nc_laowang = self.nc_boc[is_laowang]
        
        for nc_idx in nc_laowang.index:
            cond1 = (self.boc['收入']==self.nc_boc.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.boc['交易日期']==self.nc_boc.loc[nc_idx,'交易日期']) #交易时间相同
            boc_laowang = self.boc[(cond1 & cond2)]

            for idx in boc_laowang.index:
                if boc_laowang.loc[idx,"对方户名"] in self.nc_boc.loc[nc_idx,'摘要']:
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx                    
        
        for nc_idx in nc_laowang.index:
            cond1 = (self.boc['支出']==self.nc_boc.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.boc['交易日期']==self.nc_boc.loc[nc_idx,'交易日期']) #交易时间相同
            boc_laowang = self.boc[(cond1 & cond2)]

            for idx in boc_laowang.index:
                if boc_laowang.loc[idx,"对方户名"] in self.nc_boc.loc[nc_idx,'摘要']:
                    self.nc_boc.loc[nc_idx,'对账一致'] = 'yes'
                    self.boc.loc[idx,'对账一致'] = 'yes'
                    self.nc_boc.loc[nc_idx,'银行索引'] = idx
                    self.boc.loc[idx,'NC索引'] = nc_idx                    

    def export_excel(self):
        nc_rows_counts = self.nc_boc['对账一致'].value_counts(dropna=False)
        boc_rows_counts = self.boc['对账一致'].value_counts(dropna=False)

        try:
            nc_yes_rows = nc_rows_counts['yes']
        except KeyError:
            nc_yes_rows = 0
        nc_notmatch_rows = nc_rows_counts.sum()-nc_yes_rows

        try:
            boc_yes_rows = boc_rows_counts['yes']
        except KeyError:
            boc_yes_rows = 0
        boc_notmatch_rows = boc_rows_counts.sum()-boc_yes_rows
        
        print('\n')
        print("+--------------------------------------------------+")
        print("¦                  RESULTS                         ¦")
        print("+--------------------------------------------------+")
        print("¦ EXCEL    ¦       NC_BOC     ¦        BOC         ¦")
        print("+--------------------------------------------------+")
        print("¦ TOTAL    ¦{0:^18}¦{1:^20}¦".format(nc_rows_counts.sum(),boc_rows_counts.sum()))
        print("+--------------------------------------------------+")
        print("¦ MATCH    ¦{0:^18}¦{1:^20}¦".format(nc_yes_rows,boc_yes_rows))
        print("+--------------------------------------------------+")
        print("¦ NOTMATCH ¦{0:^18}¦{1:^20}¦".format(nc_notmatch_rows,boc_notmatch_rows))
        print("+--------------------------------------------------+")
        print('\n')


        self.nc_boc['交易日期'] = self.nc_boc['交易日期'].astype(str).str.slice(0,10)
        self.boc['交易日期'] = self.boc['交易日期'].astype(str).str.slice(0,10)

        save_file = self.save_path + '\\' + self.nc_file_name + '+' + self.boc_file_name + '.xlsx'
        print("结果保存至:\n\t%s\n" %(save_file))
        # self.nc_boc.to_excel(self.save_path + '/nc_boc.xlsx')
        # self.boc.to_excel(self.save_path + '/boc.xlsx')
        writer = pd.ExcelWriter(save_file,engine='xlsxwriter')
        self.nc_boc.to_excel(writer,sheet_name=self.nc_file_name,startrow=1,startcol=1,header=False,index=False)
        self.boc.to_excel(writer,sheet_name=self.boc_file_name,startrow=1,startcol=1,header=False,index=False)
        
        workbook = writer.book
        nc_sheet = writer.sheets[self.nc_file_name]
        boc_sheet = writer.sheets[self.boc_file_name]

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
        
        nc_rows,nc_cols = self.nc_boc.shape
        for i in range(nc_rows+5):
            nc_sheet.set_row(i,22,cell_format)

        yes_index = self.nc_boc[self.nc_boc['对账一致']=='yes'].index+1
        for i in yes_index:
            nc_sheet.set_row(i,22,yes_format)

        # col format
        nc_sheet.set_column(0,nc_cols+5,22)

        nc_sheet.write_row('B1',self.nc_boc.columns,header_format)
        nc_sheet.write_column('A2',self.nc_boc.index,header_format)
        nc_sheet.freeze_panes(1,1)
        nc_sheet.set_tab_color('#FF9900')

        #boc
        # row format
        boc_rows,boc_cols = self.boc.shape
        for i in range(boc_rows+5):
            boc_sheet.set_row(i,22,cell_format)

        yes_index = self.boc[self.boc['对账一致']=='yes'].index+1
        for i in yes_index:
            boc_sheet.set_row(i,22,yes_format)

        # col format
        boc_sheet.set_column(0,boc_cols+5,22)

        boc_sheet.write_row('B1',self.boc.columns,header_format)
        boc_sheet.write_column('A2',self.boc.index,header_format)
        boc_sheet.freeze_panes(1,1)
        boc_sheet.set_tab_color('#FF9900')

        writer.save()

    def doall(self):
        self.rec_mortgage()
        self.pos_to_bank()
        self.rec_pos()
        self.rec_loans()
        self.rec_appointment_building()
        self.rec_pfund()
        self.rec_fee()
        self.rec_firmamount()

        self.prepay_amount()
        self.pay_bankfee()
        self.pay_progressamount()
        self.pay_group()
        self.pay_firmamount()

        self.capital_pool()
        self.bank_transfer()
        self.inner_transfer()
        self.deal_laowang()
        self.export_excel()

    def __call__(self):
        return self.doall()
