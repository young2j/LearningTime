*十大筛选笨方法
gen big10=1 if year==2003 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"上海立信") ///
	|regexm(firm,"岳华")|regexm(firm,"中瑞华恒信")|regexm(firm,"北京京都") ///
	|regexm(firm,"信永中和")|regexm(firm,"中审"))
replace big10=1 if year==2004 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"上海立信") ///
	|regexm(firm,"岳华")|regexm(firm,"中瑞华恒信")|regexm(firm,"江苏公证") ///
	|regexm(firm,"信永中和")|regexm(firm,"中审"))
replace big10=1 if year==2005 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"上海立信") ///
	|regexm(firm,"岳华")|regexm(firm,"中瑞华恒信")|regexm(firm,"北京京都") ///
	|regexm(firm,"信永中和")|regexm(firm,"中审"))
replace big10=1 if year==2006 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"上海立信") ///
	|regexm(firm,"岳华")|regexm(firm,"中瑞华恒信")|regexm(firm,"万隆") ///
	|regexm(firm,"信永中和")|regexm(firm,"中审"))	
replace big10=1 if year==2007 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"立信") ///
	|regexm(firm,"岳华")|regexm(firm,"中瑞华恒信")|regexm(firm,"万隆") ///
	|regexm(firm,"信永中和")|regexm(firm,"中审"))
replace big10=1 if year==2008 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"立信") ///
	|regexm(firm,"利安达")|regexm(firm,"中瑞岳华")|regexm(firm,"万隆") ///
	|regexm(firm,"信永中和")|regexm(firm,"大信"))
replace big10=1 if year==2009 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"立信") ///
	|regexm(firm,"天健")|regexm(firm,"中瑞岳华")|regexm(firm,"万隆亚洲") ///
	|regexm(firm,"信永中和")|regexm(firm,"大信"))
replace big10=1 if year==2010 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"立信") ///
	|regexm(firm,"天健")|regexm(firm,"中瑞岳华")|regexm(firm,"国富浩华") ///
	|regexm(firm,"信永中和")|regexm(firm,"大信"))
replace big10=1 if year==2011 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"立信") ///
	|regexm(firm,"天健")|regexm(firm,"中瑞岳华")|regexm(firm,"国富浩华") ///
	|regexm(firm,"信永中和")|regexm(firm,"大信"))
replace big10=1 if year==2012 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"立信") ///
	|regexm(firm,"天健")|regexm(firm,"中瑞岳华")|regexm(firm,"国富浩华") ///
	|regexm(firm,"信永中和")|regexm(firm,"大华"))
replace big10=1 if year==2013 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"立信") ///
	|regexm(firm,"天健")|regexm(firm,"瑞华")|regexm(firm,"大信") ///
	|regexm(firm,"信永中和")|regexm(firm,"大华"))
replace big10=1 if year==2014 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"立信") ///
	|regexm(firm,"天健")|regexm(firm,"瑞华")|regexm(firm,"大信") ///
	|regexm(firm,"信永中和")|regexm(firm,"大华"))
replace big10=1 if year==2015 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"立信") ///
	|regexm(firm,"天健")|regexm(firm,"瑞华")|regexm(firm,"天职国际") ///
	|regexm(firm,"信永中和")|regexm(firm,"大华"))
replace big10=1 if year==2016 & (regexm(firm,"普华永道")|regexm(firm,"毕马威") ///
    |regexm(firm,"德勤")|regexm(firm,"安永华明")|regexm(firm,"立信") ///
	|regexm(firm,"天健")|regexm(firm,"瑞华")|regexm(firm,"天职国际") ///
	|regexm(firm,"信永中和")|regexm(firm,"大华"))
replace big10=0 if big10==.
		
*循环结构		
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
gen bigten=.
forvalue i=2003/2016 {
foreach x of loc c`i'{
replace bigten=1 if year==`i' & regexm(firm,"`x'")
}
}
replace bigten=0 if bigten==.


*学习记录
loc c2004 普华永道 毕马威 德勤 安永华明 上海立信 岳华 信永中和 中审 中瑞华恒信 江苏公证
loc c2005 普华永道 毕马威 德勤 安永华明 上海立信 信永中和 中审 岳华 中瑞华恒信 北京京都
loc c2006 普华永道 安永华明 德勤 毕马威 上海立信 岳华 信永中和 万隆 中审 中瑞华恒信
forvalue i=2004/2006{
di "`c`i''"
}
clear
loc c2003 普华永道 毕马威 德勤 安永华明 上海立信 岳华 中瑞华恒信 北京京都 信永中和 中审
di  "`c2003'"
普华永道 毕马威 德勤 安永华明 上海立信 岳华 中瑞华恒信 北京京都 信永中和 中审
clear
loc c2003 "普华永道 毕马威 德勤 安永华明 上海立信 岳华 中瑞华恒信 北京京都 信永中和 中审"
di  "`c2003'"
普华永道 毕马威 德勤 安永华明 上海立信 岳华 中瑞华恒信 北京京都 信永中和 中审
clear
loc c2003 "普华永道" "毕马威" "德勤" "安永华明" "上海立信" "岳华" "中瑞华恒信" "北京京都" "信永中和" "中审"
di  "`c2003'"
普华永道毕马威德勤安永华明上海立信岳华中瑞华恒信北京京都信永中和中审
di  `c2003'
普华永道" "毕马威" "德勤" "安永华明" "上海立信" "岳华" "中瑞华恒信" "北京京都" "信永中和" "中审 invalid name
r(198);















