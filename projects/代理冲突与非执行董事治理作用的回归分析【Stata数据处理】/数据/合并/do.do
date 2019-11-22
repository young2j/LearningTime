cd C:\Users\Administrator\Desktop\论文复制-陆正飞\数据\合并

mergemany 1:1 ES X control audcom,match(stkcd year) //需要安装，多个数据文件合并
drop if strmatch(ind,"J*")  //行业J为金融业（之前已剔除）
dropmiss, any obs force //需要安装，删除缺失值的命令
drop if year>2012
drop if stkcd>200000 & stkcd<300000 //以下两条命令可不用，都是A股
drop if stkcd>900000	//200、900开头的是B股
sort stkcd year 

*处理ES（分位数赋值）
replace es=-es //取相反数
sort es //从小到大排列
gen ES=_n  //9801个观测，与文章（9172）差异很小
replace ES=ES/9801  //按百分比排列了


*处理两个dummy
qui su Z,de
gen Z_d=1 if Z>r(p50)
replace Z_d=0 if Z_d==.

qui su S,de
gen S_d=1 if S>r(p50)
replace S_d=0 if S_d==.

sort stkcd year
winsor2 board-S_d,cuts(1 99) replace //需要安装，缩尾命令
global c audcom size lev roa H  H2  soe
save finaldata,replace

*数据整理完毕
*以下为各种结果表和图

*描述性统计(表2)
logout,save(result1) text replace: ///
tabstat ES board-NONEXE $c Z S Z_d S_d, ///
s(n mean median sd min p5 p95 max) col(s) format(%6.0g)

*董事构成的相关系数（表3）
logout,save(result2) text replace : ///
pwcorr_a NONEXE INDE EXE board //网上下载，相关系数自动打星

*不同股权制衡下均值t检验（表4）
logout,save(result3_1) text replace: ///
ttab NONEXE,by(Z_d S_d) title("NONEXE")  ///
     estout(c(b(fmt(4) label("mean") star))) 
	 
logout,save(result3_2) text replace: ///	 
ttab INDE,by(Z_d S_d) title("INDE")  ///
     estout(c(b(fmt(4) label("mean") star)))
	 
logout,save(result3_3) text replace: ///	 
ttab EXE,by(Z_d S_d) title("EXE")  ///
     estout(c(b(fmt(4) label("mean") star)))

*以下命令结果不好看
*ttest NONEXE,by(Z_d)
*ttest NONEXE,by(S_d)
*ttest INDE,by(Z_d)
*ttest INDE,by(S_d)
*ttest EXE,by(Z_d)
*ttest EXE,by(S_d)

*NONEXE对公司盈余平滑度（ES）的影响（表5）
xi:qui reg ES  $c NONEXE i.year i.ind  //xi：指生成虚拟变量回归
est store m1
xi:qui reg ES  $c OUTER i.year i.ind
est store m2
xi:qui reg ES  $c NONEXE INDE i.year i.ind
est store m3
esttab m1 m2 m3 using result4.doc,ar2 drop(_I*) ///
       order(_cons NONEXE OUTER INDE) ///
       title("NONEXE对公司盈余平滑度（ES）的影响")  ///
	   star(* 0.1 ** 0.05 *** 0.01) nogaps compress 

*不同股权制衡度对NONEXE治理作用的影响（表6）
gen NONEXExZ=NONEXE*Z
gen NONEXExS=NONEXE*S
xi:qui reg ES  $c NONEXE Z INDE i.year i.ind  
est store m4
xi:qui reg ES  $c NONEXE Z NONEXExZ INDE i.year i.ind
est store m5
xi:qui reg ES  $c NONEXE S INDE i.year i.ind
est store m6
xi:qui reg ES  $c NONEXE S NONEXExS INDE i.year i.ind
est store m7
esttab m4 m5 m6 m7 using result5.doc,ar2 drop(_I*) ///
       order(_cons NONEXE NONEXExZ Z NONEXExS S INDE) ///
       title("不同股权制衡度对NONEXE治理作用的影响")  ///
	   star(* 0.1 ** 0.05 *** 0.01) nogaps compress 

*不同股权性质下NONEXE对公司盈余平滑度的影响（表7）
xi:qui reg ES $c NONEXE INDE i.year i.ind if soe==1
est store m8
xi:qui reg ES $c NONEXE INDE i.year i.ind if soe==0
est store m9
esttab m8 m9 using result6.doc,ar2 drop(_I* soe) ///
       order(_cons NONEXE INDE $c) star(* 0.1 ** 0.05 *** 0.01) ///
       title("不同股权性质下NONEXE对公司盈余平滑度的影响") ///
	   mtitle("ES(soe=1)" "ES(soe=0)") nogaps compress  ///
	

*非执行董事对盈余平滑影响的两阶段回归（表8）
xi:qui reg NONEXE board Z INDE $c i.year i.ind
est store m10
predict NONEXE_hat
xi:qui reg ES $c NONEXE_hat INDE i.year i.ind
est store m11
esttab m10 m11 using result7.doc,ar2 drop(_I*) ///
       order(_cons Z board NONEXE NONEXE_hat INDE $c) ///
       title("内生性检验") star(* 0.1 ** 0.05 *** 0.01) ///
	   mtitle("NONEXE" "ES") nogaps compress 
	   
	   
*作各种图
use X.dta,clear
merge 1:1 stkcd year using ind,nogen
merge m:1 stkcd using IPO,nogen
drop if strmatch(ind,"J*")  
drop if missing(board-NONEXE)
sort stkcd year
save graphdata,replace

