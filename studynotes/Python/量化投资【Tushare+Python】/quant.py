============金融数据采集===========

-------------国外财经数据采集--pandas内置模块----------
from pandas_datareader import data,wb
import pandas_datareader as pdr

import pandas_datareader.data as web
xdata = web.DataReader(code,'yahoo',start='1/1/1900') #目前yahoo的API好像不能用了???

-------------国内财经数据采集--TuShare----------------
import tushare as ts
---最新API：融合 get_hist_data()+get_h_data()
get_k_data()
	code:证券代码,支持沪深A、B股、全部指数、ETF基金
	ktype：数据类型,默认为D日线数据 D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟
	autype:复权类型,qfq-前复权 hfq-后复权 None-不复权，默认为qfq
	index:是否为指数,默认为False设定为True时认为code为指数代码
	start:开始日期,format：YYYY-MM-DD 为空时取当前日期
	end:结束日期,format：YYYY-MM-DD 

---获取交易数据:
# 历史行情(open,high,close,low,volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20,turnover)
ts.get_hist_data('600848') #近三年
	code：股票或指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
	start：开始日期，格式YYYY-MM-DD
	end：结束日期，格式YYYY-MM-DD
	ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
	retry_count：当网络异常后重试次数，默认为3
	pause:重试时停顿秒数，默认为0

# 复权数据(open,high,close,low,volume,amount)
ts.get_h_data(code,start,end,...)
	autype:复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
	index:是否是大盘指数，默认为False

# 实时行情(changepercent,trade,open,high,low,settlement,volume,turnoverratio)
ts.get_today_all()

# 某日历史分笔(time,price,change,volume,amount,type)
ts.get_tick_data()
# 实时分笔
ts.get_realtime_quotes([])
# 当前交易日（交易进行中使用）已经产生的分笔明细数据(time,price,change,volume,amount,type)
ts.get_today_ticks()

# 大盘指数实时行情列表(change,preclose,close,high,low,volume,amount)
ts.get_index()

# 大单交易数据
ts.get_sina_dd('600848', date='2015-12-24', vol=500)  #指定大于等于500手的数据,默认400手

-----获取投资参考数据：
# 分红预案
ts.profit_data(top=60)
	year : 预案公布的年份，默认为2014
	top :取最新n条数据，默认取最近公布的25条
	retry_count：当网络异常后重试次数，默认为3
	pause:重试时停顿秒数，默认为0

# 业绩预告
ts.forecast_data(2014,2) #2014年第二季度

# 限售股解禁
ts.xsg_data()
	year:年份,默认为当前年
	month:解禁月份，默认为当前月
	retry_count：当网络异常后重试次数，默认为3
	pause:重试时停顿秒数，默认为0

# 基金持股
ts.fund_holdings(year, quarter)

# 新股数据(ipo)
ts.new_stocks()

# 融资融券+明细信息
ts.sh_margins(start='2015-01-01', end='2015-04-19')
ts.sh_margins_details(start='2015-01-01', end='2015-04-19', symbol='601989')

ts.sz_margins(start='2015-01-01', end='2015-04-19')
ts.sz_margins_details('2015-01-01')

------股票分类数据：
ts.get_industry_classified() #行业分类
ts.get_concept_classified() #概念分类
ts.get_area_classified() #地域分类(属于哪个省)
ts.get_sme_classified()#中小板002
ts.get_gem_classified() #创业板300
ts.get_st_classified() #风险警示板st
ts.get_hs300s() #沪深300成分股及权重
ts.get_sz50s() #上证50成分股
ts.get_zz500s() #中证500成分股
ts.get_terminated() #上交所终止上市股票
ts.get_suspended() #上交所暂停上市股票

------基本面数据：
# 获取沪深股票基本信息,包含代码、地区、股本、资产、市盈率、市净率、上市日期等数据
ts.get_stock_basics() #股票基本信息
ts.get_report_data(year, quarter) #业绩报告
ts.get_profit_data(year, quarter) #盈利能力
ts.get_operation_data(year, quarter) #营运能力
ts.get_growth_data(year, quarter) #成长能力
ts.get_debtpaying_data(year, quarter) #偿债能力
ts.get_cashflow_data(year, quarter) #现金流量

-----宏观经济数据：
ts.get_deposit_rate() #存款利率
ts.get_loan_rate() #贷款利率
ts.get_rrr() #存款准备金率

-----货币供应量：
ts.get_money_supply() #货币供应量(活期、定期、储蓄)
ts.get_money_supply_bal() #货币供应量(年底余额)
ts.get_gdp_year() #国内生产总值(GDP、GNP年度)
ts.get_gdp_quarter() #季度
ts.get_gdp_for() #三大需求对GDP的贡献
ts.get_gdp_pull() #三大产业对GDP的拉动
ts.get_gdp_contrib() #三大产业贡献率
ts.get_cpi() #居民消费价格指数
ts.get_ppi() #工业品出厂价格指数

-----新闻事件数据：
ts.get_latest_news(top=5,show_content=True) #显示最新5条新闻，并打印出新闻内容
ts.latest_content(url) #单独获取新闻内容

ts.get_notices() #信息地雷
ts.notice_content(url)

ts.guba_sina(show_content=True) #获取sina财经股吧首页的重点消息

----银行间同业拆放利率：
ts.shibor_data(year) #Shibor拆放利率
ts.shibor_quote_data(year) #银行报价数据
ts.shibor_ma_data(year) #Shibor均值数据
ts.lpr_data(year) #贷款基础利率（LPR）
ts.lpr_ma_data(year) #LPR均值数据

=========统计学基础============
from scipy import stats
数据的位置:mean()/median()/mode()/quantile()
数据的离散度:极差 max()-min()/平均绝对偏差 mad()/var()/std()
概率质量函数:np.random.choice([1,2,3,4,5],size=100,replace=True,p=[0.1,0.1,0.3,0.4,0.1])
概率密度函数:stats.kde.gaussian_kde()
累积分布函数:stats.kde.gaussian_kde().cumsum()

二项分布:np.random.binomial(n,p,size)
			n 伯努利试验的次数
			p 伯努利变量取值1的概率
			size 随机数的数量
		->概率质量函数:stats.binom.pmf(50,100,0.5) #100次试验50次正面朝上的概率
		->累积分布函数:stats.binom.cdf(50,100,0.5) #100次试验正面朝上次数小于等于50次的概率

正态分布: norm = np.random.normal(loc,scale,size)
		->概率密度函数:stats.norm.pdf(norm)
		->累积分布函数:stats.norm.cdf(norm)
		->查询累积密度值为 0.05的分位数:stats.norm.ppf(0.05,μ,std) 
		#即有95%的概率损失不超过VaR（value at risk,风险价值）:在α%水平下,
		#某一金融资产或组合在未来特定时间内的最大损失,即P{Xt<-VaR}=α%
卡方分布:stats.chi.pdf(x,n) #x为横轴,n为自由度
t分布:stats.t.pdf(x,n) #x为横轴,n为自由度
F分布:stats.f.pdf(x,n1,n2)

置信区间:interval(alpha,df,loc,scale)
		->stats.t.interval(0.95,len(x)-1,np.mean(x),stats.sem(x)) #x为一个样本序列

t检验：
单样本t检验:样本均值与总体均值差异的显著性检验
	->stats.ttest_1samp(series,0)
独立样本t检验：两个独立总体的样本均值差异的显著性检验,如果两个样本彼此不独立则应使用配对样本t检验
	->stats.ttest_ind(series1,series2)
配对样本t检验：检验两个相关样本是否来自具有相同均值的总体
	->stats.ttest_rel(series1,series2)

方差分析：在不同的水平（因子变量）下，反应变量是如何取值的以及哪种情况下反应变量取值更高。
	原理：TSS = ESS + FSS
		总离差平方和 = 组内偏差平方和（误差平方和） + 组间离差平方和（因子平方和）
	自由度：N-1 = (N-M) + (M-1)
	方差分析统计量=组间均方差/组内均方差：ψ = MSF/MSE = [FSS/(M-1)]/[ESS/(N-M)]~F(M-1,N-M),
									   ψ较大说明MSF对样本总波动的贡献较大，因子影响十分显著。
	->单因素方差分析：只研究一个因子的方差分析
		from statsmodels.stats import anova
		from statsmodels.formula.api import ols
		models = ols('y~c(x)',data=data).fit()
		anova.anova_lm(models)

	->多因素方差分析：研究的是每个因子是否对因变量有着重要影响，而不是因子整体对因变量是否有重要影响。
		from statsmodels.stats import anova
		from statsmodels.formula.api import ols
		models = ols('y~c(x1)+c(x2)',data=data).fit()
		anova.anova_lm(models)

	->析因方差分析：在多因素方差分析的基础上引入因子之间的乘项，一个因子对因变量的影响大小可能受另一个因子水平的影响。
		from statsmodels.stats import anova
		from statsmodels.formula.api import ols
		models = ols('y~c(x1)*c(x2)',data=data).fit()
		anova.anova_lm(models)

