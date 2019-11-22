cd C:\Users\Administrator\Desktop\论文复制-陆正飞\数据\control

*处理公司规模size
import delimited using size.csv,clear
keep if substr(accper,6,2)=="12"
renvars _all/stkcd year size
replace year=substr(year,1,4)
destring _all,replace 
replace size=ln(1+size) //为什么是ln(1+size)
sort stkcd year
save control,replace 

*处理公司资产负债率lev
import delimited using  lev.csv,clear
keep if substr(accper,6,2)=="12"
renvars _all/stkcd year lev
replace year=substr(year,1,4)
destring _all,replace 
sort stkcd year 
merge 1:1 stkcd year using control,nogen //nogen不生成_merge变量
sort stkcd year 
save control,replace 

*处理资产收益率roa
import delimited using roa.csv,clear
keep if substr(accper,6,2)=="12"
renvars _all/stkcd year roa
replace year=substr(year,1,4)
destring _all,replace 
sort stkcd year 
merge 1:1 stkcd year using control,nogen 
sort stkcd year 
save control,replace 

*处理股权制衡度Z和股权集中度H
import excel using hold.xls,clear
renvars _all/stkcd year H Z S H2
drop in 1/3
keep if substr(year,6,2)=="12"
replace year=substr(year,1,4)
destring _all,replace 
replace Z=1/Z
replace S=S/H
sort stkcd year 
merge 1:1 stkcd year using control,nogen
sort stkcd year 
merge 1:1 stkcd year using soe,nogen
save control,replace 



