cd "C:\Users\Administrator\Desktop\论文复制-陆正飞\数据\审计委员会"
*委员会公告数据（1：成立 2：换届 3：调整）
forvalues i=0/2{
import excel using CG_Commit`i'.xls,clear
drop in 1/3
renvars _all/stkcd comname repttype year
replace year=substr(year,1,4)
destring stkcd repttype year,replace
keep if regexm(comname,"审计") //对比命令drop if indexnot("审计",comname)
gen commit1=repttype if repttype==1
replace commit1=2 if repttype!=1
save commit`i',replace
}
append using commit0 commit1
duplicates drop stkcd year,force
drop comname repttype
sort stkcd  year commit1
save audit1,replace

*委员会设立数量数据（四委=4：一定有审计委员会）
import delimited CG_commit3.csv,clear
renvars _all/stkcd year totcommit commit4 othcommit
labvars stkcd year totcommit commit4 othcommit ///
"证券代码" "截止日期" "委员会总数" "四委个数" "其他委员会" //批量加标签，需安装
replace year=substr(year,1,4)
destring year,replace
sort stkcd year 
gen commit2=1 if commit4==4
replace commit2=0 if commit4!=4
duplicates drop stkcd year,force
xtset stkcd year
by stkcd: replace commit2=1 if L.commit2==1 
drop totcommit commit4 othcommit
save audit2,replace

*利用两个数据集得出公司是否拥有审计委员会
merge 1:1 stkcd year using audit1,nogen
sort stkcd year
by stkcd: replace commit1=1 if L.commit1==1 //1代表成立，以后年度一定有
gen audcom=1 if commit2==1 
replace audcom=1 if commit1!=.
replace audcom=0 if audcom!=1
drop commit1 commit2
save audcom,replace
