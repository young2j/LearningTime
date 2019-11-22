cd "C:\Users\Administrator\Desktop\论文复制-陆正飞\数据\操纵性应计"

*整理操纵性应计方程所需数据
import excel using accruals.xls,clear // firstrow
drop in 1/3
renvars _all/stkcd year assets rec ppe rev tacrul
*同ren (_all) (stkcd year assets rec ppe rev tacrul)
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
save accruals,replace //得到Jones模型回归所需数据

*IPO当年
import excel using IPO.xls,clear
drop in 1/3
renvars _all/stkcd ipoyear 
replace ipoyear=substr(ipoyear,1,4)
destring stkcd ipoyear,replace
save IPO,replace

*整理行业分类
forvalues i=1/3{
import excel using F`i'.xls,clear
drop in 1/3
renvars _all/stkcd year ind
replace year=substr(year,1,4)
replace ind=substr(ind,1,2) //二级行业分类
destring stkcd year,replace
save ind`i',replace
}
append using ind1 ind2
sort stkcd year
duplicates drop stkcd year,force
save ind,replace

*数据合并计算操纵性应计DA
use accruals,clear
merge 1:1 stkcd year using ind,update nogen
merge m:1 stkcd using IPO,nogen //同joinby stkcd using IPO,unmatched(master)
drop if strmatch(ind,"J*")   //剔除金融业
drop if year==ipoyear  //剔除IPO当年
drop ipoyear
dropmiss,any obs force //剔除缺失值
winsor2 Y-X3,cuts(1 99) replace //1%水平缩尾处理

*（insufficient observations : cap [noisily]） 
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
save DA,replace






