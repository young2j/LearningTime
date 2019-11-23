*控制变量的初步处理
set more off
cd "C:\Users\Administrator\Desktop\2161202Z6024杨双杰\control"
import delimited balance.csv,clear 
renvars _all/ stkcd year typrept recei inv fasset fadisposal iasset assets
labvars _all "证券代码" "年度" "报表类型" "应收账款" "存货" ///
             "固定资产" "固定资产清理" "无形资产" "资产总额"
keep if typrept=="A"
drop typrept fasset fadisposal iasset
keep if substr(year,6,2)=="12"
replace year=substr(year,1,4)
destring year,replace
save balance,replace

import delimited grevenue.csv,clear 
renvars _all/ stkcd year typrept ind grev susgrate
labvars _all "证券代码" "年度" "报表类型" "行业" "营业收入增长率" "可持续增长率" 
keep if typrept=="A"
drop typrept
keep if substr(year,6,2)=="12"
replace year=substr(year,1,4)
destring year,replace
save growth,replace

import delimited LEV.csv,clear
renvars _all/ stkcd year typrept ind lev
labvars _all "证券代码" "年度" "报表类型" "行业" "资产负债率" 
keep if typrept=="A"
drop typrept
keep if substr(year,6,2)=="12"
replace year=substr(year,1,4)
destring year,replace
save lev,replace

import delimited depamor.csv,clear
renvars _all/ stkcd year typrept ind depamor
labvars _all "证券代码" "年度" "报表类型" "行业" "折旧与摊销" 
keep if typrept=="A"
drop typrept
keep if substr(year,6,2)=="12"
replace year=substr(year,1,4)
destring year,replace
save depamor,replace

import delimited NI.csv,clear
renvars _all/ stkcd year typrept ni
labvars _all "证券代码" "年度" "报表类型" "净利润"  
keep if typrept=="A"
drop typrept
keep if substr(year,6,2)=="12"
replace year=substr(year,1,4)
destring year,replace
save ni,replace

import delimited ROAE.csv,clear
renvars _all/ stkcd year typrept ind roa roe roic
labvars _all "证券代码" "年度" "报表类型" "行业" ///
              "总资产净利润率" "净资产报酬率" "投入资本回报率" 
keep if typrept=="A"
drop typrept
keep if substr(year,6,2)=="12"
replace year=substr(year,1,4)
destring year,replace
save roaec,replace

import delimited roegrate.csv,clear
renvars _all/ stkcd year typrept ind roegrate
labvars _all "证券代码" "年度" "报表类型" "行业" "净资产增长率" 
keep if typrept=="A"
drop typrept
keep if substr(year,6,2)=="12"
replace year=substr(year,1,4)
destring year,replace
save roegrate,replace

import delimited PEratio.csv,clear
renvars _all/ stkcd year ind peratio
labvars _all "证券代码" "年度" "行业" "市盈率" 
keep if substr(year,6,2)=="12"
replace year=substr(year,1,4)
destring year,replace
save peratio,replace

import excel using saction.xlsx,clear firstrow
labvars _all "年度" "行政处罚" "行业惩戒"  
save sanction,replace

import excel using 境内公司基本信息—公司性质—DIB.xlsx,clear 
keep A D E 
format A %10s  
format E %-45s
drop in 1
ren (A D E) (stkcd type controller)
replace stkcd=substr(stkcd,1,6)
gen soe=1 if type=="国有企业"  
replace soe=1 if type=="其他" & regexm(controller,"国有资产监督管理")
replace soe=0 if soe==.
destring stkcd,replace
drop type controller
duplicates drop stkcd soe,force 
save soe1,replace

import excel using 上市公司实际控制人.xlsx,clear
keep A  D
drop in 1
renvars _all/stkcd contrtype
replace stkcd=substr(stkcd,1,6)
gen soe=1 if regexm(contrtype,"国资委")|regexm(contrtype,"政府")  ///
             |regexm(contrtype,"国有企业")|regexm(contrtype,"中央") 
replace soe=0 if soe==.
destring stkcd,replace
drop contrtype
duplicates drop stkcd soe,force
save soe2,replace

merge 1:1 stkcd soe using soe1,nogen
sort stkcd
duplicates drop stkcd,force
save soe,replace

*合并各数据并计算控制变量
mergemany 1:1 balance depamor growth lev ni roaec roegrate peratio,match(stkcd year)
gen lnassets=ln(assets) //企业规模
gen loss=1 if ni>0 //盈亏状况
replace loss=0 if ni<0
gen ndts=depamor/assets //非债务税盾
gen complex=(inv+recei)/assets //审计复杂程度
drop recei inv assets depamor ni 
merge m:1 stkcd using soe,update nogen
merge m:1 year using sanction,nogen
sort stkcd year
save control,replace