回归分析：需要通过statsmodels包构建一个OLS类,再调用 fit()方法。其他方法或属性：
		params()/conf_int()/fittedvalues/resid/aic/predict()
		import statsmodels.api as sm
		model = sm.OLS(y,sm.add_constant(x)).fit()
		model.summary()
		model.fittedvalues
		model.resid
		->回归诊断图：plt.scatter(model.fittedvalues,model.resid)
		->正态QQ图：sm.qqplot(model.resid_pearson,sm.norm,line='45')
		->位置尺度图：plt.scatter(model.fittedvalues,model.resid_pearson**0.5)

==========金融理论、投资组合与量化选股=========
收益率：
	计算单期简单收益率：Rt = (Pt/Pt-1) - 1 
	含股利的单期简单收益率：Rt = (Pt+Dt)/Pt-1 -1
		import ffn 
		Rt = ffn.to_returns(closeprice)
	计算年化收益率：[(1+r1)(1+r2)...(1+rn)]**m/T - 1 # m为一年的期数,T为资产持有期数,m/T为复利次数,r1-rn为T期内日收益率序列
		annualize = (1+Rt).cumprod()[-1]**(245/311)-1 #假定一年245个交易日,持有311天
		def annualize(returns,period):
			if period=='day':
				return (1+returns).cumprod()[-1]**(245/len(returns))-1
			elif period=='month':
				return (1+returns).cumprod()[-1]**(12/len(returns))-1
			elif period=='year':
				return (1+returns).cumprod()[-1]**(1/len(returns))-1
			else:
				raise Exception('Wrong Period')
	单期连续复利收益率: rt = ln(1+Rt) = ln(Pt/Pt-1) =lnPt - lnPt-1
	多期连续复利收益率: rt = ln(1+Rt(k)) = ln(Pt/Pt-k) =lnPt - lnPt-k #等于单期连续复利收益率之和
		import ffn
		ffn.to_log_returns(closeprice) #单期

风险的度量：方差（标准差）风险度量法偏离了风险的本意,风险意味着潜在的损失,只有向下的波动才和风险的本意相契合,
			向上的波动反而会使投资者获益，无法反应风险的经济性质,有违于投资者对风险的真实心理感受。
	->下行风险：下行偏差风险度量法
		总体下行偏差：δ（R,MARR）= E{[min(R-MARR,0)]**2}**0.5 #MARR为可接受最低收益率
		样本下行偏差：δ（R,MARR）= {1/T * Σ[min(R-MARR,0)]**2}**0.5 
		#Downside Risk
		def  cal_downside_deviation(returns):
			MARR = returns.mean()
			risk_return = returns[returns<MARR]
			downside_deviation = (sum((MARR-risk_return)**2)/len(returns))**0.5
			return downside_deviation

	->风险价值：VaR
		returns.quantile(0.05) #历史模拟法
		scipy.stats.norm.ppf(0.05,returns.mean(),returns.std()) #协方差矩阵法
	->期望亏空：ES（expected shortfall）
		弥补了VaR理论上的缺点,考虑的是超过VaR水平的损失的期望值
		returns[returns<=returns.quantile(0.05)].mean()
	->最大回撤：MDD（maximum drawdown）= max D(T)
		回撤指资产在T时刻的最高峰值Pt与现在价值PT之间的回落值,即对t∈(0,T),D(T)=max{0,max Pt - PT}
		回撤率 d(T) = D(T)/max Pt
		收益率序列 r=R1,R2,R3,...,RT 价格Pt=∏(1+Rt)
		
		price = (1+r).cumprod()
		D = price.cummax() - price #回撤
		d = D/(D+price) #回撤率
		MDD = D.max() #最大回撤
		mdd = d.max() #最大回撤率
		#快捷法计算最大回撤率mdd 
		import ffn
		ffn.calc_max_drawdown()

投资组合理论：
# Markowitz均值方差模型:
# E(Rp)=Rf + [E(Rm)-Rf]/δm * δp
# market-portfolio :(δm,Rm),如果所有的投资人对各资产未来收益率的估计是一致的,
	# 那么理性投资人持有风险资产的相对比例是一样的,风险偏好水平不同只会影响到持有无风险资产的比例,
	# 每个投资人持有的相同的相对投资比例的风险资产组合即为市场投资组合。  
#两种风险资产组合:
	# δ(Rp)=sqrt(Wa**2 * δ(Ra)**2 + Wb**2 * δ(Rb)**2 + 2WaWb*δ(Ra,Rb))
	import numpy as np
	import math
	import matplotlib.pyplot as plt
	def cal_mean(frac):
		return (0.08*frac+0.15*(1-frac))
	mean = list(map(cal_mean,[x/50 for x in range(51)]))
	sd_mat = np.array([list(map(lambda x:math.sqrt(\
			(x**2)*0.12**2+(1-x)**2*0.25**2+2*x*(1-x)*(-1.5+i*0.5)*0.12*0.25),\
			[x/50 for x in range(51)])) for i in range(1,6)])
	plt.plot(sd_mat[0,:],mean,label='-1')
	plt.plot(sd_mat[1,:],mean,label='-0.5')
	plt.plot(sd_mat[2,:],mean,label='0')
	plt.plot(sd_mat[3,:],mean,label='0.5')
	plt.plot(sd_mat[4,:],mean,label='1')
	plt.legend(loc='upper left')
# Markowitz 最优资产配置(二次规划问题)：
	sh_return #上证股票回报率
	#计算累积回报率
	cumreturn = (1+sh_return).cumprod()
	#绘制收益率和累积收益率图
	sh_return.plot()
	plt.title('Daily Return of 5 Stocks(2014-2015)')
	plt.legend(loc='lower center',bbox_to_anchor=(0.5,-0.3),\
				ncol=5,fancybox=True,shadow=True)
	cumreturn.plot()
	plt.title('Cumulative Return of 5 Stocks(2014-2015)')
	#查看股票回报率的相关性
	sh_return.corr()
	#定义MeanVariance类
	from scipy import linalg
	^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	-------------------------------这个类有很多问题???---------------------------------
	class MeanVariance(object):
		def __init__(self,returns):
			self.returns = returns
		#求解二次规划：方差最小
		def minVar(self,goalRet):
			covs=np.array(self.returns.cov())
			means = np.array(self.returns.mean())
			L2 = list(np.ones(len(means)))
			L1 = np.append(np.append(covs.swapaxes(0,1),[means],0),[L2],0).swapaxes(0,1)
			L2.extend([0,0])
			L3 = list(means).extend([0,0])
			L4 = np.array([L2,L3])
			L = np.append(L1,L4,0)
			results = linalg.solve(L,np.append(np.zeros(len(means)),[1,goalRet],o))
			return (np.array([list(self.returns.columns),results[:-2]]))
		#定义最小方差边界曲线函数
		def frontierCurve(self):
			goals = [x/500000 for x in range(-100,4000)]
			variances = list(map(lambda x: self.calVar(self.minVar(x)[1,:].astype(np.float)),goals))
			plt.plot(variances,goals)
		#给定各资产比例,计算收益率均值
		def meanRet(self,fracs):
			meanRisky = ffn.to_returns(self.returns).mean()
			assert len(meanRisky) == len(fracs),"Length of fractions must be equal to number of assets"
			return np.sum(np.multiply(meanRisky,np.array(fracs)))
		# 给定各资产比例,计算收益率方差
		def  calVar(self,fracs):
			return np.dot(np.dot(fracs,self.returns.cov()),fracs)
	^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	#绘制最小方差边界曲线
	minvar = MeanVariance(sh_return)
	minvar.frontierCurve()
	#选取训练集和测试集
	train_set = sh_return['2014']
	test_set = sh_return['2015']
	#选取组合
	varMinimizer = MeanVariance(train_set)
	goal_return = 0.003
	portfolio_weight = varMinimizer.minVar(goal_return)
	#计算测试集收益率
	test_return = np.dot(test_set,np.array([portfolio_weight[1,:].astype(np.float)]).swapaxes(0,1))
	test_return = pd.DataFrame(test_return,index=test_set.index)
	test_cum_return = (1+test_return).cumprod()
	#与随机生成的组合比较
	sim_weight = np.random.uniform(0,1,(100,5))
	sim_weight = np.apply_along_axis(lambda x:x/sum(x),1,sim_weight)
	sim_return = np.dot(test_set,sim_weight.swapaxes(0,1))
	sim_return = pd.DataFrame(sim_return,index = test_cum_return.index)
	sim_cum_return = (1+sim_return).cumprod()
	plt.plot(sim_cum_return.index,sim_cum_return,c="g")
	plt.plot(test_cum_return.index,test_cum_return)

