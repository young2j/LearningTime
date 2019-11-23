机器学习分类：
	有监督机器学习：给定数据集和标签X-y,训练模型,预测输出;y代表类别时是一个分类任务,y代表连续变量时是一个回归任务。
	无监督机器学习：不关心有没有标签y,只是挖掘数据集X的一些内在规律。
	强化学习：机器在环境（environment）中学习到策略（strategy）,按策略选择一个动作（action）让对应的回报（reward）最大。

======================算法汇总===========================
----线性回归算法：
from sklearn.linear_model import *
Ridge() #岭回归
LASSO() #最小绝对值收缩和选择算法,俗称套索算法
MultiTaskLasso() #多任务LASSO回归算法
LassoLars() #LARS套索算法
ElasticNet() #弹性网眼算法
MultiTaskElasticNet() #多任务弹性网眼算法
OrthogonalMatchingPursuit() #正交匹配追踪(OMP)算法
BayesianRidge() #贝叶斯岭回归算法
ARDRegression() #ARD自相关回归算法
LogisticRegression() #逻辑回归算法
SGDClassifier() #SGD随机梯度下降算法
Lars() #最小角回归算法
Perceptron() #感知器算法
PassiveAggressiveClassifier() #PA被动感知算法
RANSACRegressor() #鲁棒回归算法
HuberRegressor() #Huber回归算法
TheilSenRegressor() #Theil-Sen回归算法
PolynomialFeatures() #多项式函数回归算法
LinearRegression() #最小二乘法线性回归算法

->example:
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=1,test_size=0.4)
estimator = LogisticRegression() 
estimator.fit(x_train, y_train)
y_pred = estimator.predict(x_test.values)

---朴素贝叶斯算法：
# Naive Bayesian：基于假定--给定目标值时,属性之间相互条件独立
from sklearn.naive_bayes import *
MultinomialNB(alpha=1.0,fit_prior=True,class_prior=None) #多项式朴素贝叶斯算法
GaussianNB([priors]) #高斯朴素贝叶斯算法
BernoulliNB() #伯努利朴素贝叶斯算法

->example:
estimator = MultinomialNB(alpha=0.01)
estimator.fit(x_train, y_train)
y_pred = estimator.predict(x_test.values)

---KNN近邻算法
from sklearn.neighbors import *
KNeighborsClassifier(n_neighbors=2,weights='distance') #KNN近邻分类算法
KNeighborsRegressor() #K近邻回归算法
RadiusNeighborsClassifier(n_neighbors=2,radius=100) #半径邻分类算法
NearestNeighbors() #最近邻居算法
NearestCentroid() #最近质心算法
LSHForest() #局部敏感哈希森林算法

->example:
estimator = KNeighborsClassifier()
estimator.fit(x_train, y_train)
y_pred = estimator.predict(x_test.values)

---随机森林算法：
from sklearn.ensemble import *
RandomForestClassifier() # 随机森林算法
BaggingClassifier() # Bagging装袋算法
ExtraTreesClassifier() # 完全随机树算法
AdaBoostClassifier()
AdaBoostRegressor() # Adaboost 迭代算法,针对同一训练集训练弱分类器,然后集合构成一个强分类器
GradientBoostingClassifier() # GBDT(Gradient Boosting Decision Tree)迭代决策树算法,一种基于决策树的分类回归算法
GradientBoostingRegressor() # 梯度回归算法
VotingClassifier() #投票算法

->example:
estimator = RandomForestClassifier(n_estimators=8)
estimator.fit(x_train,y_train) 
y_pred = estimator.predict(x_test.values)

---决策树算法：
from sklearn.tree import *
DecisionTreeClassifier() #决策树算法
ExtraTreeClassifier() #完全随机树算法
ExtraTreeRegressor() #完全随机树回归算法
export_graphviz(decision_tree) #用于输出决策树图形

->example:
estimator=DecisionTreeClassifier() 
estimator.fit(x_train, y_train)
y_pred = estimator.predict(x_test.values)