*处理ST和IPO的数据
import delimited ST.csv,clear
renvars _all/ stkcd year typrept
labvars _all "证券代码" "ST年度" "报表类型"  
keep if typrept=="A"
drop typrept
keep if substr(year,6,2)=="12"
replace year=substr(year,1,4)
destring year,replace
gen st=1
save st,replace

import delimited IPO.csv,clear
renvars _all/stkcd initial ipoyear listyear
keep if initial=="A"
drop initial
replace ipoyear=substr(ipoyear,1,4)
replace listyear=substr(listyear,1,4)
destring ipoyear listyear,replace
labvars _all "年度" "IPO当年" "上市当年"
duplicates drop stkcd,force
save ipo,replace

*处理解释变量
cd "C:\Users\Administrator\Desktop\2161202Z6024杨双杰\XY"
import excel using GDP.xls,clear
drop C
drop in 1/7
renvars _all/year gdpindex 
replace year=substr(year,-4,4)
destring year gdpindex,replace 
gen gdpgrate=(gdpindex-100)/100
gen downturn=1 if gdpgrate<gdpgrate[_n-1]
replace downturn=0 if downturn==.
labvars _all "年度" "GDP指数（上年100）" "GDP增长率" "经济周期"
save X,replace

*备用数据1
import delimited CME_Pindex10.csv,clear
renvars _all/year warnindex agreeindex leadindex lagindex
labvars _all "年度" "预警指数" "一致指数" "先行指数" "滞后指数"
gen recession=1 if agreeindex<100
replace recession=0 if agreeindex>100
save macindex,replace

*备用数据2
import delimited CME_Qbcid1.csv,clear
ren (_all) (yearq q bcindex)
drop q
gen year=substr(yearq,1,4)
labvars _all "年季" "企业景气指数" "年度"
destring year yearq,replace ignore("-")
save bcindex,replace

*处理因变量
import excel using FIN_Audit.xls,clear firstrow case(lower)
drop in 1/2
keep stkcd accper audittyp auditor dadtunit tcost
renvars accper audittyp dadtunit tcost/year opin firm fee
labvars _all "证券代码" "年度" "审计意见" "审计师" "境内事务所" "审计费用"
format firm %-45s 
keep if substr(year,6,2)=="12"
replace year=substr(year,1,4)
destring stkcd year fee,replace
gen lnfee=ln(fee),after(year)
drop fee

*审计意见虚拟变量
gen opinion=0 if opin=="标准无保留意见"
replace opinion=1 if opinion==.

*筛选公司各年事务所是否为“十大”
loc c2003 普华永道 毕马威 德勤 安永华明 上海立信 岳华 中瑞华恒信 北京京都 信永中和 中审
loc c2004 普华永道 毕马威 德勤 安永华明 上海立信 岳华 信永中和 中审 中瑞华恒信 江苏公证
loc c2005 普华永道 毕马威 德勤 安永华明 上海立信 信永中和 中审 岳华 中瑞华恒信 北京京都
loc c2006 普华永道 安永华明 德勤 毕马威 上海立信 岳华 信永中和 万隆 中审 中瑞华恒信
loc c2007 普华永道 安永华明 德勤 毕马威 立信 岳华 信永中和 中审 中瑞华恒信 万隆
loc c2008 普华永道 安永华明 德勤 毕马威 中瑞岳华 立信 信永中和 大信 万隆 利安达
loc c2009 普华永道 安永华明 德勤 毕马威 中瑞岳华 立信 万隆亚洲 天健 大信 信永中和
loc c2010 普华永道 德勤 毕马威 安永华明 中瑞岳华 立信 信永中和 天健 国富浩华 大信
loc c2011 普华永道 德勤 安永华明 毕马威 中瑞岳华 立信 国富浩华 天健 信永中和 大信
loc c2012 普华永道 德勤 安永华明 毕马威 立信 中瑞岳华 天健 信永中和 国富浩华 大华
loc c2013 普华永道 德勤 瑞华 安永华明 立信 毕马威 大信 天健 信永中和 大华
loc c2014 普华永道 德勤 瑞华 立信 安永华明 毕马威 天健 大华 信永中和 大信
loc c2015 普华永道 德勤 安永华明 瑞华 立信 毕马威 天健 信永中和 天职国际 大华
loc c2016 普华永道 瑞华 德勤 立信 安永华明 毕马威 天健 信永中和 天职国际 大华
gen big10=.
forvalues i=2003/2016 {
foreach x of loc c`i'{
replace big10=1 if year==`i' & regexm(firm,"`x'")
}
}
replace big10=0 if big10==.

