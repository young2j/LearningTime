# # # # # # # # import matplotlib.pyplot as plt #惯常的import语句
# # # # # # # # plt.style.use("ggplot") #使用ggplot2风格的图形

# # # # # # # # customers = ["ABC","DEF","GHI","JKL","MNO"]
# # # # # # # # customers_index = range(len(customers))
# # # # # # # # sale_amounts = [127,90,201,111,232]

# # # # # # # # fig = plt.figure() #matplotlib绘图首先要创建一个基础图,然后在基础图中创建一个或多个子图
# # # # # # # # ax1 = fig.add_subplot(1,1,1) #创建一个一行一列并使用第一个的子图
# # # # # # # # ax1.bar(customers_index,sale_amounts,align="center",color="darkblue") 
# # # # # # # # #创建条形图bar(x,y,align,color),align="center"设置条形图与标签中间对齐

# # # # # # # # ax1.xaxis.set_ticks_position("bottom")#设置X轴刻度的位置在底部
# # # # # # # # ax1.yaxis.set_ticks_position("left") #设置Y轴刻度的位置在左侧

# # # # # # # # plt.xticks(customers_index,customers,rotation=0,fontsize="small")
# # # # # # # # #将刻度线标签由客户索引值更改为客户名称,rotation=0表示刻度标签水平无倾斜角度
# # # # # # # # plt.xlabel("Customer Name")
# # # # # # # # plt.ylabel("Sale Amount")
# # # # # # # # plt.title("Sale Amount per Customer")

# # # # # # # # plt.savefig("bar_plot.png",dpi=400,bbox_inches="tight")#bbox_inches表示将图形四周的空白部分去掉
# # # # # # # # plt.show()#表示在一个新窗口中显示
# # # # # # # import numpy as np
# # # # # # # import matplotlib.pyplot as plt
# # # # # # # plt.style.use("ggplot")

# # # # # # # mu1,mu2,sigma = 100,130,15
# # # # # # # x1 = mu1 + sigma*np.random.randn(10000)
# # # # # # # x2 = mu2 + sigma*np.random.randn(10000)

# # # # # # # fig = plt.figure()
# # # # # # # ax1 = fig.add_subplot(1,1,1)
# # # # # # # n,bins,patches = ax1.hist(x1,bins=50,normed=False,color="darkgreen")
# # # # # # # n,bins,patches = ax1.hist(x2,bins=50,normed=False,color="orange",alpha=0.5)
# # # # # # # ax1.xaxis.set_ticks_position("bottom")
# # # # # # # ax1.yaxis.set_ticks_position("left")
# # # # # # # plt.xlabel("Bins")
# # # # # # # plt.ylabel("Number of Values in Bin")
# # # # # # # fig.suptitle("Histograms",fontsize=14,fontweight="bold")
# # # # # # # ax1.set_title("Two Frequency Distributions")
# # # # # # # plt.savefig("Histogram.png",dpi=400,bbox_inches="tight")
# # # # # # # plt.show()
# # # # # # from numpy.random import randn
# # # # # # import matplotlib.pyplot as plt

# # # # # # plot_data1 = randn(50).cumsum()
# # # # # # plot_data2 = randn(50).cumsum()
# # # # # # plot_data3 = randn(50).cumsum()
# # # # # # plot_data4 = randn(50).cumsum()

# # # # # # plt.style.use("ggplot")
# # # # # # fig = plt.figure()
# # # # # # ax1 = fig.add_subplot(1,1,1)
# # # # # # ax1.plot(plot_data1,marker=r"o",color=u"blue",linestyle="-",label="Blue Solid")
# # # # # # ax1.plot(plot_data2,marker=r"+",color=u"red",linestyle="--",label="Red Dashed")
# # # # # # ax1.plot(plot_data3,marker=r"*",color=u"green",linestyle="-.",label="Green Dash Dot")
# # # # # # ax1.plot(plot_data4,marker=r"s",color=u"orange",linestyle=":",label="Orange Dotted")
# # # # # # ax1.xaxis.set_ticks_position("bottom")
# # # # # # ax1.yaxis.set_ticks_position("left")
# # # # # # ax1.set_title("Line plots:Markers,Colors,and linestyles")
# # # # # # plt.xlabel("Draw")
# # # # # # plt.ylabel("Random Number")
# # # # # # plt.legend(loc="best") #loc="best"根据图中空白把图例放在最合适的位置
# # # # # # plt.savefig("line_plot.png",dpi=4000,bbox_inches="tight")
# # # # # # plt.show()