---支持向量机算法：
from sklearn.svm import *
SVC() # 支持向量机算法
LinearSVC() #线性向量算法
NuSVC() # Nu支持向量算法
SVR() #SVR(TEpsilon)支持向量算法
NuSVR() # Nu支持SVR向量算法
OneClassSVM() #一类支持微量机异常检测算法
l1_min_c() #用于返回边界参数

->example:
estimator = SVC(kernel='rbf',probability=True)
estimator.fit(x_train,y_train)
y_pred = estimator.predict(x_test.values)

---SVM-cross向量机交叉算法：
def svm_cross(x_train,y_train):
	estimator = SVC(kernel='rbf',probability=True)
	param_grid = {'C':[1e-3,1e-2,1e-1,1,10,100,1000],'gamma':[0.001,0.0001]}
	grid_search = GridSearchCV(estimator,param_grid,n_jobs=1,verbose=1)
	grid_search.fit(x_train,y_train)
	best_parameters = grid_search.best_estimator_.get_params()
	# for para,val in best_parameters.items():
		# print(para,val)
	estimator = SVC(kernel='rbf',C=best_parameters['C'],gamma=best_parameters['gamma'],probability=True)
	estimator.fit(x_train,y_train)
	return estimator 

---神经网络算法：
from sklearn.neural_network import *
BernoulliRBM() #伯努利受限波尔兹曼机神经网络算法,简称RBM算法
MLPClassifier() #多层感知器神经网络算法,简称MLP算法
MLPRegressor() #多层感知器神经网络回归算法,简称MLP回归算法

->example:
estimator = MLPClassifier(solver='lbfgs',alpha=1e-5,hidden_layer_sizes=(5,2),random_state=1)
estimator.fit(x_train, y_train)
y_pred = estimator.predict(x_test.values)

----效果评估函数：
import numpy as np
import pandas as pd
from sklearn import metrics
def acc_evaluate(df,error_rate=5,debug_mode=True):
	df['y_abs_error'] = np.abs(df['y_test']-df['y_pred'])
	df['y_test_div'] = df['y_test']
	df.loc[df['y_test']==0,'y_test_div']= 0.00001
	df['y_error_rate'] = (df['y_abs_error']/df['y_test_div'])*100
	df_acc = df[df['y_error_rate']<error_rate]
	pred_accuracy = len(df_acc['y_pred'])/len(df['y_test'])
	if debug_mode:
		y_test,y_pred = df['y_test'],df['y_pred']
		mae = metrics.mean_absolute_error(y_test, y_pred)
		mse = metrics.mean_squared_error(y_test, y_pred)
		rmse = np.sqrt(mse)
		print('pred_accuracy:%0.2f \n MAE:%0.2f \n MSE:%0.2f \n RMSE:%0.2f' %(pred_accuracy,mae,mse,rmse))

---模型持久化：sklearn版pickle
from sklearn.externals import joblib
joblib.dump(estimator, 'estimator.pkl')
estimator = joblib.load('estimator.pkl')

---交叉验证：
from sklearn import cross_validation
scores = cross_validation.cross_val_predict(estimator, x_train,y_train,\
											cv=10,scoring='mean_squared_error/accuracy')
from sklearn import metrics
# 度量准确率
metrics.accuracy_score(y_true, y_pred)
# 度量查准率P
metrics.precision_score(y_true, y_pred)
# 度量召回率R
metrics.recall_score(y_true, y_pred)
# F1 score
metrics.f1_score(y_true, y_pred) # F1Score = 2PR/(P+R)
# 混淆矩阵
metrics.confusion_matrix(y_true, y_pred)
# 其他分类信息
metrics.classification_report(y_true, y_pred)

---特征筛选、支持度评级：
from sklearn.feature_selection import RFE
def feature_selection(estimator,X,y):
	selector = RFE(estimator)
	selector.fit(X, y)
	return pd.DataFrame({'support':selector.support_,'ranking':selector.ranking_},index='')

