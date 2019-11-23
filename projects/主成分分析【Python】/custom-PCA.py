# 数据去均值后协方差矩阵不变,特征值与特征向量也不变
# 数据标准化后的协方差矩阵等于相关系数矩阵,等于原始数据的相关系数矩阵
#机器学习采用的是规范化后的协方差矩阵

# numpy.std() 求标准差的时候默认是除以 n 的，即是有偏的，np.std无偏样本标准差方式为 ddof = 1； 
# pandas.std() 默认是除以n-1 的，即是无偏的，如果想和numpy.std() 一样有偏，需要加上参数ddof=0 ，即pandas.std(ddof=0) 

#用规范化的数据进行奇异值分解和特征分解,奇异值s的平方等于特征值,特征向量均相同,即<1><2><3>的特征向量相同,
# 但<1><2>的特征值是<3>的m=nobs-1倍,即 λ1,2/m = λ3,相差（样本数-1）倍
mat = np.array([[32,45,43],[34,56,3],[54,2,4],[43,9,65]])
mat_norm = mat-np.mean(mat,axis=0)
# mat_norm = (mat-np.mean(mat,axis=0))/np.std(mat,axis=0,ddof=1)#<1>
u,s,v=linalg.svd(mat_norm) #<1> #奇异值结果是按从大到小排序的
eva,eve=linalg.eig(mat_norm.T.dot(mat_norm)) #<2>
coveva,coveve=linalg.eig(np.cov(mat.T)) #<3>
# coveva,coveve=linalg.eig(np.corrcoef(mat.T)) #<3>


import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy import linalg
import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA


# debt = pd.read_excel("C:\\Users\\Administrator\\Desktop\\梁\\世纪华通偿债能力.xls",header=0)
debt = pd.ExcelFile("C:\\Users\\Administrator\\Desktop\\梁\\世纪华通偿债能力.xls").parse('Sheet1')
debt = debt.set_index(['截止日期'])
debt = debt.fillna(method='bfill')


class pca(object):                                                                            
	def __init__(self,data, k=None,scale_method='0_1standardized'):
		self.data=data
		self.k=k
		self.scale_method = scale_method
		self.data_scale = self.data_normalize()
		self.cov_mat = self.covar_mat()
		self.eigVals = self.calc_eigen()['Eigenvalues']
		self.eigVals_sort = self.eigVals.sort_values(ascending=False) #特征值降序排列
		self.eigVects = self.calc_eigen()['Eigenvectors']
		self.variance_ratio = self.eigvals_and_ratio()['Eigenvalues of the Covariance Matrix']['Proportion%']
		self.cum_variance_ratio = self.eigvals_and_ratio()['Eigenvalues of the Covariance Matrix']['Cumulative%']
		self.EigVects_K = self.eigvects_k()
	def __new__(cls,data,*args,**kwargs):
		if is not  isinstance(data,DataFrame):
			raise TypeError('The type of input data must be pandas DataFrame')
		return object.__new__(cls)
	def data_normalize(self):
		if self.scale_method=='0_1standardized':
			data_scale = (self.data-self.data.mean())/self.data.std() #标准化(教科书)corr()不变
		elif self.scale_method=='mean_divided':
			data_scale = self.data/self.data.mean() #均值法(文献)-corr()不变
		elif self.scale_method=='centralized':
			data_scale = self.data-self.data.mean() #中心化cov()/corr()不变 maxmin corr()不变
		else:
			raise ValueError("The parameter of 'scale_method' is not correct")
		return data_scale
	def corr_mat(self):
		corr_mat = self.data_scale.corr()
		corr_mat.columns = [['Correlation Matrix']*len(corr_mat.columns),list(corr_mat.columns)]
		return corr_mat
	def covar_mat(self): 
		cov_mat = self.data_scale.cov() #协方差矩阵(标准化时也为相关系数矩阵)
		cov_mat.columns = [['Correlation Matrix']*len(cov_mat.columns),list(cov_mat.columns)]
		return cov_mat	
	def calc_eigen(self):
		eigVals,eigVects = linalg.eig(self.cov_mat) #计算特征值和特征向量
		eigVects = pd.DataFrame(np.around(eigVects.T,4),columns=['Eigenvectors']*eigVects.shape[0])
		eigVals = [i.real if i.imag==0.0 else i for i in np.around(eigVals,4)]
		eigVals = pd.Series(eigVals,name='Eigenvalues')
		eig = pd.concat([eigVals,eigVects],axis=1)
		return eig
	def eigvals_and_ratio(self):
		eigVals_variance_ratio = self.eigVals_sort/self.eigVals.sum() #方差贡献率
		cum_variance_ratio = self.eigVals_sort.cumsum()/self.eigVals.sum() #累积方差贡献率
		eig_and_ratio = pd.DataFrame({'Eigenvalues':self.eigVals_sort,'Difference':-self.eigVals_sort.diff(),
					'Proportion%':eigVals_variance_ratio*100,'Cumulative%':cum_variance_ratio*100},columns=['Eigenvalues','Difference','Proportion%','Cumulative%'])
		eig_and_ratio.columns = [['Eigenvalues of the Covariance Matrix']*len(eig_and_ratio.columns),list(eig_and_ratio.columns)]
		eig_and_ratio = eig_and_ratio.fillna(' ')
		return eig_and_ratio
	def eigvects_k(self): 
		if self.k==None:
			self.k = (self.cum_variance_ratio<70.0).sum()+1
		elif type(self.k)==float:
			self.k = (self.cum_variance_ratio<self.k*100).sum()+1
		eigValInd = self.eigVals_sort.index #特征值降序索引号
		eigValInd_K = eigValInd[:self.k]   #保留最大的前K个特征值
		EigVects_K = self.eigVects.iloc[eigValInd_K,:]  #最大的前K个特征值对应的特征向量
		return EigVects_K
	def prin_score_equation(self):
		prin_equation = []
		for i in range(self.k):
			equation = 'Y'+str(i+1)+'='+ (pd.Series(['%+f'%(round(z[0],4))+'*'+z[1] for z in zip(self.EigVects_K.iloc[i,:],self.data_scale.columns)]).str.cat(sep=''))
			prin_equation.append(equation)
		prin_score = np.dot(self.data_scale,self.EigVects_K.T) #将数据转换到低维新空间,即主成分得分
		Y =  ['Y'+str(i+1) for i in range(self.k)]
		prin_score = pd.DataFrame(prin_score,columns=Y,index=self.data_scale.index)
		compre_score = np.dot(prin_score.values,np.vstack(self.variance_ratio[:self.k].values))
		compre_score = pd.DataFrame(compre_score,index=self.data_scale.index,columns=['comprehensive_score'])
		return prin_equation,prin_score,compre_score
	@property
	def screeplot(self):
		plt.plot(np.arange(1,len(self.data.columns)+1),self.eigVals,marker='o',linestyle='-')
		plt.xlabel('The Number of Principal Component')
		plt.ylabel('Eigenvalues')
		plt.title('Screeplot')
		plt.xticks(np.arange(len(self.data.columns)+1))
		return plt.show()
	@property
	def n_components(self):
		return self.k