# Black Litterman模型：Markowitz模型得到的最优资产配比对输入参数过于敏感。
	(1)计算历史收益率之均值μ及协方差矩阵Σ。
	(2)用历史收益率均值作为先验预期收益之期望值,即π=μ。
	(3)结合投资者个人的观点（由P、Q、Ω代表,P、Q已知,Ω需计算）。
	(4)根据公式计算后验分布之期望值、协方差。

	'''定义函数blacklitterman()来计算后验分布之期望值、协方差,输入变量有历史收益率returns,
	反应主观观点相对于先验信息地比重tau,代表投资人看法的P、Q,以历史收益率均值mu和协方差矩
	阵sigma作为先验预期收益之期望值和协方差,然后根据公式计算后验分布之期望值er和协方差posteriorsigma
	'''
	def blacklitterman(returns,tau,P,Q):
		mu = returns.mean()
		sigma = returns.cov()
		pi1 = mu
		ts = tau*sigma
		omiga = np.dot(np.dot(P,ts),P.T)*np.eye(Q.shape[0])
		middle = linalg.inv(np.dot(np.dot(P,ts),P.T)+omiga)
		er = np.expand_dims(pi1,axis=0).T + np.dot(np.dot(np.dot(ts,P.T),middle),\
				(Q-np.expand_dims(np.dot(P,pi1.T),axis=1)))
		posteriorsigma = sigma + ts - np.dot(ts.dot(P.T).dot(middle).dot(P),ts)
		return [er,posteriorsigma]
	#构造投资人个人观点-资产选择矩阵P：假设分析师认为前4只股票收益率为日均0.3%,两只交通股
	# 日均收益比浙能电力高0.1%

	pick1 = np.array([1,0,1,1,1])
	q1 = np.array([0.003*4])
	pick2 = np.array([0.5,0.5,0,0,-1])
	q2 = np.array([0.001])
	P = np.array([pick1,pick2])
	Q = np.array([q1,q2])
	#修正后验收益
	res = blacklitterman(sh_return, 0.1, P, Q)
	p_mean = pd.DataFrame(res[0],index=sh_return.columns,columns=['posterior_mean'])
	p_cov = res[1]
	#得到后验收益期望值与协方差矩阵后利用Markowitz模型进行资产配置,
	#定义新的函数blminVar()求解资产配置权重,输入变量是blacklitterman()
	#的输出结果blres,以及投资人的目标收益率goalRet
	def blminVar(blres,goalRet):
		covs = np.array(blres[1])
		means = np.array(blres[0])
		L1 = np.append(np.append(covs.swapaxes(0,1),[means.flatten()],0),[np.ones(len(means))],0).swapaxes(0,1)
		L2 = list(np.ones(len(means)))
		L2.extend([0,0])
		L3 = list(means)
		L3.extend([0,0])
		L4 = np.array([L2,L3])
		L = np.append([L1,L4,0])
		results = linalg.solve(L,np.append(np.zeros(len(means)),[1,goalRet],0))
		return pd.DataFrame(results[:-2],index=blres[1].columns,columns=['p_weight'])

#CAPM Rit - Rft = αi + βi(Rmt - Rft)+εit
	#式中α是由Jensen引入的,称为Jensen's Alpha,CAPM假设Rit服从正态分布,所有资产的α都应该是0,
	#或者不显著地异于0,若α显著异于0,则称个股i有异常收益,α值代表收益率胜过大盘的部分。
	
	#所有投资者都试图利用各种分析方法创造显著正的α:
		# 基本面分析：经济环境、产业、公司
		# 技术面分析：'历史会重演'
		# 消息面分析：基于CAPM模型的事件研究法
		# Alpha策略：基于CAPM构建投资组合对冲掉系统风险,锁定Alpha超额收益

#Fama-French Three Factors Model:
	理论模型：E(Rit) - Rft = bi[E(Rmt)-Rft] + si E(SMBt) + hi E(HMLt)
	实证模型：Rit -  Rft = αi + bi(Rmt-Rft) + si SMBt + hi HMLt + εit
	#3个因子均为投资组合的收益率：
		1.市场风险溢价因子--对应市场投资组合的收益率;
		2.市值因子SMB(Small Minus Big)--小公司比大公司高出的收益率,
			对应做多市值较小公司、做空市值较大公司的投资组合之收益率;
		3.账面市值比因子HML(High Minus Low)--高B/M股票收益率减去低B/M公司的股票收益率,
			对应的是做多高B/M比的公司、做空低B/M比的公司投资组合之收益率。 

#时间序列：
自协方差：γl = cov(Xk,Xk-l),l =0,1,2...
自相关系数：ρl = cov(Xk,Xk-l)/var(Xk) = γl/γ0
	--同一变量在不同时期取值的相关程度。刻画的是自己过去的行为对自己现在的影响。
偏自相关系数： pll = corr(Xk,Xk-l|Xk-1,Xk-2,...,Xk-l+1)
	--自相关系数刻画的不单单是昨天对今天的直接影响,也包含了更早各期信息对今天的间接影响,
		衡量的是前面所有期加总的影响效果,PACF衡量过去单期对现在的影响效果,剔除了其他期的作用。

#计算自相关系数
statsmodels.tsa.stattools.acf(x,unbiased=False,nlags=40,qstat=False,fft=False,alpha=None)
	nlags表示计算acf的最大滞后期数
	qstat表示是否返回Ljung-Box检验的结果
	fft为使用的算法
	alpha表示计算自相关系数的置信区间所用的置信水平
statsmodels.tsa.stattools.pacf(x,nlags=40,method='ywunbiased',alpha=None)
#绘制自相关系数图
statsmodels.graphics.tsaplots.plot_acf(x,use_vline=True,lags=30)
statsmodels.graphics.tsaplots.plot_pacf(x,use_vline=True,lags=30)

#对一个平稳的时间序列而言,其自相关系数或偏自相关系数大都快速减小至0,
#非平稳时间序列其自相关系数多数呈现缓慢下降的趋势。

平稳性：
	分析的前提是'历史可以重演',即时间序列的基本特性必须能从过去维持到我们欲推测的时期;
如果时间序列的基本特性维持不变就称时间序列是平稳的;若时间序列的基本特性只存在于所发生的当期,
不会延续到未来,那么这样一个时间序列不足以昭示未来,就称时间序列是非平稳的。
#随机游走过程(单位根过程)--非平稳
	Xt = Xt-1 + εt,其中X0=0,εt~N(0,δε**2)

#ADF单位根检验：
	ADF(y,lags,trend,max_lags,method)
		trend--'nc'不含截距项;'c'含有截距项;'ct'包含截距项及线性趋势项;'ctt'包含截距及二次趋势项
		lags--一阶差分的滞后阶数,若不指定则使用method所指定的方法选择滞后阶数
		max_lags--根据method所指定的方法选择滞后阶数时的滞后阶数上限
		method--选择阶数所使用的方法,包括'aic'、'bic'、't_stat'
	from arch.unitroot import ADF
	ADF().summary().as_text()

#白噪声：特殊的平稳时间序列--无自相关性,预测也无法进行
	对任意时点t,E(Xt)=0,var(Xt)=δ**2,γl=0(l>0)
	#白噪声检验:LB检验--Q统计量--H0为纯随机序列(白噪声序列)
	statsmodels.tsa.stattools.q_stat(acf,nobs,type='ljungbox')
	->example:#返回两个数组,一个Q统计量数组+一个p值数组
		stattools.q_stat(stattools.acf(sh_return),len(sh_return))

预测：前提是平稳的、非随机序列
#移动平均预测：取平均数时,数值的随机波动成分在一定程度上会被消除掉,预测值受过去极端值的干扰
			# 减少,从而达到平滑效果。<简单移动平均、加权移动平均、指数加权移动平均>
#预测模型
	---平稳、同方差时间序列---
	AR(p)、MA(q)、ARMA(p,q)
	---非平稳、同方差序列---
	ARIMA
	---非平稳、异方差序列---
	ARCH、GARCH
example:ARMA模型构建
	1.单位根检验：无单位根则继续
	2.白噪声检验：LB检验,非白噪声则继续
	3.识别参数p和q：plot_acf/plot_pacf
	4.构建p、q组合：选择AIC、或者BIC最小的模型
	from statsmodels.tsa import arima_model
	model1 = arima_model.ARIMA(CPItrain,order=(1,0,1)).fit() #order(p,I,q)
	model2=arima_model.ARIMA(CPItrain,order=(1,0,2)).fit()
	...
	5.模型评价：系数显著性检验、残差序列白噪声检验[若为白噪声说明已充分提取了序列信息,否则模型需要完善]