drop opin firm
order opinion big10,before(auditor)	
sort stkcd year
duplicates drop stkcd year,force
save Y,replace

*计算操纵性应计
import delimited MNMAPR_Accruals.csv,clear 
renvars _all/stkcd year assets rec ppe rev tacrul
labvars stkcd year assets rec ppe rev tacrul "证券代码" "会计年度" ///
     "资产总额" "应收账款" "固定资产原值" "营业收入" "总应计利润"
replace year=substr(year,1,4)
destring _all,replace
bysort stkcd:gen lassets=assets[_n-1]
bysort stkcd:gen delta_rev=rev-rev[_n-1]
bysort stkcd:gen delta_rec=rec-rec[_n-1]
gen Y=tacrul/lassets
gen X1=1/lassets
gen X2=(delta_rev-delta_rec)/lassets
gen X3=ppe/lassets
drop assets-delta_rec
merge 1:1 stkcd year using ind,nogen
keep if inrange(year,2003,2016) //样本区间为2003-2016
drop if ind=="J" //剔除金融业
drop if inrange(stkcd,200000,300000)|stkcd>900000 //剔除B股 
dropmiss,any obs force
sort stkcd year
save accruals,replace //得到Jones模型回归所需数据

winsor2 Y-X3,cuts(1 99) replace 
egen g=group(year ind) 
qui su g 
loc n=r(max) 
gen DA=. 
forvalues i=1/`n'{
qui cap reg Y X1 X2 X3 if g==`i',noc
qui predict r if e(sample),resid
qui replace DA=r if e(sample)
drop r
} 
drop g Y X1 X2 X3 
replace DA=abs(DA)
save DA,replace

merge 1:1 stkcd year using Y,nogen
save Y,replace



cd "C:\Users\Administrator\Desktop\2161202Z6024杨双杰\合并"
mergemany 1:1 Y control st,match(stkcd year)
merge 1:1 stkcd year using ind,update nogen
merge m:1 year using X,nogen
merge m:1 stkcd using ipo,nogen
replace ind=substr(ind,1,2)
drop if st==1 //剔除st公司
drop if year==ipoyear //剔除IPO当年
drop if ind=="J" //剔除金融业
drop if inrange(stkcd,200000,300000)|stkcd>900000 //剔除B股 
drop if lev>=1 //剔除资产负债率大于1的样本
sort stkcd year
drop ipoyear listyear gdpindex gdpgrate st
order stkcd year ind big10 opinion downturn  lnfee DA  grev lev  ///
      roa peratio lnassets ndts complex  saction  loss soe
labvars big10 DA opinion lnfee lnassets loss ndts complex soe ///
       "是否十大"  "|操纵性应计|"  "审计意见" "对数审计费用" "企业规模" ///
       "盈亏状况" "非债务税盾" "审计复杂度" "企业性质"
dropmiss stkcd-saction, any obs force
winsor2 lnfee-complex susgrate-roegrate,cuts(1 99) replace
save finaldata,replace
global c gre-loss

*描述性统计
logout,save(result1) word replace: ///
tabstat big10-soe,s(n mean median sd min max) col(s) format(%6.0g)

*pearson相关系数
logout,save(result2) word replace:pwcorr_a downturn big10 DA lnfee opinion $c

*不同经济周期周期下审计质量的差异（T检验）
logout,save(result3) excel replace: ///
ttab big10 DA lnfee opinion,by(downturn) title("big10" "DA" "lnfee" "opinion") ///
     estout(c(b(fmt(4) label("mean") star))) 

*回归分析
*第一步 混合回归vs固定效应回归
xtset stkcd year
xtreg big10 downturn $c ,fe
est store m1
xtreg DA downturn $c ,fe
est store m2
xtreg lnfee downturn $c ,fe
est store m3
xtreg opinion downturn $c ,fe
est store m4
esttab m1 m2 m3 m4,ar2 title("经济周期对审计质量的影响")  ///
	   star(* 0.1 ** 0.05 *** 0.01) nogaps compress 
//根据fe回归的F检验结果应使用固定效应回归模型	

*第二步  固定效应vs随机效应——hausman检验
xtset stkcd year
xtreg big10 downturn $c ,re
est store m5
xtreg DA downturn $c ,re
est store m6
xtreg lnfee downturn $c ,re
est store m7
xtreg opinion downturn $c ,re
est store m8
esttab m5 m6 m7 m8,ar2 title("经济周期对审计质量的影响")  ///
	   star(* 0.1 ** 0.05 *** 0.01) nogaps compress 

