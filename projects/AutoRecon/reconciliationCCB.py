#!/usr/bin/env python
# coding: utf-8
# 建行对账
# 
import pandas as pd
import numpy as np
import re
import xlsxwriter

# 整理表格
class DealExcelCCB(object):
    def __init__(self,nc_path,bank_path):
        self.nc_path = nc_path
        self.bank_path = bank_path

    def dealNC(self):
        # read
        nc_ccb = pd.read_excel(self.nc_path,header=None)
        nc_ccb = nc_ccb.dropna(how='all')

        # deal year/head/tail
        year = nc_ccb.iloc[0,0]
        init_period = nc_ccb.iloc[2,:] # 暂时保存期初行
        month_year_sum = nc_ccb.tail(2) # 暂时保存本月及本年累计行

        # drop useless rows
        nc_ccb.columns = nc_ccb.iloc[1,:] 
        nc_ccb = nc_ccb.drop([0,1,2]) 
        nc_ccb = nc_ccb.head(len(nc_ccb)-2)

        time = str(year) + '-' + nc_ccb['月'].astype(str) + '-' + nc_ccb['日'].astype(str)
        nc_ccb.insert(0,'日期',pd.to_datetime(time,format='%Y-%m-%d').astype(str).str.slice(0,10))

        nc_ccb.reset_index(drop=True,inplace=True)

        # 提取交易时间
        time_pattern1 = re.compile(r'\d{4}-\d+-\d+')
        time_pattern2 = re.compile(r'\d{4}\.\d+\.\d+')
        time_pattern3 = re.compile(r'\d+\.\d+')

        transac_time = nc_ccb['摘要'].copy()
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

        nc_ccb.insert(6,'交易日期',transac_time)
        nc_ccb['交易日期']=pd.to_datetime(transac_time,format='%Y-%m-%d')

        # 生成对账标记
        nc_ccb.insert(0,"银行索引",None)
        nc_ccb.insert(0,'对账一致',None)

        # 转换字段类型
        nc_ccb.columns = list(map(lambda x: str(x).strip(),nc_ccb.columns))
        nc_ccb.loc[:,['银行账户名称','摘要']] = nc_ccb[['银行账户名称','摘要']].apply(lambda s: s.str.strip().str.replace('[ （）()]',''))
        nc_ccb.loc[:,['借方','贷方','余额']] = nc_ccb[['借方','贷方','余额']].apply(lambda s: s.astype(np.float64))

        nc_ccb.drop(['月','日'],axis=1,inplace=True)

        return nc_ccb

    def dealBANK(self):
        # read
        ccb = pd.read_excel(self.bank_path,header=None)
        ccb = ccb.dropna(how='all')
        
        if ccb.iloc[0,0]=='组织':
            ccb.columns = ccb.loc[0,:]
            ccb = ccb.drop(0)
            
            need_fields = ["组织","银行","账号","币种","交易日期","收入","支出","当前余额", 
                           "用途","对方户名", "对方账号","对方开户机构","来源","备注","业务类型","资金系统单据号"]
            for col in need_fields:
                if col not in ccb.columns:
                    ccb[col] = None
            ccb['交易日期'] = pd.to_datetime(ccb['交易日期'])

            strip_fields = ["组织","账号","币种","用途","对方户名","备注","业务类型"]
            ccb.loc[:,strip_fields] = ccb[strip_fields].apply(lambda s: s.str.strip().str.replace('[ （）()]',''))
            
        else:
            # drop useless rows
            for row in ccb.index:
                for col in ccb.columns:
                    if str(ccb.loc[row,col]).strip()=='交易时间':
                        header_row = row
            #             print(header_row)
                        break
            ccb.columns = ccb.loc[header_row,:]
            ccb = ccb.loc[header_row+1:,:]
            
            
            # transform columns
            ccb.columns = list(map(lambda x: str(x).strip(),ccb.columns))
    
            if "账户名称" not in ccb.columns:
                ccb['账户名称'] = None
                
            if "账号" not in ccb.columns:
                ccb['账号'] = None
                
            rename_dict = {
                "账户名称":"组织",
                "交易时间": "交易日期",
                "贷方发生额（收入）":"收入",
                "贷方发生额/元(收入)":"收入",
                "借方发生额（支取）":"支出",
                "借方发生额/元(支取)":"支出",
                "余额":"当前余额",
                "摘要":"用途",
                "凭证种类":"业务类型",
            }
    
            ccb.rename(columns=rename_dict,inplace=True)
    
            ccb['交易日期'] = pd.to_datetime(ccb['交易日期'].str.slice(0,8),format='%Y-%m-%d')  
            
            ccb["银行"] = 'CCB-建设银行'
            ccb["来源"] = 'U-CCB'
            ccb['资金系统单据号'] = None
    
            # drop useless columns
            need_fields = ["组织","银行","账号","币种","交易日期","收入","支出","当前余额", 
                           "用途","对方户名", "对方账号","对方开户机构","来源","备注","业务类型","资金系统单据号"]
            ccb = ccb[need_fields]
            
            strip_fields = ["组织","账号","币种","用途","对方户名","备注","业务类型","对方开户机构"]
            ccb.loc[:,strip_fields] = ccb[strip_fields].apply(lambda s: s.str.strip().str.replace('[ （）()]',''))
        
        # 对账标记
        ccb.insert(0,"NC索引",None)
        ccb.insert(0,'对账一致',None)
        ccb.reset_index(inplace=True)
        ccb.sort_values(['index'])
        ccb.drop(['index'],axis=1,inplace=True)

        num_fields = ['收入','支出','当前余额']
        ccb.loc[:,num_fields] = ccb[num_fields].apply(lambda s: s.replace({'-':None}).astype(np.float64))

        return ccb