#查看系数的置信区间
	model.conf_int()
	stdresid = model.resid/math.sqrt(model.sigma2) #标准化残差序列
	plot_acf(stdresid,lags=20)
	LjungBox = stattools.q_stat(stattools.acf(stdresid)[1:13],len(stdresid))
	LjungBox[1][-1]
#模型预测
	model.forecast(3)[0]

3、4 更为简洁的方法:statsmodels.tsa.stattools.arma_order_select_ic #arma阶数选择信息准则
	from statsmodels.tsa import stattools,arima_model
	stattools.arma_order_select_ic(CPItrain,max_ma=4) #会给出最大4阶中BIC最小的阶数
	model = arima_model.ARIMA(CPItrain,order=(1,0,0)).fit()

#GARMA(p,q):时间序列每个时间点变量的波动率是最近P个时间点残差平方的线性组合,与最近q个时间
			# 变量波动率的线性组合相加
	#通常以收益率序列的平方以及绝对值序列的图形来识别序列是否具有ARCH效应(波动聚集效应)
	plt.subplot(211)
	plt.plot(sh_return**2)
	plt.subplot(212)
	plt.plot(np.abs(sh_return))
	#利用LB检验来检验收益率平方的自相关性
	from statsmodels.tsa import stattools
	LjungBox = stattools.q_stat(stattools.acf(sh_return**2)[1:13],len(sh_return))
	LjungBox[1][-1]
	# 构建GARCH模型
	from arch import arch_model
	am = arch_model(sh_return) #默认GARCH(1,1)
	model = am.fit(update_freq=0) #不输出中间结果
	model.summary()

配对交易：又称为价差交易或统计套利交易,指在市场中寻找两只历史价格走势有对冲效果的股票（走势一致）,
		组成配对使得股票的价差大致在一个范围内波动。
	#股票对的选择：行业内匹配、产业链配对、财务管理配对
	#选择标准一：最小距离法
	1.单期收益率：rt = (Pt-Pt-1)/Pt-1
	2.标准化价格：pt = ∏(1+rt) #累计收益率表示
	3.价格偏差平方和：SSDx,y = Σ(ptx - pty)**2
	def SSD(price_x,price_y):
		if price_x is None or price_y is None:
			print('缺少价格序列')
		return_x = (price_x-price_x.shift(1))/price_x.shift(1)[1:] #计算单期收益率
		return_y = (price_y-price_y.shift(1))/price_y.shift(1)[1:]
		standard_x = (1+return_x).cumprod()
		standard_y = (1+return_y).cumprod()
		SSD = np.sum((standard_x-standard_y)**2)
		return SSD

	#选择标准二：协整--金融资产对数价格一般为一阶单整序列。其一阶差分约等于单期简单收益率。
	1.首先检验两只股票的对数价格序列是否为 I(1),或者收益率序列{rt}是否平稳;
		from arch.unitroot import ADF
		import numpy as np
		logprice = np.log(price)
		ADF(logprice).summary().as_text() #应具有单位根
		logprice_diff = logprice.diff()[1:]
		ADF(logprice_diff).summary().as_text() #应拒绝单位根
	2.协整检验：对两个序列进行线性回归,检验残差序列是否平稳
		import statsmodels.api as sm
		mmodel = sm.OLS(logprice_x,sm.add_constant(logprice_y))
		results = model.fit()
		results.summary()
		resid_adf = ADF(results.resid,trend='nc')#残差序列单位根检验,因残差均值为0所以trend为nc
	3.编写策略
->最小距离法交易策略：
	# 根据两只股票A、B价格差得均值和标准差设定交易信号触发点'u±nδ'
	# 当价差下穿u-nδ时正向开仓,当价差线回复到均线时平仓,当价差线上穿u+nδ时反向开仓
	standardA = (1+retA).cumprod() #标准化价格【累计收益率】
	standardB = (1+retB).cumprod()
	SSD_pair = standardB - standardA
	meanSSD_pair = np.mean(SSD_pair)
	stdSSD_pair = np.std(SSD_pair)
	thresholdUp = meanSSD_pair + 1.2stdSSD_pair
	thresholdDown = meanSSD_pair - 1.2stdSSD_pair
	SSD_pair.plot()
	plt.axhline(y = meanSSD_pair,color='black')
	plt.axhline(y = thresholdUp,color='green')
	plt.axhline(y = thresholdDown,color='green')

->更好的编程规范--构建PairTrading类[配对交易]
import re
import pandas as pd
import numpy as np
from arch.unitroot import ADF
import statsmodels.api as sm
class PairTrading(object):
	def __init__(self,priceX,priceY):
		if priceX is None or priceY is None:
			print('缺少价格序列')
		self.priceX = priceX
		self.priceY = priceY
		self.returnX = (priceX-priceX.shift(1))/priceX.shift(1)[1:]
		self.returnY = (priceY-priceY.shift(1))/priceY.shift(1)[1:]
		self.standardX = (1+self.returnX).cumprod()
		self.standardY = (1+self.returnY).cumprod()
	#最小距离
	def SSD(self):
		SSD = np.sum((self.standardX-self.standardY)**2)
		return SSD
	def SSDspread(self):
		spread = self.standardY - self.standardX
		return spread
	#协整
	def cointegration(self): # log(P_Y) = α + β*log(P_X) + ε
		logpriceX = np.log(self.priceX)
		logpriceY = np.log(self.priceY)
		results = sm.OLS(logpriceY,sm.add_constant(logpriceX)).fit()
		resid = results.resid
		resid_adf = ADF(resid)
		if resid_adf.pvaule>=0.05:
			print('''交易价格不具有协整关系
				P-value of ADF test:%f
				Coefficients of regression:
				Itercept:%f
				Beta:%f
				'''%(resid_adf.pvaule,results.params[0],results.params[1]))
			return None
		else:
			print('''交易价格具有协整关系
				P-value of ADF test:%f
				Coefficients of regression:
				Itercept:%f
				Beta:%f
				'''%(resid_adf.pvaule,results.params[0],results.params[1]))
			return (results.params[0],results.params[1])
	def CointegrationSpread(self,FormPeriod,TradePeriod):
		if not (re.fullmatch('\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}',FormPeriod)
			or re.fullmatch('\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}',TradePeriod)):
			print('形成期或交易期格式错误')
		formX=self.priceX[FormPeriod.split(':')[0]:FormPeriod.split(':')[1]]
		formY=self.priceY[FormPeriod.split(':')[0]:FormPeriod.split(':')[1]]
		coefficients=self.cointegration(formX,formY)
		if coefficients is None:
			print('未形成协整关系,无法配对')
		else:
			# spread=log(P_Y)-[α_hat + β_hat*log(P_X)],形成期估计的参数应用于交易期,类似于残差
			spread = (np.log(self.priceY[TradePeriod.split(':')[0]:TradePeriod.split(':')[1]])\
					-coefficients[0]-coefficients[1]*np.log(self.priceX[TradePeriod.split(':')[0]:\
						TradePeriod.split(':')[1]]))
			return spread
	def CalBound(self,method,FormPeriod,TradePeriod,width=1.5):
		if not (re.fullmatch('\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}',FormPeriod)
			or re.fullmatch('\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}',TradePeriod)):
			print('形成期或交易期格式错误')
		if method == 'SSD':
			spread = self.SSDspread(self.priceX[FormPeriod.split(':')[0]:FormPeriod.split(':')[1]],\
									self.priceY[FormPeriod.split(':')[0]:FormPeriod.split(':')[1]])	
			mu = np.mean(spread)
			sd = np.std(spread)
			UpperBound = mu+width*sd
			LowerBound = mu-width*sd
			return (UpperBound,LowerBound)
		elif method='cointegration':
			spread = self.CointegrationSpread(FormPeriod, TradePeriod)
			mu = np.mean(spread)
			sd = np.std(spread)
			UpperBound = mu+width*sd
			LowerBound = mu-width*sd
			return (UpperBound,LowerBound)
		else:
			print('不存在该方法,请选择SSD或者cointegration')			

K线图------------
# matplotlib.finance :
	candlestick2_ochl()/candlestick2_ohlc()/candlestick_ochl()/candlestick_ohlc()
#参数：
	#日期数据必须为浮点型：需要将字符串时间格式转为浮点型--matplotlib.dates/finance/pylab.date2num()
	#传入的数据对象为序列类型:需要将DataFrame转为list