hausman m1 m5,sigmamore
hausman m2 m6,sigmamore
hausman m3 m7,sigmamore
hausman m4 m8,sigmamore	
//hausman 检验均强烈拒绝随机效应模型

*最终选择固定效应回归模型,并控制时间和行业效应,样本区间为2004-2016年
xtset stkcd year
xi:xtlogit big10 downturn $c i.ind i.year if year>=2004,fe nolog
est store m9
xi:logit big10 downturn $c i.ind i.year if year>=2004,r
est store m10
xi:xtreg DA downturn  $c i.ind i.year if year>=2004,fe r
est store m11
esttab m9 m10 m11 using result4.doc,replace ar2 scalar(r2_p) ///
       title("经济周期对审计质量的影响")  ///
	   mtitle("big10(面板)" "big10(混合)" "DA") ///
	   star(* 0.1 ** 0.05 *** 0.01) drop(_I*) nogaps 
	   
*按企业性质分组回归
xi:xtlogit big10 downturn $c i.ind i.year if year>=2004 & soe==1,fe nolog
est store m12
xi:xtlogit big10 downturn $c i.ind i.year if year>=2004 & soe==0,fe nolog
est store m13
xi:logit big10 downturn $c i.ind i.year if year>=2004 & soe==1,r
est store m14
xi:logit big10 downturn $c i.ind i.year if year>=2004 & soe==0,r
est store m15
xi:xtreg DA downturn  $c i.ind i.year if year>=2004 & soe==1,fe r
est store m16
xi:xtreg DA downturn  $c i.ind i.year if year>=2004 & soe==0,fe r
est store m17
loc m m12 m13 m14 m15 m16 m17
esttab `m' using result5.doc,replace ar2 scalar(r2_p)  drop(_I*) ///
       title("不同企业性质下经济周期对审计质量的影响") nogaps ///
	   mtitle("big10(面板soe=1)" "big10(面板soe=0)" "big10(混合soe=1)" ///
	   "混合soe=0" "DA soe=1" "DA soe=0") star(* 0.1 ** 0.05 *** 0.01) 
	  

*敏感性分析-分年度区间回归
xi:xtlogit big10 downturn $c i.ind i.year if year>=2006,fe nolog
est store m18
xi:logit big10 downturn $c i.ind i.year if year>=2006,r
est store m19
xi:xtreg DA downturn  $c i.ind i.year if year>=2006,fe r
est store m20
esttab m18 m19 m20 using result6.doc,replace ar2 scalar(r2_p) ///
       title("2006-2016年经济周期对审计质量的影响")  ///
	   mtitle("big10(面板)" "big10(混合)" "DA") ///
	   star(* 0.1 ** 0.05 *** 0.01) drop(_I*) nogaps 

xi:xtlogit big10 downturn $c i.ind i.year if year>=2009,fe nolog
est store m21
xi:logit big10 downturn $c i.ind i.year if year>=2009,r
est store m22
xi:xtreg DA downturn  $c i.ind i.year if year>=2009,fe r
est store m23
esttab m21 m22 m23 using result7.doc,replace ar2 scalar(r2_p) ///
       title("2009-2016年经济周期对审计质量的影响")  ///
	   mtitle("big10(面板)" "big10(混合)" "DA") ///
	   star(* 0.1 ** 0.05 *** 0.01) drop(_I*) nogaps	
	   
*稳健性分析	   
xi:xtreg lnfee downturn  $c i.ind i.year,fe r
est store m24
xi:xtlogit opinion downturn $c i.ind i.year,fe nolog
est store m25
xi:logit opinion downturn $c i.ind i.year,r
est store m26
esttab m24 m25 m26 using result8.doc,replace ar2 scalar(r2_p) ///
       title("经济周期对审计质量的影响")  ///
	   mtitle("lnfee" "opinion(面板)" "opinion(混合)" ) ///
	   star(* 0.1 ** 0.05 *** 0.01) drop(_I*) nogaps    

*作经济周期波动图
cd "C:\Users\Administrator\Desktop\2161202Z6024杨双杰\合并"
use X,clear
keep if year>=2004
replace gdpgrate=gdpgrate*100
format gdpgrate %4.1f
sc gdpgrate year,c(l) xlabel(2004(1)2016) ylabel(,angle(0)) ///
   xtitle(" ") ytitle("GDP增长率%（上年=100）") mlabel("gdpgrate") ///
   subtitle("图1 GDP各年增长率变化趋势图",pos(6)) graphregion(color(white))
