cd C:\Users\Administrator\Desktop\论文复制-陆正飞\数据\X

*整理董事有关的数据变量
import excel using d.xlsx,clear
drop in 1/3
save X,replace 

forvalues i=1(1)6{
import excel using CG_Director`i'.xlsx,clear
drop in 1/3
append using X
save X,replace 
}
renvars _all/stkcd year name ten  po sex
format name po %30s
keep if substr(ten,1,1)=="1"   //职务编码第一位1：代表董事会成员
replace year=substr(year,1,4)
save X,replace 

*整理出公司每年各类董事总数
use X,clear
sort stkcd year ten
bysort stkcd year:gen board=_N  //生成公司每年董事总人数（董事会规模）
gen exe=1 if substr(ten,3,4)!="0000"  //根据编码生成执行董事
gen outer=1 if substr(ten,3,4)=="0000" //根据编码生成外部董事
bysort stkcd year:egen EXE=sum(exe) //生成公司每年执行董事总数
bysort stkcd year:egen OUTER=sum(outer) //生成公司每年外部董事总数
gen inde=1 if substr(ten,1,2)=="14" & po=="独立董事" //根据编码与名称判断独董
replace inde=1 if substr(ten,1,2)=="12"  //编码前两位12：代表独立董事
bysort stkcd year:egen INDE=sum(inde) //生成公司每年独董总数
gen NONEXE=OUTER-INDE //生成公司每年执行董事总数

*计算公司每年各类董事比例
replace NONEXE=NONEXE/board
replace EXE=EXE/board
replace INDE=INDE/board
replace OUTER=OUTER/board

*整理出最终董事变量数据
keep stkcd year board NONEXE EXE INDE OUTER
destring _all,replace 
sort stkcd year 
duplicates drop
save X,replace 