import matplotlib.pyplot as plt
import matplotlib.finance as mpf 
from datetime import datetime
def candlestick(df):
	fig,ax = plt.subplots(figsize=(14,7))
	quotes = []
	for index,(d,o,c,h,l) in enumerate(zip(df.index,df.open,df.close,df.high,df.low)):
	# for index,row in df.iterrows():
		# d = datetime.strptime(index,'%Y-%m-%d')
		# d = mpf.date2num(d)
		# dochl = (d,row[:4])
		d = datetime.strptime(d,'%Y-%m-%d')
		d = mpf.date2num(d)
		dochl = (d,o,c,h,l)
		quotes.append(dochl)
	mpf.candlestick_ochl(ax, quotes,width=0.6,colorup='red',colordown='green')
	ax.xaxis_date()
	ax.autoscale_view()
	return plt.show()

->捕捉早晨之星：
	#计算每一个交易日收盘价与开盘价的差值
	ClOp = Close - Open 
	#---捕捉绿色实体、十字星和红色实体---
	shape = [0,0,0]
	lag1ClOp = ClOp.shift(1) 
	lag2ClOp = ClOp.shift(2) 
	for i in range(3,len(ClOp)):
		if all([lag2ClOp[i]<-11,abs(lag1ClOp[i]<2,ClOp[i]>6,\
			abs(ClOp[i])>abs(lag2ClOp[i])*0.5)]): #只捕捉到了相对大小
			shape.append(1)
		else:
			shape.append(0)
	#查看第一个1所在位置
	shape.index(1)
	#---捕捉十字星---
	Doji = [0,0,0]
	for i in range(3,len(Open)):
		if all([lagOpen[i]<Open[i],lagOpen[i]<lag2Close[i],\
			lagClose[i]<Open[i],lagClose[i]<lag2Close[i]]): #进一步捕捉相对位置
			Doji.append(1)
		else:
			Doji.append(0)
	#有多少个十字星
	Doji.count(1)
	#---捕捉下跌趋势---
	ret = Close/Close.shift(1) - 1
	lag1ret = ret.shift(1)
	lag2ret = ret.shift(2)
	trend = [0,0,0]
	for i in range(3,len(ret)):
		if all([lag1ret[i]<0,lag2ret[i]<0]):
			trend.append(1)
		else:
			trend.append(0)
	#---捕捉早晨之星---
	DawnStar=[]
	for i in range(len(trend)):
		if all([shape[i]==1,Doji[i]==1,trend[i]==1]):
			DawnStar.append(1)
		else:
			DawnStar.append(0)
	#---查看早晨之星的日期---
	for i in  range(len(DawnStar)):
		if DawnStar[i]==1:
			print(data.index[i])

->捕捉乌云盖顶：
lagClose = Close.shift(1)
lagOpen = Open.shift(1)
cloud = pd.Series(0,index=Close.index)
for i in range(1,len(Close)):
	if all([Close[i]<Open[i],lagClose[i]>lagOpen[i]\
		Open[i]>lagClose[i],Close[i]>lagOpen[i]\
		Close[i]<0.5*(lagClose[i]+lagOpen[i])]):
		cloud[i]=1
trend = pd.Series(0,index=Close.index)
for i in range(2,len(Close)):
	if Close[i-1] >Close[i-2]>Close[i-3]:
		trend[i]=1
darkcloud = cloud + trend
darkcloud[darkcloud==2]

----动量交易策略----
#若动量>0,说明股票还具备上涨的能量,释放出买入信号;若动量<0,说明股票可能有下跌的能量,释放出卖出信号。
#动量产生的原因
	# 1.反应不足：投资者对信息的反应不及时,使得上涨下跌会持续一段时间
	# 2.正反馈模式：羊群效应、从众心理、认知判断倾向于公众舆论或者行为
	# 3.过度反应：因高估自身的投资判断能力或过度相信对私有信息的预测性而保持错误行为
# 动量的计算
	作差法：Momentum_t = Pt - Pt-m
	作除法：Momentum_t =ROCt(rate of change)=(Pt-Pt-m)/Pt-m

def momentum(price,period):
	lagprice=price.shift(period)
	momentum = price-lagprice
	momentum = momentum.dropna()
	return momentum
#根据动量值生成买卖点--以35日动量为例
signal = []
for i in momentum35:
	if i>0:
		signal.append(1) #买入
	else:
		signal.append(-1) #卖出
#根据买卖点制定买入卖出交易
signal = pd.Series(signal)
trade_sig = signal.shift(1)
ret = Close/Close.shift(1) - 1
momentumRet = (ret*trade_sig).dropna()
#策略评价--计算策略获胜率
win = momentumRet[momentumRet>0]
winrate = len(win)/len(momentumRet[momentumRet!=0])
loss = momentumRet[momentumRet<0]
performance = pd.DataFrame({'win':win.describe(),'loss':loss.describe()})

-------相对强弱指标RSI--------
RSI(relative strength index):衡量买卖力量的强弱。若买入力量大于卖出力量则价格会上涨;反之下跌。
RSI = 100 * RS/(1+RS) = 100 * UP/(UP+DOWN)
	#UP、DOWN分别表示t期内股价上涨、下跌幅度平均值-(可利用SMA/WMA/EWMA)
	#RSI∈[0,100],当RSI接近0时,卖方力量强,股票下跌的力量远大于上涨的力量
		#当RSI接近于100时,股票上涨的力量远大于下跌的力量。
#编写RSI函数：参数为价格序列price以及期数period
def rsi(price,period=6):
	import numpy as np
	import pandas as pd
	from pandas import Series
	if not isinstance(price,Series):
		print('TypeError:The type of input must be pandas Series')
	prc_change = price - price.shift(1)
	up_prc_change = pd.Series(np.where(prc_change>0,prc_change,0),index=price.index)
	down_prc_change = pd.Series(np.where(prc_change<0,np.abs(prc_change),0),index=price.index)
	up_prc_change_mean = up_prc_change.rolling(window=period).mean()
	down_prc_change_mean = down_prc_change.rolling(window=period).mean()
	rsi = 100*up_prc_change_mean/(up_prc_change_mean+down_prc_change_mean)
	return rsi
# 交易信号：
->#RSI超买线、超卖线、中心线
	超买线：RSI=70/80/90,股票买入力量过大,买入力量未来可能减小回归正常,股价可能下跌,此时应卖出股票;
	超卖线：RSI=30/20/10,股票卖出力量过大,卖出力量未来可能减小回归正常,股价可能上涨,此时应买入股票;
	中心线：RSI=50,股票买卖力量均衡
->#RSI'黄金交叉'与'死亡交叉'
	定义不同时间跨度的RSI：
	当短期RSI线向上穿过长期RSI线时,股票近期买入力量较强,价格上涨力量很大,释放出较强的买入信号,称为'黄金交叉';
	当短期RSI线向下穿过长期RSI线时,股票近期卖出力量较强,价格下跌力量很大,释放出较强的卖出信号,称为'死亡交叉'。
#RSI策略编写
rsi6 = rsi(price,6)
rsi24 = rsi(price,24)
sig1=[] #超买超卖信号
for i in rsi6:
	if i>80:
		sig1.append(-1)
	elif i<20:
		sig1.append(1)
	else:
		sig1.append(0)
signal1 = pd.Series(sig1,index=rsi6.index)
signal2 = pd.Series(0,index=rsi6.index) #交叉信号
lagrsi6=rsi6.shift(1)
lagrsi24=rsi24.shift(1)
for i in lagrsi6.index:
	if (rsi6[i]>rsi24[i]) and (lagrsi6[i]<lagrsi24[i]):
		signal2[i] = 1
	elif (rsi6[i]<rsi24[i]) and (lagrsi6[i]>lagrsi24[i]):
		signal2[i] = -1
signal = signal1 + signal2 #合并交易信号
signal[signal>=1]=1
signal[signal<=-1]=-1
signal = signal.dropna()
#RSI策略执行
tradesig = signal.shift(3)
ret = Close/Close.shift(1) - 1
# -----买入交易收益率
ret = ret[tradesig.index] 
buy = tradesig[tradesig==1]
buyRet = ret[tradesig==1] * buy
# ----卖出交易收益率
sell=tradesig[tradesig==-1]
sellRet = ret[tradesig==-1] * sell
#----合并收益率
tradeRet = ret*tradesig
#比较RSI指标交易策略的累计收益率
cum_stock = np.cumprod(1+ret)-1
cum_trade = np.cumprod(1+tradeRet)-1
#----作收益率图
#RSI策略评价
def strat_review(tradesignal,ret):
	ret = ret[tradesignal.index]
	tradeRet = ret*tradesignal
	tradeRet[tradeRet==(-0)]=0
	win_rate =len(tradeRet[tradeRet>0])/len(tradeRet[tradeRet!=0]) 
	win_mean =sum(tradeRet[tradeRet>0])/len(tradeRet[tradeRet>0])
	loss_mean =sum(tradeRet[tradeRet<0])/len(tradeRet[tradeRet<0])
	performance = pd.DataFrame({"win_rate":win_rate,"win_mean":win_mean,"loss_mean":loss_mean})
	return performance