---降维：
from sklearn.cross_decomposition import PCA
pca_2n = PCA(n_components=2) #降维只保留两个特征序列
x_train = pca_2n.fit_transform(x_train)

---聚类：
from sklearn.cluster import KMeans
kmean = KMeans(n_clusters=2) 
kmean.fit(X)
kmean.predict(X)

============================sklearn===============================
---多项式与线性回归:
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def polynomial_model(degree=1): #degree为多项式阶数
	polynomial_features = PolynomialFeatures(degree=degree,include_bias=False)
	linear_regression = LinearRegression()
	#一个Pipeline可以包含多个处理节点，除了最后一个节点只需fit()方法外，其他节点都必须实现fit()和transform()方法。
	pipeline = Pipeline([('polynomial_features',polynomial_features),\
						('linear_regression',linear_regression)])
	return pipeline

---学习曲线：
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit

cv = ShuffleSplit(n_splits=10,test_size=0.2,random_state=0) #随机从数据集中分配出训练样本和交叉验证样本,计算10次交叉验证数据集的分数
def plot_learning_curve(estimator,title,X,y,ylim=None,cv=None,\
						n_jobs=1,train_sizes=np.linspace(0.1,1.0, 5)):
	plt.title(title)
	if ylim is not None:
		plt.ylim(*ylim)
	plt.xlabel('Training Examples')
	plt.ylabel('Score')
	train_sizes,train_scores,test_scores = learning_curve(estimator, X, y,\
									cv=cv,n_jobs=n_jobs,train_sizes=train_sizes) # key step
	train_scores_mean = np.mean(train_scores,axis=1)
	train_scores_std = np.std(train_scores,axis=1)
	test_scores_mean = np.mean(test_scores,axis=1)
	test_scores_std = np.std(test_scores,axis=1)
	plt.grid()
	plt.fill_between(train_sizes,train_scores_mean-train_scores_std,\
					train_scores_mean+train_scores_std,alpha=0.1,color='r')
	plt.fill_between(train_sizes,test_scores_mean-test_scores_std,\
					test_scores_mean+test_scores_std,alpha=0.1,color='g')
	plt.plot(train_sizes,train_scores_mean,'o-',color='r',label='Training score')
	plt.plot(train_sizes,test_scores_mean,'o-',color='g',label='Cross-Validation score')
	plt.legend(loc='best')
	return plt

==========K近邻算法=========
---K近邻分类：
from sklearn.datasets.samples_generator import make_blobs
centers = [[-2,2],[2,2],[0,4]]
#生成60个在以centers为中心点的周围分布的数据集,数据点分布的松散度为0.6标准差。
X,y=make_blobs(n_samples=60,centers=centers,random_state=0,cluster_std=0.60)
plt.figure(figsize=(6,3),dpi=144)
c = np.array(centers)
plt.scatter(X[:,0],X[:,1],c=y,s=20,cmap='cool')
plt.scatter(c[:,0],c[:,1],s=20,marker='^',c='orange')

from sklearn.neighbors import KNeighborsClassifier
k=5
clf = KNeighborsClassifier(n_neighbors=k)
clf.fit(X,y)
X_sample =np.array([[0,2]])
y_sample = clf.predict(X_sample)
neighbors = clf.kneighbors(X_sample,return_distance=False)#将样本周围距离最近的5个点取出来，取出来的点是训练集里的索引
plt.figure(figsize=(6,3),dpi=200)
plt.scatter(X[:,0],X[:,1],c=y,s=20,cmap='cool')
plt.scatter(c[:,0],c[:,1],s=20,marker='^',c='orange')
plt.scatter(X_sample[:,0],X_sample[:,1],marker='x',c=y_sample,s=100,cmap='cool')
for i in neighbors[0]:
    plt.plot([X[i][0],X_sample[0][0]],[X[i][1],X_sample[0][1]],'k--',linewidth=0.6)

