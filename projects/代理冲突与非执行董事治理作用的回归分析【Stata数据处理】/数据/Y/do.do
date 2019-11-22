cd C:\Users\Administrator\Desktop\论文复制-陆正飞\数据\Y

*处理净利润数据
import delimited FS_Comins.csv,clear  //csv 与excel 导入语言不一样
renvars _all /stkcd year c ni
keep if c=="A"  //保留合并报表数据（A）
keep if substr(year,6,2)=="12"
replace year=substr(year,1,4)
destring year,replace 
drop c
sort stkcd year 

*合并DA以计算PDA
merge 1:1 stkcd year using DA,nogen
gen PDA=ni-DA
sort stkcd year 

*计算DA和PDA的变化值
xtset stkcd year 
gen d_PDA=PDA-L.PDA
gen d_DA=DA-L.DA
save p,replace 

*采用当年及前3年数据计算变化值的相关系数
forvalues i=2003(1)2012{
use p,clear 
gen j=year-`i' //生成年度差值
keep if j>0 & j<4 //保留差值为1/2/3的年份
replace year=`i'+3 
save p`i',replace 
}

*经上步循环当前数据为p2012，再合并
forvalues i=2003(1)2011{
append using p`i'
sort stkcd year
save P_all,replace 
}

*计算相关系数es
statsby r(rho),by(stkcd year) nodots:corr d_PDA d_DA //分组生成统计量,nodots省去过程
rename _stat_1 es
save es,replace 

use p,clear
drop if year<2006
merge 1:1 stkcd year using es,nogen update
keep stkcd year ind es
save ES,replace 