# 对账规则
class CheckCCB(object):
    def __init__(self,nc_ccb,ccb,nc_file_name,ccb_file_name,save_path=None):
        self.nc_ccb = nc_ccb
        self.ccb = ccb
        self.nc_file_name = nc_file_name
        self.ccb_file_name = ccb_file_name
        self.save_path = save_path

    def rec_mortgage(self):
        '''
        收取银行按揭
        eg：
        NC摘要：2019-08-01收陈娇;施前杰[眉山]蘭台府-蘭台府一期-11-1803银行按揭 <br>
        rule:<br>
        1. NC<->银行：<br>
            借方<->贷方发生额（收入）
        2. 银行——对方户名：个贷系统平账专户
        3. 银行——备注：给施前杰的贷款
        4. 交易时间相同
        '''
        regex_mortgage = re.compile(r'.*收.*银行按揭$')
        is_mortgage = self.nc_ccb['摘要'].str.match(regex_mortgage)
        nc_mortgage = self.nc_ccb[is_mortgage]

        for nc_idx in nc_mortgage.index:
            cond1 = (self.ccb['收入']==self.nc_ccb.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            ccb_mortgage = self.ccb[(cond1 & cond2)]

            for idx in ccb_mortgage.index:
                name_regex = re.compile(r'.*给(.*)的贷款.*')
                name = name_regex.findall(ccb_mortgage.loc[idx,'备注'])[0]

                otherside_cond = (ccb_mortgage.loc[idx,'对方户名']=="个贷系统平账专户")
                substract_cond = (name in self.nc_ccb.loc[nc_idx,'摘要'])
                if  otherside_cond and substract_cond: # 对方户名为 nc摘要中的姓名
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx                    

    def rec_pfund(self):
        '''
        收取公积金
        eg：
        NC摘要：2019-08-02收张凤;黄永刚[眉山]蘭台府-蘭台府一期-01-1101公积金 <br>
        rule:<br>
        1. NC<->银行：<br>
            借方<->贷方发生额（收入）
        2. 银行——对方户名：个贷系统平账专户
        3. 银行——备注：给黄永刚的贷款
        3_. 银行——用途: 给黄永刚的贷款 【资金系统】
        4. 交易时间相同
        '''        
        regex_pfund = re.compile(r'.*收.*公积金$')
        is_pfund = self.nc_ccb['摘要'].str.match(regex_pfund)
        nc_pfund = self.nc_ccb[is_pfund]
        
        for nc_idx in nc_pfund.index:
            cond1 = (self.ccb['收入']==self.nc_ccb.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            ccb_pfund = self.ccb[(cond1&cond2)]

            for idx in ccb_pfund.index:
                name_regex = re.compile(r'.*给(.*)的贷款.*')
                name_u = name_regex.findall(ccb_pfund.loc[idx,'备注'])[0]
                name_cs = name_regex.findall(ccb_pfund.loc[idx,'用途'])[0]
                otherside_cond = (ccb_pfund.loc[idx,'对方户名']=="个贷系统平账专户") 
                substract_cond = (name_u in self.nc_ccb.loc[nc_idx,'摘要']) # 对方户名为 nc摘要中的姓名
                purpose_cond = (name_cs in self.nc_ccb.loc[nc_idx,'摘要'])

                if  otherside_cond and (substract_cond or purpose_cond): 
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx                    

    def save_margin(self):
        '''
        存建行保证金——未解决
        eg:存建行保证金
        【银行无对应账，暂时无法提取规则】
        '''
        pass


    def rec_appointment_building(self):
        '''
        收楼款/收定金/收预约金/收垫付款
        eg:
            2019-09-09收黄丽萍[乐山]蘭台府-四期-1号楼-2-403定金
            2019-09-09收彭春燕;耿勇[乐山]蘭台府-四期-1号楼-2-806垫付款
            2019-09-09收汤富林[乐山]蘭台府-四期-1号楼-1-2201楼款
            2019-09-08收夏小琼[乐山]蘭台府-四期-1号楼-1-701预约金
        
        rule1:
            > 逐笔比对
            1. 借贷金额相同
            2. 交易时间相同
            3. 银行——对方用户: 黄丽萍/彭春燕/汤富林/夏小琼

        rule2:
            > nc为多笔金额，银行为汇总数
            
            1. 交易时间相同【X 差一天】
            2. 银行——对方户名：银联商务股份有限公司客户备付金
            3. 汇总nc金额
            4. 银行金额=nc汇总金额
            5. 银行——用途：0905-0905费0元【1.改用5.作为rule3】
        '''   
        # rule1
        regex_appointment_building = re.compile(r'.*收.*定金$|.*收.*楼款$|.*收.*预约金$|.*收.*垫付款$')
        is_appointment_building = self.nc_ccb['摘要'].str.match(regex_appointment_building)
        nc_appointment_building = self.nc_ccb[is_appointment_building]

        for nc_idx in nc_appointment_building.index:
            cond1 = (self.ccb['收入']==self.nc_ccb.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']== self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            ccb_appointment_building = self.ccb[(cond1 & cond2)]

            for idx in ccb_appointment_building.index:
                if ccb_appointment_building.loc[idx,"对方户名"] in self.nc_ccb.loc[nc_idx,'摘要']: # 对方单位为 nc摘要中的姓名
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx

        # rule2
        nc_sum_appointment_building = nc_appointment_building.groupby(['交易日期'])['借方'].sum().reset_index().rename(columns={"借方":"借方和"})

        for sum_idx in nc_sum_appointment_building.index:
            time_cond = (self.ccb['交易日期']==nc_sum_appointment_building.loc[sum_idx,'交易日期'])
            otherside_cond = (self.ccb['对方户名'].str.strip()=="银联商务股份有限公司客户备付金")
            ccb_appointment_building = self.ccb[(time_cond&otherside_cond)]

            for idx in ccb_appointment_building.index:
                if ccb_appointment_building.loc[idx,'收入'] == nc_sum_appointment_building.loc[sum_idx,'借方和']:
                    idxs_cond = (nc_appointment_building['交易日期']==nc_sum_appointment_building.loc[sum_idx,'交易日期'])
                    nc_idxs = nc_appointment_building[idxs_cond].index
                    
                    self.nc_ccb.loc[nc_idxs,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idxs,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = ";".join(map(str,nc_idxs.values))

        # rule3
        nc_sum_appointment_building = nc_appointment_building.groupby(['交易日期'])['借方'].sum().reset_index().rename(columns={"借方":"借方和"})

        for sum_idx in nc_sum_appointment_building.index:
            purpose_cond = (self.ccb['用途'].str.match(r'\d{4}-\d{4}费'))
            otherside_cond = (self.ccb['对方户名'].str.strip()=="银联商务股份有限公司客户备付金")
            ccb_appointment_building = self.ccb[(purpose_cond&otherside_cond)]

            for idx in ccb_appointment_building.index:
                if ccb_appointment_building.loc[idx,'收入'] == nc_sum_appointment_building.loc[sum_idx,'借方和']:
                    idxs_cond = (nc_appointment_building['交易日期']==nc_sum_appointment_building.loc[sum_idx,'交易日期'])
                    nc_idxs = nc_appointment_building[idxs_cond].index
                    
                    self.nc_ccb.loc[nc_idxs,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idxs,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = ";".join(map(str,nc_idxs.values))

    
    def rec_reservefund(self):
        '''
        收取备用金
        eg:
            收到zhouy-周杨(乐山)归还F0401-备用金
        
        rule:
            1. 借贷金额相同
            2. 银行——对方单位: 周杨
        '''
        regex_rec_reservefund = re.compile(r'收.*归还.*备用金$')
        is_rec_reservefund = self.nc_ccb['摘要'].str.match(regex_rec_reservefund)
        nc_rec_reservefund = self.nc_ccb[is_rec_reservefund]

        for nc_idx in nc_rec_reservefund.index:
            cond1 = (self.ccb['收入']==self.nc_ccb.loc[nc_idx,'借方']) #借贷金额相同
            ccb_rec_reservefund = self.ccb[cond1]

            for idx in ccb_rec_reservefund.index:
                otherside_cond = (ccb_rec_reservefund.loc[idx,'对方户名'] in self.nc_ccb.loc[nc_idx,'摘要'])
                if otherside_cond: # 对方单位为 nc摘要中的姓名/公司
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes' 
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx

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
        is_rec_bidbond = (self.nc_ccb['摘要'].str.match(regex_rec_bidbond))
        nc_rec_bidbond = self.nc_ccb[is_rec_bidbond]
        
        for nc_idx in nc_rec_bidbond.index:
            cond1 = (self.ccb['收入']==self.nc_ccb.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期'])
            ccb_rec_bidbond = self.ccb[(cond1&cond2)]

            for idx in ccb_rec_bidbond.index:
                otherside_cond = (str(ccb_rec_bidbond.loc[idx,"对方户名"]) in self.nc_ccb.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx

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
        is_rec_group = (self.nc_ccb['摘要'].str.match(regex_rec_group))
        nc_rec_group = self.nc_ccb[is_rec_group]
        
        for nc_idx in nc_rec_group.index:
            cond1 = (self.ccb['收入']==self.nc_ccb.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            ccb_rec_group = self.ccb[(cond1 & cond2)]

            for idx in ccb_rec_group.index:
                otherside_cond = (ccb_rec_group.loc[idx,"对方户名"].startswith('领地集团股份有限公司'))
                if otherside_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx

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
        is_rec_firmamount = (self.nc_ccb['摘要'].str.match(regex_rec_firmamount))
        nc_rec_firmamount = self.nc_ccb[is_rec_firmamount]
        
        for nc_idx in nc_rec_firmamount.index:
            cond1 = (self.ccb['收入']==self.nc_ccb.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.ccb['交易日期'] == self.nc_ccb.loc[nc_idx,'交易日期'])
            ccb_rec_firmamount = self.ccb[(cond1&cond2)]

            for idx in ccb_rec_firmamount.index:
                otherside_cond = (str(ccb_rec_firmamount.loc[idx,"对方户名"]) in self.nc_ccb.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx 

    def rec_bankfee(self):
        '''
        收银行利息
        eg: 2019-09-21银行结息
        	2019-09-21收银行利息
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行-用途：结息
        '''        
        regex_rec_bankfee = re.compile(r'.*行.*利息.*|.*行.*结息')
        is_rec_bankfee = self.nc_ccb['摘要'].str.match(regex_rec_bankfee)
        nc_rec_bankfee = self.nc_ccb[is_rec_bankfee]

        # rule1
        for nc_idx in nc_rec_bankfee.index:
            cond1 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            cond2 = (self.ccb['收入']==self.nc_ccb.loc[nc_idx,'借方']) #借贷金额相同
            ccb_rec_bankfee = self.ccb[(cond1 & cond2)]

            for idx in ccb_rec_bankfee.index:
                purpose_cond = ("结息" in ccb_rec_bankfee.loc[idx,'用途'])
                if purpose_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx
        # rule2
        for nc_idx in nc_rec_bankfee.index:
            cond1 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            cond2 = (self.ccb['用途']=='结息')
            ccb_rec_bankfee = self.ccb[(cond1 & cond2)]

            if ccb_rec_bankfee['支出'].sum()==self.nc_ccb.loc[nc_idx,'贷方']:
                self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                self.ccb.loc[ccb_rec_bankfee.index,'对账一致'] = 'yes'
                self.nc_ccb.loc[nc_idx,'银行索引'] = ';'.join(map(str,ccb_rec_bankfee.index.values))
                self.ccb.loc[ccb_rec_bankfee.index,'NC索引'] = nc_idx

    def pay_salary(self):
        '''
        计发工资
        eg: 计发7月工资/计发食堂员工7月工资
        
        ruel1:
            > 逐笔比对
            1. 借贷金额相同
            2. 银行——备注：8月工资
            3. 交易时间相同 【没有】
        
        rule2： 
        
            > nc为汇总数，可能是多笔汇总，银行是多笔金额 【需要双边汇总,汇总前无法通过金额进行匹配】
        
            1. 汇总nc工资数：贷方
            2. 银行——备注：8月工资
            3. 汇总银行支出金额
            4. nc汇总数=银行汇总金额
        '''

        regex_pay_salary = re.compile(r'.*发.*月工资.*')
        is_pay_salary = self.nc_ccb['摘要'].str.match(regex_pay_salary)
        nc_pay_salary = self.nc_ccb[is_pay_salary]        
        
        #rule1
        for nc_idx in nc_pay_salary.index:
            cond1 = (self.ccb['支出']==self.nc_ccb.loc[nc_idx,'贷方']) #借贷金额相同
            ccb_pay_salary = self.ccb[cond1]
            for idx in ccb_pay_salary.index:
                memo_cond = ("工资" in self.ccb.loc[idx,'备注'])
                if memo_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx                  

        # rule2
        salary_cond = (self.ccb['备注'].astype(str).str.contains('月工资'))
        ccb_pay_salary = self.ccb[salary_cond]
        
        if nc_pay_salary['贷方'].sum()==ccb_pay_salary['支出'].sum():
            self.nc_ccb.loc[nc_pay_salary.index,'对账一致'] = 'yes'
            self.ccb.loc[ccb_pay_salary.index,'对账一致'] = 'yes'
            self.nc_ccb.loc[nc_pay_salary.index,'银行索引'] = ';'.join(map(str,ccb_pay_salary.index.values))
            self.ccb.loc[ccb_pay_salary.index,'NC索引'] = ';'.join(map(str,nc_pay_salary.index.values))

    def pay_bankfee(self):
        '''
        支付银行手续费
        eg: 8.7中行6569手续费<br>
        
        rule:
        > 逐笔比对
        > nc是一个总额，银行为多笔金额
        
        1. 交易时间相同
        2. 银行-摘要：收费
        3. 汇总银行金额等于NC贷方金额
        '''        
        regex_pay_bankfee = re.compile(r'.*行.*手续费.*')
        is_pay_bankfee = self.nc_ccb['摘要'].str.match(regex_pay_bankfee)
        nc_pay_bankfee = self.nc_ccb[is_pay_bankfee]

        # rule1
        for nc_idx in nc_pay_bankfee.index:
            cond1 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            cond2 = (self.ccb['支出']==self.nc_ccb.loc[nc_idx,'贷方']) #借贷金额相同
            ccb_pay_bankfee = self.ccb[(cond1 & cond2)]

            for idx in ccb_pay_bankfee.index:
                purpose_cond = ("收费" in ccb_pay_bankfee.loc[idx,'用途'])
                if purpose_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx
        # rule2
        for nc_idx in nc_pay_bankfee.index:
            cond1 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            cond2 = (self.ccb['用途']=='收费')
            ccb_pay_bankfee = self.ccb[(cond1 & cond2)]

            if ccb_pay_bankfee['支出'].sum()==self.nc_ccb.loc[nc_idx,'贷方']:
                self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                self.ccb.loc[ccb_pay_bankfee.index,'对账一致'] = 'yes'
                self.nc_ccb.loc[nc_idx,'银行索引'] = ';'.join(map(str,ccb_pay_bankfee.index.values))
                self.ccb.loc[ccb_pay_bankfee.index,'NC索引'] = nc_idx

        # 资金系统rule1:
        regex_pay_bankfee = re.compile(r'.*\d+手续费$')
        is_pay_bankfee = self.nc_ccb['摘要'].str.match(regex_pay_bankfee)
        nc_pay_bankfee = self.nc_ccb[is_pay_bankfee]
              
        for nc_idx in nc_pay_bankfee.index:
            cond1 = (self.ccb['支出']==self.nc_ccb.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.ccb["对方户名"].isnull())
            ccb_pay_bankfee = self.ccb[(cond1&cond2)]
        
            for idx in ccb_pay_bankfee.index:
                purpose_cond = (ccb_pay_bankfee.loc[idx,'用途'].startswith("收费项目"))
                if purpose_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx

        # 资金系统rule2:
        for nc_idx in nc_pay_bankfee.index:
            cond1 = (self.ccb['用途'].str.startswith("收费项目"))
            cond2 = (self.ccb["对方户名"].isnull())
            ccb_pay_bankfee = self.ccb[(cond1&cond2)]

            ccb_sum_pay_bankfee = ccb_pay_bankfee.groupby(['交易日期'])['支出'].sum().reset_index().rename(columns={'支出':'支出和'})

            for sum_idx in ccb_sum_pay_bankfee.index:
                if ccb_sum_pay_bankfee.loc[sum_idx,'支出和']==nc_pay_bankfee.loc[nc_idx,'贷方']:
                    ccb_idxs_cond = (ccb_pay_bankfee['交易日期']==ccb_sum_pay_bankfee.loc[sum_idx,'交易日期'])
                    ccb_idxs = ccb_pay_bankfee[ccb_idxs_cond].index

                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[ccb_idxs,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = ';'.join(map(str,ccb_idxs.values))
                    self.ccb.loc[ccb_idxs,'NC索引'] = nc_idx

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
        is_pay_firmamount = (self.nc_ccb['摘要'].str.match(regex_pay_firmamount))
        nc_pay_firmamount = self.nc_ccb[is_pay_firmamount]
        
        for nc_idx in nc_pay_firmamount.index:
            cond1 = (self.ccb['支出']==self.nc_ccb.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期'])
            ccb_pay_firmamount = self.ccb[(cond1&cond2)]

            for idx in ccb_pay_firmamount.index:
                otherside_cond = (str(ccb_pay_firmamount.loc[idx,"对方户名"]) in self.nc_ccb.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx


    def pay_wechat(self):
        '''
        微信认证手续费
        eg: 9.7微信认证手续费
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——备注：微信认证，请转告陈星宇转账金额
        '''
        regex_pay_wechat = re.compile(r'.*微信认证.*')
        is_pay_wechat = self.nc_ccb['摘要'].str.match(regex_pay_wechat)
        nc_pay_wechat = self.nc_ccb[is_pay_wechat]
        
        for nc_idx in nc_pay_wechat.index:
            cond1 = (self.ccb['收入']==self.nc_ccb.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            ccb_pay_wechat = self.ccb[(cond1 & cond2)]
        #     print("---------------------------\n",ccb_pay_wechat) 
            for idx in ccb_pay_wechat.index:
                memo_cond = ('微信' in ccb_pay_wechat.loc[idx,"备注"])
                if memo_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx

    def pay_landmargin(self):
        '''
        付土地保证金
        eg: 2019-09-06支付土地保证金
        rule:
        1. 借贷金额相同
        2. 交易时间相同
        3. 银行——备注：顺庆区清泉寺片区Dc-1地块土地款
        '''
        regex_pay_landmargin = re.compile(r'.*付.*土地保证金')
        is_pay_landmargin = self.nc_ccb['摘要'].str.match(regex_pay_landmargin)
        nc_pay_landmargin = self.nc_ccb[is_pay_landmargin]
        
        for nc_idx in nc_pay_landmargin.index:
            cond1 = (self.ccb['支出']==self.nc_ccb.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            ccb_pay_landmargin = self.ccb[(cond1 & cond2)]
        #     print("---------------------------\n",ccb_pay_landmargin) 
            for idx in ccb_pay_landmargin.index:
                memo_cond = ('土地' in ccb_pay_landmargin.loc[idx,"备注"])
                if memo_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx    

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
        is_pay_group = self.nc_ccb['摘要'].str.match(regex_pay_group)
        nc_pay_group = self.nc_ccb[is_pay_group]
        
        for nc_idx in nc_pay_group.index:
            cond1 = (self.ccb['支出']==self.nc_ccb.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            ccb_pay_group = self.ccb[(cond1 & cond2)]
        #     print("---------------------------\n",ccb_pay_group) 
            for idx in ccb_pay_group.index:
                otherside_cond = (ccb_pay_group.loc[idx,"对方户名"].startswith('领地集团股份有限公司'))
                if otherside_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx

    def prepay_firmamount(self):
        '''
        预付公司款项/支付公司预付款
        eg:<br>
        预付2910102-成都京东世纪贸易有限公司F030207 -已成交客户回馈款<br>
        预付2910102-成都京东世纪贸易有限公司F020202-生日款<br>
        预付00001043-国网四川省电力公司眉山供电公司F01050203-工程类水电费款<br>
        支付迅达（中国）电梯有限公司乐山领地澜山项目二期电梯采购及安装工程施工合同预付款
        预付00005422-杜小英龙景苑4-2-401F020211-员工宿舍费用款GYSYFK-190909-000634
        rule:
        1. 借贷金额相同
        2. 银行——对方单位：成都京东世纪贸易有限公司/国网四川省电力公司眉山供电公司/迅达（中国）电梯有限公司
        '''
        
        regex_prepay_firm_amount = re.compile(r'预付.*公司.*款.*|支付.*公司.*预付款.*|预付.*员工.*款.*')
        is_prepay_firm_amount = self.nc_ccb['摘要'].str.match(regex_prepay_firm_amount)
        nc_prepay_firm_amount = self.nc_ccb[is_prepay_firm_amount]
        
        for nc_idx in nc_prepay_firm_amount.index:
            cond1 = (self.ccb['支出']==self.nc_ccb.loc[nc_idx,'贷方']) #借贷金额相同
            ccb_prepay_firm_amount = self.ccb[(cond1)]

            for idx in ccb_prepay_firm_amount.index:
                receiver_cond = ccb_prepay_firm_amount.loc[idx,'对方户名'] in self.nc_ccb.loc[nc_idx,'摘要'] # 对方单位是 nc摘要中的公司
                if receiver_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx


    def pay_refund(self):
        '''
        退楼款/退违约金/退待退款项/退预约金
        eg:
            2019-09-04退陈玉[乐山]蘭台府-二期-6号楼-1101楼款
            2019-09-04退张玉娇[乐山]蘭台府-三期-2号楼-1204违约金
            2019-09-04退何平[乐山]蘭台府-三期-2号楼-1403待退款项
            2019-09-04退巫新娥[乐山]蘭台府-三期-2号楼-604预约金
        
        rule:
            1. 借贷金额相同
            2. 交易时间相同
            3. 银行——对方户名：姓名
        '''
        regex_appointment_refund = re.compile(r'.*退.*待退款项.*|.*退.*[预违]约金.*|.*退.*楼款.*')
        is_appointment_refund = self.nc_ccb['摘要'].str.match(regex_appointment_refund)
        nc_appointment_refund = self.nc_ccb[is_appointment_refund]
               
        for nc_idx in nc_appointment_refund.index:
            cond1 = (self.ccb['支出']==self.nc_ccb.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            ccb_appointment_refund = self.ccb[(cond1&cond2)]

            for idx in ccb_appointment_refund.index:
                otherside_cond = (ccb_appointment_refund.loc[idx,'对方户名'] in self.nc_ccb.loc[nc_idx,'摘要']) # 对方单位为 nc摘要中的姓名

                if otherside_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx

    def pay_reimburse(self):
        '''
        支付报销款
        eg:
            支付1020202284-中国邮政速递物流股份有限公司乐山市分公司报销F010102-快递费款
        
        rule:
            1. 借贷金额相同
            2. 银行——对方户名: 中国邮政速递物流股份有限公司
        '''
        regex_pay_reimburse = re.compile(r'支付.*报销.*款$')
        is_pay_reimburse = self.nc_ccb['摘要'].str.match(regex_pay_reimburse)
        nc_pay_reimburse = self.nc_ccb[is_pay_reimburse]

        for nc_idx in nc_pay_reimburse.index:
            cond1 = (self.ccb['支出']==self.nc_ccb.loc[nc_idx,'贷方']) #借贷金额相同
            ccb_pay_reimburse = self.ccb[cond1]

            for idx in ccb_pay_reimburse.index:
                otherside_cond = (ccb_pay_reimburse.loc[idx,'对方户名'] in self.nc_ccb.loc[nc_idx,'摘要'])
                if otherside_cond: # 对方单位为 nc摘要中的姓名/公司
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes' 
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx

    def pay_bidbond(self):
        '''
        退投标保证金
        eg：
            2019-09-05 退四川创佳暖通有限公司投标保证金
        
        rule:
            1.借贷金额相同
            2.交易时间相同
            3.银行——对方户名：四川创佳暖通设备有限公司 
        '''
        regex_pay_bidbond = re.compile(r'.*退.*投标保证金')
        is_pay_bidbond = (self.nc_ccb['摘要'].str.match(regex_pay_bidbond))
        nc_pay_bidbond = self.nc_ccb[is_pay_bidbond]
        
        for nc_idx in nc_pay_bidbond.index:
            cond1 = (self.ccb['支出']==self.nc_ccb.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期'])
            ccb_pay_bidbond = self.ccb[(cond1&cond2)]

            for idx in ccb_pay_bidbond.index:
                otherside_cond = (str(ccb_pay_bidbond.loc[idx,"对方户名"]) in self.nc_ccb.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx


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
        is_return_loans = self.nc_ccb['摘要'].str.match(regex_return_loans)
        nc_return_loans = self.nc_ccb[is_return_loans]
        
        for nc_idx in nc_return_loans.index:
            cond1 = (self.ccb['支出']==self.nc_ccb.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) # 交易时间相同
            ccb_return_loans = self.ccb[(cond1 & cond2)]

            for idx in ccb_return_loans.index:
                otherside_cond = (ccb_return_loans.loc[idx,'对方户名'] in self.nc_ccb.loc[nc_idx,'摘要'])
                if otherside_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx 


    def inner_transfer(self):
        '''
        内部转账
        eg:【资金系统】
        2019-09-02内部转款

        rule:
            1. 借贷金额相同
            2. 交易时间相同
            3. 银行——备注：网络转账;刘小荣;7-1-201;汇户;1091
        '''
        regex_inner_transfer = re.compile(r'.*内部转[款账帐].*')
        is_inner_transfer = self.nc_ccb['摘要'].str.match(regex_inner_transfer)
        nc_inner_transfer = self.nc_ccb[is_inner_transfer]
               
        for nc_idx in nc_inner_transfer.index:
            cond1 = (self.ccb['支出']==self.nc_ccb.loc[nc_idx,'贷方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            ccb_inner_transfer = self.ccb[(cond1&cond2)]

            for idx in ccb_inner_transfer.index:
                memo_cond = ("网络转账" in ccb_inner_transfer.loc[idx,'备注'])
                if memo_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx

        for nc_idx in nc_inner_transfer.index:
            cond1 = (self.ccb['收入']==self.nc_ccb.loc[nc_idx,'借方']) #借贷金额相同
            cond2 = (self.ccb['交易日期']==self.nc_ccb.loc[nc_idx,'交易日期']) #交易时间相同
            ccb_inner_transfer = self.ccb[(cond1&cond2)]

            for idx in ccb_inner_transfer.index:
                memo_cond = ("网络转账" in ccb_inner_transfer.loc[idx,'备注'])
                if memo_cond:
                    self.nc_ccb.loc[nc_idx,'对账一致'] = 'yes'
                    self.ccb.loc[idx,'对账一致'] = 'yes'
                    self.nc_ccb.loc[nc_idx,'银行索引'] = idx
                    self.ccb.loc[idx,'NC索引'] = nc_idx            


    def export_excel(self):
        nc_rows_counts = self.nc_ccb['对账一致'].value_counts(dropna=False)
        ccb_rows_counts = self.ccb['对账一致'].value_counts(dropna=False)

        try:
            nc_yes_rows = nc_rows_counts['yes']
        except KeyError:
            nc_yes_rows = 0
        nc_notmatch_rows = nc_rows_counts.sum()-nc_yes_rows

        try:
            ccb_yes_rows = ccb_rows_counts['yes']
        except KeyError:
            ccb_yes_rows = 0
        ccb_notmatch_rows = ccb_rows_counts.sum()-ccb_yes_rows
        

        print('\n')
        print("+--------------------------------------------------+")
        print("¦                  RESULTS                         ¦")
        print("+--------------------------------------------------+")
        print("¦ EXCEL    ¦       NC_CCB     ¦         CCB        ¦")
        print("+--------------------------------------------------+")
        print("¦ TOTAL    ¦{0:^18}¦{1:^20}¦".format(nc_rows_counts.sum(),ccb_rows_counts.sum()))
        print("+--------------------------------------------------+")
        print("¦ MATCH    ¦{0:^18}¦{1:^20}¦".format(nc_yes_rows,ccb_yes_rows))
        print("+--------------------------------------------------+")
        print("¦ NOTMATCH ¦{0:^18}¦{1:^20}¦".format(nc_notmatch_rows,ccb_notmatch_rows))
        print("+--------------------------------------------------+")
        print('\n')


        self.nc_ccb['交易日期'] = self.nc_ccb['交易日期'].astype(str).str.slice(0,10)
        self.ccb['交易日期'] = self.ccb['交易日期'].astype(str).str.slice(0,10)

        
        save_file = self.save_path + '\\' + self.nc_file_name + '+' + self.ccb_file_name + '.xlsx'
        print("结果保存至:\n\t%s\n" %(save_file))
        # self.nc_ccb.to_excel(self.save_path + '/nc_ccb.xlsx')
        # self.ccb.to_excel(self.save_path + '/ccb.xlsx')
        writer = pd.ExcelWriter(save_file,engine='xlsxwriter')
        self.nc_ccb.to_excel(writer,sheet_name=self.nc_file_name,startrow=1,startcol=1,header=False,index=False)
        self.ccb.to_excel(writer,sheet_name=self.ccb_file_name,startrow=1,startcol=1,header=False,index=False)
        
        workbook = writer.book
        nc_sheet = writer.sheets[self.nc_file_name]
        ccb_sheet = writer.sheets[self.ccb_file_name]

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
        
        nc_rows,nc_cols = self.nc_ccb.shape
        for i in range(nc_rows+5):
            nc_sheet.set_row(i,22,cell_format)

        yes_index = self.nc_ccb[self.nc_ccb['对账一致']=='yes'].index+1
        for i in yes_index:
            nc_sheet.set_row(i,22,yes_format)

        # col format
        nc_sheet.set_column(0,nc_cols+5,22)

        nc_sheet.write_row('B1',self.nc_ccb.columns,header_format)
        nc_sheet.write_column('A2',self.nc_ccb.index,header_format)
        nc_sheet.freeze_panes(1,1)
        nc_sheet.set_tab_color('#FF9900')

        #ccb
        # row format
        ccb_rows,ccb_cols = self.ccb.shape
        for i in range(ccb_rows+5):
            ccb_sheet.set_row(i,22,cell_format)

        yes_index = self.ccb[self.ccb['对账一致']=='yes'].index+1
        for i in yes_index:
            ccb_sheet.set_row(i,22,yes_format)

        # col format
        ccb_sheet.set_column(0,ccb_cols+5,22)

        ccb_sheet.write_row('B1',self.ccb.columns,header_format)
        ccb_sheet.write_column('A2',self.ccb.index,header_format)
        ccb_sheet.freeze_panes(1,1)
        ccb_sheet.set_tab_color('#FF9900')

        writer.save()



    def doall(self):
        self.rec_mortgage()
        self.rec_pfund()
        self.rec_appointment_building()
        self.rec_reservefund()
        self.rec_bidbond()
        self.rec_group()
        self.rec_firmamount()
        self.rec_bankfee()

        self.pay_salary()
        self.pay_firmamount()
        self.pay_wechat()
        self.pay_landmargin()
        self.pay_group()
        self.prepay_firmamount()
        self.pay_refund()
        self.save_margin()
        self.pay_bankfee()
        self.pay_reimburse()
        self.pay_bidbond()
        self.return_loans()
        self.inner_transfer()

        self.export_excel()

    def __call__(self):
        return self.doall()