drop if missing(ipoyear)
xtset stkcd year
bys stkcd (year): replace ipoyear=L.ipoyear+1 if year!=ipoyear //IPO不一致的成为缺失
drop if missing(ipoyear)
save ipograph,replace
collapse (mean) NONEXE INDE EXE,by(ipoyear)

*图1 上市公司IPO之后10年间董事比例变化
twoway (line NONEXE ipoyear,lwidth(0.8)) ///
       (line INDE ipoyear,lpattern(shortdash)lwidth(0.8)) ///
       (line EXE ipoyear,lpattern(longdash) lwidth(0.8)), ///
	   xlabel(2006 "IPO" 2007 "1" 2008 "2" 2009 "3" 2010 "4" ///
	          2011 "5" 2012 "6" 2013 "7" 2014 "8" 2015 "9",noticks) ///
	   ylabel(#10,grid gmin gmax  glcolor(black) angle(0) format(%4.2f) noticks) ///
	   xtitle(" ") ytitle("人数比例")  yscale(titlegap(6)) ///
	   title("图1 上市公司IPO之后10年间董事比例变化",pos(6)) ///
	   legend(label(1 "NONEXE") label(2 "INDE") label(3 "EXE") pos(3) col(1) ///
	          region(lpattern(blank))) graphregion(color(white))

		
use ipograph,clear
gen NONEXE_n=NONEXE*board
gen INDE_n=INDE*board
gen EXE_n=EXE*board
collapse (mean) NONEXE_n INDE_n EXE_n board,by(ipoyear)
gen board_3=board/3 

*图2 上市公司IPO之后10年间董事会规模和三部分董事人数变化
twoway (connect board_3 ipoyear,msymbol(D) lwidth(0.8)) ///
       (line NONEXE ipoyear,lwidth(0.8)) ///
       (line INDE ipoyear,lpattern(shortdash)lwidth(0.8)) ///
       (line EXE ipoyear,lpattern(longdash) lwidth(0.8)), ///
	   xlabel(2006 "IPO" 2007 "1" 2008 "2" 2009 "3" 2010 "4" ///
	          2011 "5" 2012 "6" 2013 "7" 2014 "8" 2015 "9",noticks) ///
	   yscale(titlegap(6) outergap(8))  ///
	   ylabel(#12,grid nogmin gmax glcolor(black) angle(0)  noticks) ///
	   xtitle(" ") ytitle("人数")  ///
	   subtitle("图2 上市公司IPO之后10年间董事会规模" "和三部分董事人数变化",pos(6)) ///
	   legend(label(1 "board/3") label(2 "NONEXE")  ///
	          label(3 "INDE") label(4 "EXE") pos(3) col(1) ///
			  region(lpattern(blank))) graphregion(color(white))
			  

 
use graphdata,clear
drop ind ipoyear
sum NONEXE
gen g_NONEXE=autocode(NONEXE,10,r(min),r(max))
egen g1=group(g_NONEXE) 
collapse (mean) NONEXE INDE EXE,by(g1)

*图3 按照NONEXE大小分组董事会成员比例分析
twoway (line NONEXE g1,lwidth(0.8)) ///
       (line INDE g1,lpattern(shortdash)lwidth(0.8)) ///
       (line EXE g1,lpattern(longdash) lwidth(0.8)), ///
	   xlabel(1 "min" 2 3 4 5 6 7 8 9 10 "max",noticks) ///
	   ylabel(#5,grid nogmin gmax glcolor(black) angle(0) format(%4.1f) noticks) ///
	   xtitle(" ") ytitle(" ")  ///
	   subtitle("图3 按照NONEXE大小分组董事会成员比例分析",pos(6))  ///
       legend(label(1 "NONEXE") label(2 "INDE") label(3 "EXE") ///
	          pos(3) col(1) region(lpattern(blank))) graphregion(color(white))
		
use graphdata,clear
drop ind ipoyear
sum board
gen g_board=autocode(board,5,r(min),r(max))
egen g2=group(g_board) 
collapse (mean) NONEXE INDE EXE board,by(g2)
 
*图4  按照BOARD大小分组董事会成员比例分析
twoway (line NONEXE g2,lwidth(0.8)) ///
       (line INDE g2,lpattern(shortdash)lwidth(0.8)) ///
       (line EXE g2,lpattern(longdash) lwidth(0.8)), ///
	   xlabel(1 "min" 2 3 4 "max" 5,noticks) ///
	   ylabel(#4,grid nogmin gmax glcolor(black) angle(0) format(%4.1f) noticks) ///
	   xtitle(" ") ytitle(" ")  ///
	   subtitle("图4 按照BOARD大小分组董事会成员比例分析",pos(6))  ///
       legend(label(1 "NONEXE") label(2 "INDE") label(3 "EXE")  ///
	           pos(3) col(1) region(lpattern(blank))) graphregion(color(white))

*图5 NONEXE的Kernel密度估计			   
use graphdata,clear
drop ind ipoyear
kdensity NONEXE,norm note(,pos(2) ring(0)) lwidth(0.6) ///
         title("图5 NONEXE的Kernel密度估计",pos(6))  
			  
*图6 INDE的kernel密度估计			
kdensity INDE,norm note(,pos(2) ring(0)) lwidth(0.6) ///
         title("图6 INDE的kernel密度估计",pos(6)) 			   
			   
			   
			   
			   
			   
			   
			   
			   
 