# # # # # import numpy as np
# # # # # import matplotlib.pyplot as plt

# # # # # x = np.arange(1,15,1) #stat=1,stop=15,step=1,返回数组
# # # # # y_linear = x+5*np.random.randn(14) 
# # # # # y_quadratic = x**2+10*np.random.randn(14) 
# # # # # fn_linear = np.poly1d(np.polyfit(x, y_linear, deg=1))
# # # # # '''
# # # # # [1] np.poly1d(c_or_r,r=False)返回一维多项式(方程),例如p=np.poly1d((2,2,2,3))返回：
# # # # # 	2 x**3 + 2 x**2 + 2 x + 3 = 0
# # # # # 	若r=True,则(2,2,2,3)为根,p.c查看系数,p.r查看根,p(num)方程等于num. 
# # # # # [2] np.polyfit()返回线性拟合的系数,degree为拟合程度
# # # # # '''
# # # # # fn_quadratic = np.poly1d(np.polyfit(x, y_quadratic, deg=2))

# # # # # plt.style.use("ggplot")
# # # # # fig = plt.figure()
# # # # # ax1 = fig.add_subplot(1,1,1)
# # # # # ax1.plot(x,y_linear,"bo", #"bo"蓝色圆圈
# # # # # 		x,y_quadratic,"go", #"go"绿色圆圈,下类似. 
# # # # # 		x,fn_linear(x),"b-",
# # # # # 		x,fn_quadratic(x),"g-",linewidth=2) 
# # # # # ax1.xaxis.set_ticks_position("bottom")
# # # # # ax1.yaxis.set_ticks_position("left")
# # # # # ax1.set_title("Scatter Plots Regression Lines")
# # # # # plt.xlabel("x")
# # # # # plt.ylabel("f(x)",rotation=45)
# # # # # plt.xlim(min(x)-1,max(x)+1) #设置X轴的范围
# # # # # plt.ylim(min(y_quadratic)-10,max(y_quadratic)+10)
# # # # # plt.savefig("scatter_plot.png",dpi=400,bbox_inches="tight")
# # # # # plt.show()
# # # # import numpy as np
# # # # import matplotlib.pyplot as plt

# # # # N=500
# # # # normal = np.random.normal(loc=0, scale=1, size=N)
# # # # #返回正态分布,loc为mean的位置,scale为sd的大小,size为样本数
# # # # lognormal = np.random.lognormal(mean=0, sigma=1, size=N)#对数正态分布
# # # # index_value = np.random.random_integers(low=0, high=N-1, size=N)#创建随机索引
# # # # normal_sample = normal[index_value]
# # # # lognormal_sample = lognormal[index_value]
# # # # box_plot_data = [normal,normal_sample,lognormal,lognormal_sample]

# # # # fig = plt.figure()
# # # # ax1 = fig.add_subplot(1,1,1)
# # # # box_labels = ["normal","normal_sample","lognormal","lognormal_sample"]
# # # # ax1.boxplot(box_plot_data,notch=False,sym=".",vert=True,whis=1.5,showmeans=True,labels=box_labels)
# # # # ax1.xaxis.set_ticks_position("bottom")
# # # # ax1.yaxis.set_ticks_position("left")
# # # # ax1.set_title("Box Plots") #plt.title()
# # # # ax1.set_xlabel("Distribution") #plt.xlabel()
# # # # ax1.set_ylabel("Value",rotation=90) #plt.ylabel()
# # # # plt.savefig("box_plot.png",dpi=400,bbox_inches="tight")
# # # # plt.show()
# # # import pandas as pd
# # # import numpy as np
# # # import matplotlib.pyplot as plt

# # # data_frame = pd.DataFrame (np.random.rand(5,3),#np.random.rand(5,3)为5行3列随机数组
# # # 			index=["Customer 1","Customer 2","Customer 3","Customer 4","Customer 5"],
# # # 			columns=pd.Index(["Metric 1","Metric 2","Metric 3"],name="Metrics")) 
# # # #pd.DataFrame(data,index,columns,name):
# # # #  name  columns1 columns2 columns3
# # # # index1   data     data     data 
# # # # index2   data     data     data 
# # # # index3   data     data     data 
# # # plt.style.use("ggplot")
# # # fig,axes = plt.subplots(nrows=1,ncols=2) #创建一个基础图和一行两列的子图
# # # ax1,ax2 = axes.ravel() #将子图分别赋予ax1,ax2,等同于索引axes[0,0]和axes[0,1]
# # # data_frame.plot(kind="bar",ax=ax1,alpha=0.75,title="Bar Plot")
# # # plt.setp(ax1.get_xticklabels(),rotation=45,fontsize=10) #设置刻度标签属性
# # # plt.setp(ax1.get_yticklabels(),rotation=0,fontsize=10)
# # # ax1.set_xlabel("Customer")
# # # ax1.set_ylabel("Value")
# # # ax1.xaxis.set_ticks_position("bottom")
# # # ax1.yaxis.set_ticks_position("left")