buy_only = strat_review(buy, ret)
sell_only = strat_review(sell, ret)
trade_all = strat_review(tradesig, ret)
Test = pd.DataFrame({'buy_only':buy_only,'sell_only':sell_only,'trade_all':trade_all})
----------均线系统策略-----------
--期数的选择：
	1.事件发展的周期性：以周期长度为期数,消除周期性影响（如季节性）
	2.对趋势修匀的要求：期数越多趋势越清晰
	3.对趋势反映近期变化敏感度的要求：期数越少,反应的变化越敏感;长期趋势做长期平均,短期趋势做短期平均
--简单移动平均：Series.rolling(window=5).mean()
--加权移动平均：wma
	#需自定义加权移动平均wma
def wma(price,window=5):
	import numpy as np
	import pandas as pd 
	from pandas import Series,DataFrame
	if not isinstance(price, (Series,DataFrame)):
		print('TypeError:The type of input must be pandas Series or DataFrame')
	arr = np.arange(1,window+1)
	w = arr/arr.sum()
	wma = Series(0.0,index=price.index)
	for i in np.arange(window-1,len(price)):
		wma[price.index[i]] = np.dot(w,price[price.index[(i+1-window):(i+1)]])
	return wma 
--指数加权移动平均： pd.Series.ewm(com=None, span=None, min_periods=0).mean()

# 均线交叉策略:
	当短期均线从（下/上）向（上/下）穿过长期均线时,释放出（买入/卖出）信号。
sma5 = Close.rolling(window=5).mean()
sma30 = Close.rolling(window=30).mean()
signal = pd.Series(0,index=sma30.index)
for i in range(1,len(sma30)):
	if all([sma5[i]>sma30[i],sma5[i-1]<sma30[i-1]]):
		signal[i] = 1
	elif all([sma5[i]<sma30[i],sma5[i-1]>sma30[i-1]]):
		signal[i] = -1
tradesig = signal.shift(1)

buy = pd.Series(0,index=sma30.index)
buy[tradesig==1] = 1
ret = Close/Close.shift(1) -1
buy_ret = (buy*ret).dropna()
win_rate_buy = len(buy_ret[buy_ret>0])/len(buy_ret[buy_ret!=0])

sell = pd.Series(0,index=sma30.index)
sell[tradesig==-1] = -1
sell_ret = (sell*ret).dropna()
win_rate_sell = len(sell_ret[sell_ret>0])/len(sell_ret[sell_ret!=0])

strat_ret = (tradesig*ret).dropna()
win_rate = len(strat_ret[strat_ret>0])/len(strat_ret[strat_ret!=0])

cum_ret_buy = (1+buy_ret).cumprod() -1
cum_ret_sell = (1+sell_ret).cumprod() -1
cum_ret = (1+strat_ret).cumprod() -1

#异同移动平均线--MACD(Moving Average Convergence/Divergence)
两线一柱（DIF、DEA、MACD）：
	股价 的指数加权移动平均离差值：DIF = ewma12 - ewma26
	离差值 的指数加权移动平均：DEA = ewma9
	MACD = DIF - DEA # MACD可以反映出股票近期价格走势的能量和变化强度
1.DIF与DEA都在零刻度上方,表明市场可能是多头行情;反之市场可能处于空头行情。
	->'零上双金叉策略'：DIF先上穿DEA,不久下跌到DEA下方,然后DIF又上穿DEA,说明股价上升趋势较强。
2.DIF上穿信号线DEA时,释放出买入信号;当DIF下穿信号线DEA时,释放出卖出信号。
3.MACD柱形图在零刻度上方,表示DIF大于DEA,市场走势较强;反之市场走势较弱。

import talib
dif,dea,bar = talib.MACD(df.close,fastperiod=12,slowperiod=26,signalperiod=9)

# DIF与DEA线交叉背离策略
	->DIF、DEA均为正,DIF上穿DEA为买入信号;
	->DIF、DEA均为负,DIF下穿DEA为卖出信号。
signal_macd = pd.Series(0,index=DIF.index[1:])
for i in range(1,len(DIF)):
	if all([DIF[i]>DEA[i]>0.0,DIF[i-1]<DEA[i-1]]):
		signal_macd[i]=1
	elif all([DIF[i]<DEA[i]<0.0,DIF[i-1]>DEA[i-1]]):
		signal_macd = -1
tradesig = signal_macd.shift(1)
strat_ret = (tradesig*ret).dropna()
strat_ret[strat_ret==-0]=0
win_rate_macd = len(strat_ret[strat_ret>0])/len(strat_ret[strat_ret!=0])

# 多种均线指标综合运用策略
asset = pd.Series(0.0,index=Close.index)
cash = pd.Series(0.0,index=Close.index)
share = pd.Series(0,index=Close.index)

entry = 3
cash[:3]=20000
while  entry<len(Close):
	cash[entry] = cash[entry-1]
	if all([Close[entry-1]>=Close[entry-2]>=Close[entry-3],tradesig[entry-1]!=-1]):
		share[entry]=1000
		cash[entry] = cash[entry] - 1000*Close[entry]
		break
	entry+=1
i = entry+1
while  i<len(tradesig):
	cash[i] = cash[i-1]
	share[i] = share[i-1]
	if tradesig[i]==1:
		share[i] = share[i] + 3000
		cash[i] =cash[i] - 3000*Close[i]
	if all([tradesig[i]==-1,share[i]>=1000]):
		share[i] = share[i] -1000
		cash[i] = cash[i] + 1000*Close[i]
	i+=1
asset = cash + share*Close

strat_ret = (asset[-1]-20000)/20000

-----通道突破策略-----------
# 唐安奇通道:当价格线向上突破上界时买入;当价格线向下突破下界时卖出。
上界 = 过去20日内的最高价
下界 = 过去20日内的最低价
中轨道 = (上界+下界)/2

UpperBound = High.rolling(20).max().dropna()
LowerBound = Low.rolling(20).min().dropna()
MiddleBound = (UpperBound+LowerBound)/2

def upbreak(price,UpperBound):
	n = min([len(price),len(UpperBound)])
	price = price[-n:]
	UpperBound = UpperBound[-n:]
	signal = pd.Series(0,index=price.index)
	for i in range(1,len(price)):
		if all([price[i]>UpperBound[i],price[i-1]<UpperBound[i-1]]):
			signal[i]=1
	return signal

def downbreak(price,LowerBound):
	n = min([len(price),len(LowerBound)])
	price = price[-n:]
	LowerBound = LowerBound[-n:]
	signal = pd.Series(0,index=price.index)
	for i in range(1,len(price)):
		if all([price[i]<LowerBound[i],price[i-1]>LowerBound[i-1]]):
			signal[i]=-1
	return signal

UpBreak = upbreak(Close[UpperBound.index[0]:], UpperBound)
DownBreak = downbreak(Close[LowerBound.index[0]:], LowerBound)

signal = upbreak+downbreak
tradesig = signal.shift(1)
ret = Close/Close.shift(1) -1
strat_ret = (tradesig*ret).dropna()
strat_ret[strat_ret==-0]=0
win_rate = len(strat_ret[strat_ret>0])/len(strat_ret[strat_ret!=0])

#布林带通道：以股价平均线为参照线,上通道为均线加上一定倍数的标准差,下通道为均线减去一定倍数的标准差
def bbands(price,window=20,times=2):
	import pandas as pd 
	from pandas import Series,DataFrame
	if not isinstance(price, (Series,DataFrame)):
		print('TypeError:The type of input must be pandas Series or DataFrame')
	sma = price.rolling(window).mean()
	sd = price.rolling(window).std()
	UpBBand = sma + times*sd
	DownBBand = sma - times*sd
	BBands = pd.DataFrame({'UpBBand':UpBBand.dropna(),\
							'MiddleBBand':sma.dropna(),\
							'DownBBand':DownBBand.dropna(),\
							'sigma':sd.dropna()})
	return BBands

#布林带风险：股价突破布林带上下界时,说明股价出现了异常波动,异常波动的概率称为布林带风险。
def  BollRisk(price,α=0.05):
	import pandas as pd 
	from pandas import Series,DataFrame
	from scipy import stats
	if not isinstance(price, (Series,DataFrame)):
		print('TypeError:The type of input must be pandas Series or DataFrame')
	times = stats.norm.ppf(1-α/2)
	BBands = bbands(price,times=times)
	price = price[BBands.index[0]:]
	try:
		up_risk = pd.value_counts(price>BBands.UpBBand)[True]
	except:
		up_risk = 0
	try:
		down_risk = pd.value_counts(price<BBands.DownBBand)[True]
	except:
		down_risk = 0
	boll_risk = (up_risk+down_risk)/len(price)
	return pd.Series([α,round(times,2),round(boll_risk,4)],index=['conf_level','n','boll_risk'])

