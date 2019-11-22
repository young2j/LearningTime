#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import re

class CheckPOS(object):
    def __init__(self, pos_path,pos_file_name,save_path=None):
        self.pos_path = pos_path
        self.pos_file_name = pos_file_name
        self.save_path = save_path
        self.year = None

    def dealExcelPOS(self):
        # read
        nc_pos = pd.read_excel(self.pos_path, header=None)
        nc_pos = nc_pos.dropna(how='all')

        # deal year/head/tail
        year = nc_pos.iloc[0, 0]
        self.year = str(year)
        init_period = nc_pos.iloc[2, :]  # 暂时保存期初行
        month_year_sum = nc_pos.tail(2)  # 暂时保存本月及本年累计行

        # drop useless rows
        nc_pos.columns = nc_pos.iloc[1, :]
        nc_pos = nc_pos.drop([0, 1, 2])
        nc_pos = nc_pos.head(len(nc_pos)-2)

        time = str(year) + '-' + \
            nc_pos['月'].astype(str) + '-' + nc_pos['日'].astype(str)
        nc_pos.insert(0, '日期', pd.to_datetime(
            time, format='%Y-%m-%d').astype(str).str.slice(0, 10))

        nc_pos.reset_index(drop=True, inplace=True)

        # 提取交易时间
        time_pattern1 = re.compile(r'\d{4}-\d+-\d+')
        time_pattern2 = re.compile(r'\d{4}\.\d+\.\d+')
        time_pattern3 = re.compile(r'\d+\.\d+')

        transac_time = nc_pos['摘要'].copy()
        for i in range(len(transac_time)):
            time1 = time_pattern1.findall(transac_time[i])  # [2019-07-01]
            if time1 != []:
                transac_time[i] = time1[0]
            else:
                time2 = time_pattern2.findall(transac_time[i])  # [2019.8.2]
                if time2 != []:
                    transac_time[i] = time2[0]
                else:
                    time3 = time_pattern3.findall(transac_time[i])  # [8.2] #[2019.7]
                    try:
                        if len(str(time3[0]).split('.')[0]) == 4:
                            transac_time[i] = None
                        else:
                            transac_time[i] = str(year) + '.' + time3[0]
                    except IndexError:
                        transac_time[i] = None

        nc_pos.insert(0,'对齐',None)
        nc_pos.insert(6, '交易日期', transac_time)
        nc_pos['交易日期'] = pd.to_datetime(transac_time, format='%Y-%m-%d')

        # 转换字段类型
        nc_pos.columns = list(map(lambda x: str(x).strip(), nc_pos.columns))
        nc_pos.loc[:, ['借方', '贷方', '余额']] = nc_pos[['借方', '贷方', '余额']].apply(
            lambda s: s.astype(np.float64))

        nc_pos.drop(['月', '日'], axis=1, inplace=True)

        return nc_pos

    def checkPOS(self):
        nc_pos = self.dealExcelPOS()
        is_pos = nc_pos['摘要'].str.contains(r"POS到账|pos到账")
        cr_pos = nc_pos[is_pos] # pos到账
        dt_pos = nc_pos[is_pos==False] # 收

        dt_time = cr_pos['摘要'].str.findall(r"(\d{4})-(\d{4})") # [(0904, 0904)]
        for idx in dt_time.index:
            if dt_time[idx]!=[]:
                dt_time[idx] = self.year + dt_time[idx][0][0] + '-' + self.year + dt_time[idx][0][1]
            else:
                dt_time[idx] = '-'

        dt_time = dt_time.str.split('-',expand=True)
        dt_time.columns = ['time_start','time_end']
        dt_time = dt_time.apply(pd.to_datetime)
        cr_pos = pd.concat([cr_pos,dt_time],axis=1)

        c = 0
        for cr_idx in cr_pos.index:
            if str(cr_pos.loc[cr_idx,'time_start'])=='NaT':
                delta = 1
                while delta<5:
                    time_delta = (cr_pos.loc[cr_idx, '交易日期']-dt_pos['交易日期']).apply(lambda d: d.days)
                    # print('time_delta：',time_delta)
                    time_cond = ((time_delta >= 1) & (time_delta <= delta))
                    dt_pos_part = dt_pos[time_cond]
                    if np.around(dt_pos_part['借方'].sum(), 2) == np.around(cr_pos.loc[cr_idx, '贷方'], 2):
                        idxs = [cr_idx]+dt_pos_part.index.tolist()
                        nc_pos.loc[idxs, '对齐'] = c
                        c += 1
                    delta+=1
            else:
                time_cond1 = dt_pos['交易日期']>= cr_pos.loc[cr_idx,'time_start']
                time_cond2 = dt_pos['交易日期']<= cr_pos.loc[cr_idx,'time_end']
                dt_pos_part = dt_pos[(time_cond1&time_cond2)]
                
                if np.around(dt_pos_part['借方'].sum(), 2) == np.around(cr_pos.loc[cr_idx, '贷方'], 2):
                    idxs = [cr_idx]+dt_pos_part.index.tolist()
                    nc_pos.loc[idxs, '对齐'] = c
                    c += 1

        return nc_pos

    def export_excel(self):
        nc_pos = self.checkPOS()
        total_rows = nc_pos['对齐'].shape[0]
        yes_rows = (nc_pos['对齐'].notnull() * 1).sum()

        print('\n')
        print("+--------------------------------------------------+")
        print("¦                  RESULTS                         ¦")
        print("+--------------------------------------------------+")
        print("¦    TOTAL     ¦    MATCH_ROWS    ¦    NOT_MATCH   ¦")
        print("+--------------------------------------------------+")
        print("¦{0:^14}¦{1:^18}¦{2:^16}¦".format(total_rows,yes_rows,total_rows-yes_rows))
        print("+--------------------------------------------------+")
        print('\n')

        nc_pos['交易日期'] = nc_pos['交易日期'].astype(str).str.slice(0, 10)

        save_file = self.save_path + '\\' + self.pos_file_name + '_check' + '.xlsx'
        print("结果保存至:\n\t%s\n" % (save_file))

        writer = pd.ExcelWriter(save_file, engine='xlsxwriter')
        nc_pos.to_excel(writer, sheet_name=self.pos_file_name,
                             startrow=1, header=False, index=False)

        workbook = writer.book
        pos_sheet = writer.sheets[self.pos_file_name]

        header_format = workbook.add_format({
            "bold": True,
            "bg_color": '#67d8ef',
                        'font_size': 12,
                        'font_name': "微软雅黑",
                        "align": 'center',
                        'border': 2,
        })

        cell_format = workbook.add_format({
            "font_size": 10,
            "font_name": "微软雅黑",
            "border": 1,
            "border_color": '#67d8ef',
            "align": "left",
        })

    
        def gen_yes_format(number):
            color_list = ['#FFB5B5', '#FF60AF',  '#CA8EFF', '#F9F900', '#AAAAFF', '#D2E9FF',
                          '#80FFFF', '#7AFEC6', '#00DB00', '#FFD306', '#F75000', 
                          '#5CADAD', '#8080C0', '#AE57A4', '#ffff00', '#FF8EFF',
                          '#FF79BC', '#FF77FF', '#BE77FF', '#5E005E', '#3A006F'
                          '#C48888', '#B9B973', '#81C0C0', '#A6A6D2', '#C07AB8', 
                          '#EFFFD7', '#FFFFDF', '#FFF8D7', '#FFEEDD', '#ECECFF', 
                          '#64A600', '#737300', '#977C00', '#BB5E00', '#A23400'] * 5

            format_dict = {
                "bg_color": color_list[number],
                "font_size": 10,
                "font_name": "微软雅黑",
                "border": 1,
                "border_color": '#67d8ef',
                "align": "left"
            }
            
            yes_format = workbook.add_format(format_dict)

            return yes_format
 

        nc_rows, nc_cols = nc_pos.shape
        # row format
        for i in range(nc_rows+5):
            pos_sheet.set_row(i, 20, cell_format)

        for num in nc_pos['对齐'].unique():
            if num is not np.nan:
                yes_index = nc_pos[nc_pos['对齐'] == num].index+1
                for i in yes_index:
                    pos_sheet.set_row(i, 20, gen_yes_format(int(num)))

        # col format
        pos_sheet.set_column(0, nc_cols+5, 15)

        pos_sheet.write_row('A1', nc_pos.columns, header_format)
        pos_sheet.freeze_panes(1, 0)
        pos_sheet.set_tab_color('#FF9900')

        writer.save()

    def doall(self):
        self.export_excel()