# # # colors = dict(boxes="DarkBlue",whiskers="Gray",medians="Red",caps="Black")
# # # data_frame.plot(kind="box",color=colors,sym=".",ax=ax2,title="Box Plot")
# # # plt.setp(ax2.get_xticklabels(),rotation=45,fontsize=10) #设置刻度标签属性
# # # plt.setp(ax2.get_yticklabels(),rotation=0,fontsize=10)
# # # ax2.set_xlabel("Metric")
# # # ax2.set_ylabel("Value")
# # # ax2.xaxis.set_ticks_position("bottom")
# # # ax2.yaxis.set_ticks_position("left")

# # # plt.savefig("pandas_plots.png",dpi=400,bbox_inches="tight")
# # # plt.show()
# # from ggplot import *

# # print(mtcars.head())
# # plt1 = ggplot(aes(x='mpg'), data=mtcars) +\
# #  		geom_histogram(fill='darkblue', binwidth=2) +\
# # 		xlim(10, 35) + ylim(0, 10) +\
# # 		xlab("MPG") + ylab("Frequency") +\
# # 		ggtitle("Histogram of MPG") +\
# # 		theme_matplotlib()
# # print(plt1)

# # print(meat.head())
# # plt2 = ggplot(aes(x='date', y='beef'), data=meat) +\
# # 		geom_line(color='purple', size=1.5, alpha=0.75) +\
# # 		stat_smooth(colour='blue', size=2.0, span=0.15) +\
# # 		xlab("Year") + ylab("Head of Cattle Slaughtered") +\
# # 		ggtitle("Beef Consumption Over Time") +\
# # 		theme_seaborn()
# # print(plt2)

# # print(diamonds.head())
# # plt3 = ggplot(diamonds, aes(x='carat', y='price', colour='cut')) +\
# # 		geom_point(alpha=0.5) +\
# # 		scale_color_gradient(low='#05D9F6', high='#5011D1') +\
# # 		xlim(0, 6) + ylim(0, 20000) +\
# # 		xlab("Carat") + ylab("Price") +\
# # 		ggtitle("Diamond Price by Carat and Cut") +\
# # 		theme_gray()
# # print(plt3)

# # ggsave(plt3, "ggplot_plots.png")
# import seaborn as sb
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from pylab import savefig

# sb.set(color_codes =True) #seaborn有自己的默认调色板,参数默认False

# #直方图
# x = np.random.normal(size = 100)
# sb.distplot(x,bins=20,kde=False,rug=True,label="Histogram w/o Density")
# sb.utils.axlabel("Value","Frequency")
# plt.title("Histogram of a Random Sample from a normal Distribution")
# plt.legend()
# plt.show()

# #带有回归直线的散点图与单变量直方图
# mean,cov = [5,10],[(1,0.5),(0.5,1)]
# data = np.random.multivariate_normal(mean, cov, 200)
# data_frame = pd.DataFrame(data,columns=["x","y"])
# sb.jointplot(x="x", y="y",data=data_frame,kind="reg").set_axis_labels("x","y")
# plt.suptitle("Joint Plot of Two Variables")
# plt.show()

# #成对变量之间的散点图与单变量直方图
# iris = sb.load_dataset("iris")
# sb.pairplot(iris)
# plt.show()

# #某几个变量的箱线图
# tips = sb.load_dataset("tips")
# sb.factorplot(x="time",y="total_bill",hue="smoker",col="day",data=tips,kind="box",size=4,aspect=0.5)
# plt.show()

# #带有bootstrap置信区间的线性回归
# sb.lmplot(x="total_bill",y="tip", data=tips)
# plt.show()

# #带有bootstrap置信区间的logit回归
# tips["big_tip"] = (tips.tip/tips.total_bill)>0.15
# sb.lmplot(x="total_bill", y="big_tip", data=tips,logistic=True,	y_jitter=0.03).set_axis_labels("Total Bill","Big Tip")
# plt.title("logistic Regression")
# plt.show()
# savefig("seaborn_plots.png")
