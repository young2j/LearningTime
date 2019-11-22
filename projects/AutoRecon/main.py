#!/usr/bin/env python
# coding: utf-8

from reconciliationICBC import DealExcelICBC,CheckICBC
from reconciliationABC import DealExcelABC,CheckABC
from reconciliationBOC import DealExcelBOC,CheckBOC
from reconciliationCCB import DealExcelCCB,CheckCCB
from reconciliationCEB import DealExcelCEB,CheckCEB
from reconciliationPOS import CheckPOS
import os
import consolechars
# from cfonts import say

if __name__=='__main__':

    # say("LEADING ssc", font='simple', size=(150, 30), colors=['candy'], 
    #     background='transparent', align='center', letter_spacing=None, 
    #     line_height=20, space=True,max_length=0)

    consolechars.say("LEADING SSC")

    go_on = True

    while go_on:
        try:
            bank_name = input("请选择对账银行或其他功能(1.工行[icbc] 2.农行[abc] 3.中行[boc] 4.建行[ccb]) 5.光大[ceb] 6.POS)\n")

            nc_path = input("请输入NC/POS表路径:\n").strip(r'\'|\"')
            nc_file_name = os.path.basename(nc_path).split('.')[0]

            if bank_name.lower()!='pos' and bank_name!='6':
                bank_path = input("请输入银行表路径:\n").strip(r'\'|\"')
                bank_file_name = os.path.basename(bank_path).split('.')[0]

            if os.path.isdir(nc_path):
                save_path = nc_path
            elif os.path.isfile(nc_path) and os.path.dirname(nc_path)!='':
                save_path = os.path.dirname(nc_path)
            elif os.path.dirname(nc_path)=='':
                save_path = os.getcwd()
            
        
            if bank_name.lower()=="icbc" or bank_name=='1' or bank_name == "工行":
                deal_excel = DealExcelICBC(nc_path=nc_path,bank_path=bank_path)
                nc_icbc = deal_excel.dealNC()
                icbc = deal_excel.dealBANK()
            
                check_icbc = CheckICBC(nc_icbc,icbc,nc_file_name,bank_file_name,save_path)
                check_icbc.doall()
            
            elif bank_name.lower()=='abc' or bank_name=='2' or bank_name=='农行':
                deal_excel = DealExcelABC(nc_path=nc_path,bank_path=bank_path)
                nc_abc = deal_excel.dealNC()
                abc = deal_excel.dealBANK()
            
                check_abc = CheckABC(nc_abc,abc,nc_file_name,bank_file_name,save_path)
                check_abc.doall()
            
            elif bank_name.lower()=='boc' or bank_name=='3' or bank_name=='中行':
                deal_excel = DealExcelBOC(nc_path=nc_path,bank_path=bank_path)
                nc_boc = deal_excel.dealNC()
                boc = deal_excel.dealBANK()

                check_boc = CheckBOC(nc_boc,boc,nc_file_name,bank_file_name,save_path)
                check_boc.doall()
            
            elif bank_name.lower() == 'ccb' or bank_name=='4' or bank_name=='建行':
                deal_excel = DealExcelCCB(nc_path=nc_path,bank_path=bank_path)
                nc_ccb = deal_excel.dealNC()
                ccb = deal_excel.dealBANK()
            
                check_ccb = CheckCCB(nc_ccb,ccb,nc_file_name,bank_file_name,save_path)
                check_ccb.doall()

            elif bank_name.lower() == 'ceb' or bank_name=='5' or bank_name=='光大':
                deal_excel = DealExcelCEB(nc_path=nc_path,bank_path=bank_path)
                nc_ceb = deal_excel.dealNC()
                ceb = deal_excel.dealBANK()

                check_ceb = CheckCEB(nc_ceb,ceb,nc_file_name,bank_file_name,save_path)
                check_ceb.doall()
            
            elif bank_name.lower() == 'pos' or bank_name == '6':
                checkPOS = CheckPOS(pos_path=nc_path,pos_file_name=nc_file_name,save_path=save_path)
                checkPOS.doall()

            choice = True
            while choice:
                go = input("continue/exit: [enter/n] ? ")

                if go.strip()=='':
                    choice = False
                elif go.lower()=='n':
                    choice = False
                    go_on = False
                else:
                    pass
        except Exception as e:
            raise e
            # print("ERROR:",e)
            # time.sleep(60)
            os.system('pause')