#布林带策略
BBands = bbands(Close)
upsig = upbreak(Close, BBands.UpBBand)
downsig = downbreak(Close, BBands.DownBBand)

tradesig = upsig.shift(2)+downsig.shif(2)
tradesig[tradesig==-0]=0

def strat_review(price,tradesig):
	ret = price/price.shift(1) -1
	strat_ret = (ret*tradesig).dropna()
	ret = ret[-len(strat_ret):]
	win_rate = [len(ret[ret>0])/len(ret[ret!=0]),\
				len(strat_ret[strat_ret>0])/len(strat_ret[strat_ret!=0])]
	win_mean = [np.mean(ret[ret>0]),np.mean(strat_ret[strat_ret>0])]
	loss_mean =  [np.mean(ret[ret<0]),np.mean(strat_ret[strat_ret>0])]
	performance = pd.DataFrame({'win_rate':win_rate,'win_mean':win_mean,'loss_mean':loss_mean})
	performance.index =['stock','trade_strat']
	return performance
#特殊布林带策略：上穿下通道时买,下穿上通道时卖
...
upsig = upbreak(Close, BBands.DownBBand)
downsig = downbreak(Close, BBands.UpBBand)
...

#商品通道指数CCI
CCI（N日）=（TP－MA）÷MD÷0.015 
	其中：
	TP=（最高价 +最低价 +收盘价）÷3
	MA=最近N日收盘价的累计之和÷N
	MD=最近N日（MA－收盘价）的累计之和÷N
	0.015为计算系数，N为计算周期

def CCI(data, ndays): 
	TP = (data['High'] + data['Low'] + data['Close']) / 3 
	CCI = pd.Series((TP - pd.rolling_mean(TP, ndays)) / (0.015 * pd.rolling_std(TP, ndays)),name = 'CCI') 
	data = data.join(CCI) 
	return data
->CCI指标区间的划分
	1、按市场的通行的标准，CCI指标的运行区间可分为三大类：大于100、小于-100和100 — -100之间。
	2、当CCI＞+100时，表明股价已经进入非常态区间——超买区间，股价的异动现象应多加关注。
	3、当CCI＜-100时，表明股价已经进入另一个非常态区间——超卖区间，投资者可以逢低吸纳股票。
	4、当CCI介于100—-100之间时表明股价处于窄幅振荡整理的区间——常态区间，投资者应以观望为主。

->CCI指标区间的判断
	1、当CCI指标从下向上突破100线而进入非常态区间时，表明股价脱离常态而进入异常波动阶段，中短线应及时买入。
	2、当CCI指标从上向下突破-100线而进入另一个非常态区间时，表明股价的盘整阶段已经结束，将进入一个比较长的寻底过程，投资者应以持币观望为主。
	3、当CCI指标从上向下突破+100线而重新进入常态区间时，表明股价的上涨阶段可能结束，将进入一个比较长时间的盘整阶段。投资者应及时逢高卖出股票。
	4、当CCI指标从下向上突破-100线而重新进入常态区间时，表明股价的探底阶段可能结束，又将进入一个盘整阶段。投资者可以逢低少量买入股票。
	5、当CCI指标在+100线—-100线的常态区间运行时，投资者则可以用KDJ、CCI等其他超买超卖指标进行研判。

----------随机指标交易策略-------------
随机指标KDJ:由K线、D线、J线三条线组成,根据特定周期内资产的最高价、最低价、最后一个计算时点
	的收盘价以及这三种价格的比例关系,来计算最后一个时点的未成熟随机值RSV（Raw Stochastic Value）,
	进而通过移动平均法来计算K、D、J的值。

	RSV =(第n天的收盘价-n天内的最低价)/(n天内的最高价-n天内的最低价) *100
	->RSV∈[0,100],取值越大,说明收盘价在价格区间中的相对位置越高,市场中可能出现超买现象;
		取值越小,收盘价的相对位置越低,市场中可能出现超卖行情。

#计算RSV
def RSV(price,window=9):
	import pandas as pd 
	from pandas import Series,DataFrame
	if not isinstance(price, (Series,DataFrame)):
		print('TypeError:The type of input must be pandas Series or DataFrame')
	max_price = price.rolling(window).max()
	min_price = price.rolling(window).min()
	RSV = 100*(price - min_price)/(max_price-min_price)
	return RSV.dropna()

->RSV的缺点：当市场行情连续上涨（下跌）时,RSV在一段时间内可能连续多期取值100（0）,
	会出现所谓的'钝化'现象,从而失去捕捉收盘价变化的作用,甚至造成超买超卖的'假信号'。
->为了解决上述问题引入K指标对RSV进行平滑。
	Kt = 2/3*Kt-1 + 1/3*RSVt
	Dt = 2/3*Dt-1 + 1/3*Kt
	J = 3*Kt - 2*Dt #KD的辅助指标,进一步反映了K指标和D指标的乖离程度。较为可靠。
->如无特别指定,第一期K值和D值默认为50;权重2/3和1/3是常用权重

def KDJ(RSV,K0=50,D0=50,w=2/3):
	K = pd.Series(0.0,index=RSV.index)
	K[0] = w*K0 + (1-w)*RSV[0]
	D = pd.Series(0.0,index=RSV.index)
	D[0] = w*D0 + (1-w)*K[0]
	for i in range(1,len(RSV)):
		K[i] = w*K[i-1] + (1-w)*RSV[i]
		D[i] = w*D[i-1] + (1-w)*K[i]
	J = 3*K - 2*D
	return pd.DataFrame({'K':K,'D':D,'J':J},columns=['K','D','J'])

# KDJ交易策略
	1.K值或D值在80以上为超买区,在20以下为超卖区;
	2.J值大于100可视为超买区,小于0视为超卖区;
	3.K线上穿D线为'黄金交叉',买入;K线下穿D线为'死亡交叉',卖出;

signal_K = KDJ.K.apply(lambda x: -1 if x>85 else 1 if x<20 else 0)
signal_D = KDJ.D.apply(lambda x: -1 if x>80 else 1 if x<20 else 0)
signal_J = KDJ.J.apply(lambda x: -1 if x>100 else 1 if x<0 else 0)
signal_KDJ = signal_K + signal_D + signal_J
signal_KDJ.name = 'KDJsignal'
signal_J =signal_KDJ.apply(lambda x: 1 if x>=2 else -1 if x<=-2 else 0)

ret = (Close-Close.shift(1))/Close.shift(1)
tradesig = signal_KDJ.shift(1)
trade_ret = (tradesig*ret).dropna()
ret = ret[trade_ret.index[0]:]

def backtest(ret,trade_ret):
	def performance(x):
		import ffn
		win_rate = len(x[x>0])/len(x[x!=0])
		ret_ann = (1+x).cumprod()[-1]**(245/len(x))-1
		sharpe = ffn.calc_risk_return_ratio(x)
		max_drawdown = ffn.calc_max_drawdown((1+x).cumprod())
		performance = pd.Series([win_rate,ret_ann,sharpe,max_drawdown],\
						index=['win_rate','ret_ann','sharpe','max_drawdown'])
		return performance
	stock_perfo = performance(ret)
	trade_perfo = performance(trade_ret)
	return pd.DataFrame({'stock_perfo':stock_perfo,'trade_perfo':trade_perfo})
KDJ_cum_ret = (1+trade_ret)*cumprod()

#KD金叉与死叉
def upbreak(K,D):
	signal = np.all([K>D,K.shift(1)<D.shift(1)],axis=0) #！！！！！！！！！！
	return pd.Series(signal*1,index=K.index)

def downbreak(K,D):
	signal = np.all([K<D,K.shift(1)>D.shift(1)],axis=0)
	return pd.Series(signal*-1,index=K.index)

Close_Diff = Close.diff()
price_trend = 2*(Close_Diff>0)-1 #[1,-1]！！！！！！！！！！！！！

signal_up = upbreak(KDJ.K, KDJ.D) #[1,0] 金叉信号
signal_down = downbreak(KDJ.K, KDJ.D) #[-1,0] 死叉信号

signal = ((price_trend+signal_up)==2)*1
signal[(price_trend+signal_down)==-2] = -1
# signal = price_trend + signal_up + signal_down
# signal = signal.replace([2,-2,1,-1],[1,-1,0,0])

ret = (Close-Close.shift(1))/Close.shift(1)
tradesig = signal.shift(1)
trade_ret = (tradesig*ret).dropna()
ret = ret[trade_ret.index[0]:]

backtest(ret, trade_ret)
cross_cum_ret = (1+trade_ret).cumprod()