---K近邻回归：
n_dots =40
X=5*np.random.rand(n_dots,1)
y = np.cos(X).ravel()
y+=0.2*np.random.rand(n_dots)-0.1 #添加噪声

from sklearn.neighbors import KNeighborsRegressor
k = 5
knn = KNeighborsRegressor(k)
knn.fit(X,y)
T = np.linspace(0,5,500)[:,np.newaxis]
y_pred = knn.predict(T)
knn.score(X,y)

plt.figure(figsize=(6,3),dpi=200)
plt.scatter(X,y,c='g',label='data',s=20)
plt.plot(T,y_pred,c='k',label='prediction',lw=3)
plt.legend(loc='upper right')
plt.axis('tight')
plt.title('KNeighborsRegressor(k=%i)'%k)
plt.show()

---多个模型比较：
#多次随机分配训练数据集和交叉验证数据集，然后求模型准确性评分的平均值。
#sklearn提供了KFold和cross_val_score方法来实现。
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
kfold = KFold(n_splits=10) #把数据集分为10份，其中1份作为交叉验证数据集来计算模型准确性，剩余9份为训练集
cv_result = cross_val_score(estimator, X,Y,cv=kfold) #cross_val_score总共会计算10次
cv_result.mean()

---特征选择：
sklearn.feature_selection.chi2() #计算卡方值
sklearn.feature_selection.f_classif() #计算F值
from sklearn.feature_selection import SelectKBest
selector = SelectKBest(k=2) #选择相关性最大的两个特征，默认使用F值检验
X_new = selector.fit_transform(X,Y) #重新选择的特征

=========线性回归算法============
#准备数据-波士顿房价数据
from sklearn.datasets import load_boston
boston = load_boston()
X = boston.data
y = boston.target
#模型训练
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import time
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=3)
model = LinearRegression(normalize=True) #normalize=Ture数据归一化
start = time.clock()
model.fit(X_train,y_train)
train_score = model.score(X_train,y_train)
cv_score = model.score(X_test,y_test)
print('elaspe:%.6f;\ntrain_score:%0.6f;\ncv_score:%.6f'%(time.clock()-start,train_score,cv_score))
#模型优化-欠拟合-增加模型复杂度-创建多项式模型函数
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
def polynomial_model(degree=1):
    polynomial_features = PolynomialFeatures(degree=degree,include_bias=False)
    linear_regression = LinearRegression(normalize=True)
    pipeline = Pipeline([('polynomial_features',polynomial_features),('linear_regression',linear_regression)])
    return pipeline
degrees = [1,2,3]
results = []
for deg in degrees:
    model = polynomial_model(deg)
    start = time.clock()
    model.fit(X_train,y_train)
    train_score = model.score(X_train,y_train)
    cv_score = model.score(X_test,y_test)
    mse = mean_squared_error(y_train,model.predict(X_train))
    results.append({'degree':deg,'elapse':time.clock()-start,'train_score':train_score,'cv_score':cv_score,'mse':mse})
for r in results:
    print('degree:%i;------\n  elaspe:%.6f;\n  train_score:%0.6f;\n  cv_score:%.6f;\n  mse:%.6f'%\
          (r['degree'],r['elapse'],r['train_score'],r['cv_score'],r['mse']))
#画学习曲线
from matplotlib.figure import SubplotParams
from sklearn.model_selection import ShuffleSplit
cv = ShuffleSplit(n_splits=10,test_size=0.2,random_state=0)
plt.figure(figsize=(12,2.5),dpi=200,subplotpars=SubplotParams(hspace=0.3))
for i in range(len(degrees)):
    plt.subplot(1,3,i+1)
    plot_learning_curve(polynomial_model(degrees[i]),'Learning Curve(degree=%i)'%degrees[i],X,y,ylim=(0.01,1.01),cv=cv)
plt.show()

=====逻辑回归算法======