#根据交易信号构造交易状态函数(假设不能做空)
def Hold(signal):
	hold = pd.Series(0,index=signal.index)
	for i in range(1,len(hold)):
		if hold[i-1]==0 and signal[i]==1:
			hold[i] = 1
		elif hold[i]==1 and sinal[i]==1:
			hold[i]=1
		elif hold[i]==1 and signal[i]==0:
			hold[i] =1
	return hold
hold = Hold(signal)
#定义模拟交易函数 ????感觉有错误
def TradeSimulate(price,hold):
	position = pd.Series(0,index=price.index)
	position[hold.index] = hold.values
	cash = 20000*np.ones_like(price) 
	for t in range(1,len(price)):
		if position[t-1]==0 and position[t]==1:
			cash[t] = cash[t-1]-price[t]*1000
		if position[t-1]==1 and position[t]==0:
			cash[t] = cash[t-1]+price[t]*1000
		if position[t-1]==position[t]:
			cash[t]=cash[t-1]
	asset = cash+price*position*1000
	account = pd.DataFrame({'asset':asset,'cash':cash,'position':position})
	return account

能量潮交易策略：
->OBV（On Balance Volume）：
	成交量可以反映出市场买卖双方的活跃情况,量是价的先行者,市场动能应该由成交量的变化情况来反映。
	# 理论依据
	1.当投资者对股价的预期一致时,成交量较小,例如当投资者一致认为股价将上涨时,买单数量会变多,持有
	  股票的人不会卖出,卖单数量相对较少,成交量就相对较小;相反,当投资者对股价的预期不一致时,成交量上升。
	2.根据重力原理：股价易跌难涨,且股价下跌所需要的成交量要小于股价上升所需要的成交量。
	3.根据惯性原理：热门股在相当长一段时间内会保持较大成交量和价格波动,冷门股则相反。 

->指标计算：
  --累积OBV
	OBVn = OBVn-1 ± Vn #将股价上涨时的成交量正累加,股价下跌时的成交量负累加
	Close_Diff = Close.diff()
	OBV=((2*(Close_Diff>=0)-1)*Volume).cumsum()
  --移动型OBV
  	smOBV = 累积OBV.rolling().mean()
  --修正行OBV：多空比率净额（Volume Accumulation）
  	VAn =VAn-1 + Vn*[(Cn-Ln)-(Hn-Cn)]/(Hn-Ln) 
  	# 考虑了股价因素,Hn、Ln、Cn分别是最高价、最低价和收盘价
  	# Cn-Ln:表示多头力量强度 
  	# Hn-Cn:表示空头力量强度 
	# (Cn-Ln)-(Hn-Cn)：表示多头净力量幅度
	# [(Cn-Ln)-(Hn-Cn)]/(Hn-Ln)：表示多头相对力量对于成交量的贡献程度
	AdjOBV = ((((Close-Low)-(High-Close))/(High-Low))*Volume).cumsum()

# OBV指标交易策略制定:OBV指标增大时买入,减小时卖出。
import ffn 
def trade_strat(price,OBV):#定义交易策略函数
	signal = (2*(OBV.diff()>0)-1)
	ret = ffn.to_returns(price)
	trade_ret = ret*signal.shift(1)
	return pd.DataFrame({'stock_ret':ret,'trade_ret':trade_ret}).dropna()

((1+ret).cumprod()-1).plot(label='ret',linestyle='dashed')
((1+trade_ret).cumprod()-1).plot(label='trade_ret') #评价策略表现

backtest(ret, trade_ret) #交易表现

OBV指标应用原则：单期OBV指标并没有太大意义
1.OBV曲线稳步上升,同时股价上涨：行情稳步向上,股价仍有上涨空间,中长期走势良好;--多
2.OBV曲线缓慢下降,同时股价下跌：行情不佳,股价会继续下跌;--空或观望
3.OBV曲线上升但股价下降：表明股价下跌时成交量却在上升,投资者信心不断增强;--多
4.OBV曲线下降但股价上升：股价上升但成交量在缩小,表明投资者逐渐丧失信心,股价很可能接近顶点;--空
5.两种极端情况：OBV曲线快速上升,表明买盘迅速涌入,持续性不强,股价在短暂拉升后可能会迅速下跌;
			  OBV曲线快速下降,表明卖盘迅速涌入,随后仍有可能有较长下跌。--观望

====数据标准化====
def regular_std(s): #零-均值规范化
	return (s-s.mean())/s.std()
def regular_mm(s): #最大最小规范化
	return (s-s.min())/(s.max()-s.min())
def regular_two_series(s1,s2,type='look_max') #两个序列向较大(小)均值序列看齐
	s1_mean = s1.mean()
	s2_mean = s2.mean()
	if type=='look_max':
		s1 ,s2 = (s1,s1_mean/s2_mean * s2) if s1_mean>s2_mean else (s1*s2_mean/s1_mean,s2)
	elif type == 'look_min':
		s1 ,s2 = (s1*s2_mean/s1_mean,s2) if s1_mean>s2_mean else (s1,s1_mean/s2_mean * s2)
	return s1,s2
====双y轴======
_,ax1 = plt.subplots()
ax1.plot()
ax2 = ax1.twinx()
ax2.plot()

===分位数====
from scipy import stats
stats.scoreatpercentile(s, per)

=====插值=====#看不懂
from scipy.interpolate import interp1d,splrep,splev
_,axs = plt.subplots(1,2)
linear_interp = interp1d(x, y) #线性插值
axs[0].plot(x,y,'',x,linear_interp(x),'r.')
splrep_interp = splrep(x, y) #B-spline插值
axs[1].plot(x,y,'',x,splev(x, splrep_interp),'g.')

====凸优化======
import scipy.optimize as sco
sco.fminbound(func, x1, x2) #寻找给定范围内的最小值
sco.fmin_bfgs(f, x0) #寻找给定值的局部最小值
sco.brute(func, ranges) #求解函数全局最优权重
sco.minimize(fun, x0) #标准凸优化求解

=====3D绘图=====
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = Axes3D(fig)
x = np.arange(-10,10,0.5)
y = np.arange(-10,10,0.5)
x_grid,y_grid = np.meshgrid(x,y)
z_grid = x_grid**2 + y_grid**2
ax.plot_surface(x_grid, y_grid, z_grid,rstride=1,cstride=1,cmap='hot')

=====PCA/SVD====
from sklearn.decomposition import PCA
pca = PCA(0.95) #PCA(n_components=None, copy=True, whiten=False)  
#PCA对象的属性
	components_ ：返回具有最大方差的成分。
	explained_variance_ratio_：返回 所保留的n个成分各自的方差百分比。
	n_components_：返回所保留的成分个数n。
	mean_：
	noise_variance_：

# PCA对象的方法
fit(X,y=None) #训练。因为PCA是无监督学习算法，此处y自然等于None。
fit_transform(X)#用X来训练PCA模型，同时返回降维后的数据--lowDimDataMat。
inverse_transform()#将降维后的数据转换成原始数据，X=pca.inverse_transform(newX)
transform(X)#将数据X转换成降维后的数据。当模型训练好后，对于新输入的数据，都可以用transform方法来降维。
get_covariance()
get_precision()
get_params(deep=True)
score(X, y=None)

def pca(dataMat, k):
	'''
	减去平均数
	计算协方差矩阵
	计算协方差矩阵的特征值和特征向量
	将特征值从大到小排序
	保留最大的K个特征向量
	将数据转换到上述K各特征向量构建的新空间中
	'''
	meanVals = np.mean(dataMat, axis=0)
	DataRmMean = dataMat - meanVals           #减去平均值
	covMat = np.cov(DataRmMean, rowvar=0) #rowvar=0表示列为变量
	eigVals,eigVects = linalg.eig(covMat) #计算特征值和特征向量
	#print eigVals
	eigValInd = np.argsort(eigVals)
	eigValInd = eigValInd[:-(k+1):-1]   #保留最大的前K个特征值
	redEigVects = eigVects[:,eigValInd]        #对应的特征向量
	lowDimDataMat = np.dot(DataRmMean,redEigVects)     #将数据转换到低维新空间
	reconMat = np.dot(lowDimDataMat,redEigVects.T) + meanVals   #重构数据，用于调
	return lowDimDataMat, reconMat

lowDMat, reconMat = pca(dataMat,1)
print "shape(lowDMat): ",lowDMat.shape
#二维作图
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(dataMat[:,0].flatten().A[0],dataMat[:,1].flatten().A[0],marker='^',s=90)
ax.scatter(reconMat[:,0].flatten().A[0],reconMat[:,1].flatten().A[0],marker='o',s=50,c='red')
plt.show()


from scipy import linalg
u,d = linalg.eig(mat) #特征分解只能作用于方阵
u,s,v = linalg(mat) #奇异值分解为奇异值和奇异向量,可作用于任何维度,但旋转不可转回
