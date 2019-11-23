'''=================DataFrame+SparkML Pipeline：企业财务困境预测===============
 * 一、运行环境
 *     1.ubuntu-18.04
 *     2.hadoop-3.0.1 + spark-2.3.1 + hive-3.0.0
 *     3.jdk1.8 + python3.6
       4.IDE：notebook+eclipse
 * 二、数据来源
 *    Kaggle:包含3672个样本，共83个样本特征。
 * 三、项目简介
 *    从数据来源处得知，企业财务困境值大于-0.5即表示企业运行健康，否则企业陷入财务困境而无法继续经营。
 *    该问题既可以视为分类问题，也可以视为回归问题，因此分别采用了决策树、随机森林二元分类和决策树回归、
      GBT回归四个算法对企业财务困境进行预测。
 * 四、执行过程如下
 '''
#  ============================1.创建spark环境=================================
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkConf

global train_df,test_df

def CreateSparkSession():
    sparkConf = SparkConf().setAppName('Finacial Distress Prediction')  \
            .set('spark.ui.showConsoleProgress','false') 
    sc = SparkContext(conf=sparkConf)
    print('当前环境为：master='+sc.master)
    SetLogger(sc) 
    SetPath(sc)
    spark = SparkSession.builder.config(conf=sparkConf).getOrCreate()
    return spark
 
def SetLogger(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)
    logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)

def SetPath(sc):
    global Path
    if sc.master[0:5]=="local":
        Path = "file:/home/hadoop/eclipse-workspace/FinancialDistressPre/"
    else:
        Path = "hdfs://ubuntu:9000/sparkproject/FinancialDistressPre/"
    return Path

# ==============================2.导入数据并整理拆分=================================
from pyspark.sql.functions import col
# import pyspark.sql.types

def ETL_Data(Path,spark):
    raw_df = spark.read.format("csv") \
                  .option("header","true") \
                  .option("delimiter",",") \
                  .load(Path+"data/FinacialDistress.csv")
    rawDF = raw_df.select(['Company','Time'] + [col(c).cast('double').alias(c) \
                                                for c in raw_df.columns[2:]])
    rawDF = rawDF.na.fill(0) #若有缺失值则为‘?’替换为0
    df = rawDF.withColumn('Financial Distress01', \
                          (rawDF['Financial Distress']>-0.5).cast('int')) #根据取值生成分类变量
    print("数据集共有%s个样本，%s列，%s个特征" % (df.count(),len(df.first()),len(df.first())-4))
    print("数据结构（部分）如下：")
    df.select('Company','Time','Financial Distress','x1','x2').show(10)
    train_df,test_df = df.randomSplit([0.7,0.3])
    return train_df,test_df

# ==========================3.进一步处理特征，生成Features Vector====================
''' 特征处理Pipeline：StringIndexer => OneHotEncoder => VectorAssembler
        a.利用StringIndexer将文字分类特征转换为数值分类特征
        b.利用OneHotEncoder将数值分类特征转换为Vector如(0,0,0,1,0,1,0,0)
        c.使用 VectorAssembler 将所有特征集成为一个特征Vector
        
from pyspark.ml.feature import StringIndexer,OneHotEncoder

-------StringIndexer---------

# StringIndexer是一个Estimator
category = StringIndexer(inputCol='inputStr',outputCOl='outputNum') 

# 调用fit方法后生成一个Transformer
categoryTransformer = category.fit(df) 
categoryTransformer.labels即为分类字符串

# 将Transformer应用到train_df和test_df
trainDF = categoryTransformer.transform(train_df)
testDF = categoryTransformer.transform(test_df)

--------OneHotEncoder--------
encoder = OneHotEncoder(inputCol='outputNum',outputCol='outputVec',dropLast=False)
train_DF = encoder.transform(trainDF)
testDF = encoder.transform(testDF)
'''
#本数据集合没有字符串分类变量，可直接对数据特征进行归集
from pyspark.ml.feature import VectorAssembler

def vecAssembler():
    assemblers = train_df.columns[3:-1]
    vecAssembler = VectorAssembler(inputCols=assemblers,outputCol= 'Features')
    return vecAssembler
# ===========================4.建立sparkML Pipeline进行模型训练与预测========================
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml.regression import GBTRegressor
from pyspark.ml.tuning import ParamGridBuilder,TrainValidationSplit,CrossValidator
from pyspark.ml.evaluation import BinaryClassificationEvaluator,RegressionEvaluator
from pyspark.ml import Pipeline

# 定义算法字典
algo_dict = {
             'dtc':DecisionTreeClassifier,
             'rfc':RandomForestClassifier,
             'dtr':DecisionTreeRegressor,
             'gbtr':GBTRegressor
             }
# 定义默认训练参数列表
maxDepth = [5,10,15,20]
maxBins = [10,15,20,25]
numTrees = [10,20,30]
impurity = ["gini","entropy"]
maxIter = [10,20]

# 定义分类学习流程
def Classifier(algorithm,maxDepth=maxDepth,maxBins=maxBins,numTrees=numTrees):
    algo = algo_dict[str(algorithm)]
    model = algo(labelCol='Financial Distress01',featuresCol='Features')
    if algorithm == 'dtc':
        paramGrid = ParamGridBuilder().addGrid(model.impurity,impurity) \
                                     .addGrid(model.maxDepth,maxDepth) \
                                     .addGrid(model.maxBins,maxBins) \
                                     .build() 
    elif algorithm == 'rfc':
        paramGrid = ParamGridBuilder().addGrid(model.impurity,impurity) \
                                      .addGrid(model.maxDepth,maxDepth) \
                                      .addGrid(model.maxBins,maxBins) \
                                      .addGrid(model.numTrees,numTrees) \
                                      .build()                            
    evaluator = BinaryClassificationEvaluator(rawPredictionCol='rawPrediction', \
                                              labelCol='Financial Distress01', \
                                              metricName='areaUnderROC')           
    print("\n-------------运用TrainValidationSplit寻找最优模型------------------")
    tvs_pipeline(algorithm,model,paramGrid,evaluator)
    print("\n-------------运用CrossValidator寻找最优模型------------------")
    cv_pipeline(algorithm,model,paramGrid,evaluator)

# 定义回归分析流程
def Regressor(algorithm,maxDepth=maxDepth,maxBins=maxBins,maxIter=maxIter):
    algo = algo_dict[str(algorithm)]
    model = algo(labelCol='Financial Distress',featuresCol='Features')
    if algorithm == 'dtr':
        paramGrid = ParamGridBuilder().addGrid(model.maxDepth,maxDepth) \
                                      .addGrid(model.maxBins,maxBins) \
                                      .build() 
    elif algorithm == 'gbtr':
        paramGrid = ParamGridBuilder().addGrid(model.maxDepth,maxDepth) \
                                      .addGrid(model.maxBins,maxBins) \
                                      .addGrid(model.maxIter,maxIter) \
                                      .build()                            
    evaluator = RegressionEvaluator(labelCol='Financial Distress', \
                                        predictionCol = 'prediction', \
                                        metricName='rmse')        
    print("\n-------------运用TrainValidationSplit寻找最优模型------------------")
    tvs_pipeline(algorithm,model,paramGrid,evaluator)
    print("\n-------------运用CrossValidator寻找最优模型------------------------")
    cv_pipeline(algorithm,model,paramGrid,evaluator)    

# 定义训练验证和结果评估流程
def tvs_pipeline(algorithm,model,paramGrid,evaluator):
    TVS = TrainValidationSplit(estimator = model,evaluator=evaluator, \
                                estimatorParamMaps = paramGrid,trainRatio=0.7)
    TVS_pipeline = Pipeline(stages=[vecAssembler,TVS])
    TVS_models = TVS_pipeline.fit(train_df)
    TVS_predict = TVS_models.transform(test_df)
    bestModel = TVS_models.stages[1].bestModel
    if algorithm == 'dtc' or algorithm=='dtr':
        print('\n最优模型深度为%i，含有%i个节点' % (bestModel.depth,bestModel.numNodes))
    elif algorithm == 'rfc' or algorithm == 'gbtr':
        print('\n最优模型包含%i个树，共%i个节点' % (bestModel.getNumTrees,bestModel.totalNumNodes))
    print('预测结果（部分）为：')
    TVS_predict.select('Company','Time','Features','Financial Distress',\
                       'Financial Distress01','prediction').show(10)
    eva = evaluator.evaluate(TVS_predict)
    if algorithm == 'dtc' or algorithm == 'rfc':
        print("预测准确率auc为%.2f%%" % (eva*100))                  
    elif algorithm == 'dtr' or algorithm =='gbtr':
        evaluator_r2 = RegressionEvaluator(labelCol='Financial Distress', \
                                        predictionCol = 'prediction', \
                                        metricName='r2')  
        r2 = evaluator_r2.evaluate(TVS_predict)
        print("预测误差rmse为%.4f,回归拟合r2为%.4f" % (eva,r2))
 
# 定义交叉验证和结果评估流程      
def cv_pipeline(algorithm,model,paramGrid,evaluator):
    CV = CrossValidator(estimator = model, evaluator = evaluator,\
                    estimatorParamMaps = paramGrid,numFolds=3)
    CV_pipeline = Pipeline(stages=[vecAssembler,CV])
    CV_models = CV_pipeline.fit(train_df)
    CV_predict = CV_models.transform(test_df)
    bestModel_ = CV_models.stages[1].bestModel
    if algorithm == 'dtc' or algorithm=='dtr':
        print('\n最优模型深度为%i，含有%i个节点' % (bestModel_.depth,bestModel_.numNodes))
    elif algorithm == 'rfc' or algorithm == 'gbtr':
        print('\n最优模型包含%i个树，共%i个节点' % (bestModel_.getNumTrees,bestModel_.totalNumNodes))
    print('预测结果（部分）为：')
    CV_predict.select('Company','Time','Features','Financial Distress',\
                       'Financial Distress01','prediction').show(10)
    eva = evaluator.evaluate(CV_predict)
    if algorithm == 'dtc' or algorithm == 'rfc':
        print("预测准确率auc为%.2f%%" % (eva*100))                  
    elif algorithm == 'dtr' or algorithm =='gbtr':
        evaluator_r2 = RegressionEvaluator(labelCol='Financial Distress', \
                                        predictionCol = 'prediction', \
                                        metricName='r2')  
        r2 = evaluator_r2.evaluate(CV_predict)
        print("预测误差rmse为%.4f,回归拟合r2为%.4f" % (eva,r2))
 

# 定义主程序
if __name__=="__main__":
    print("创建spark环境")
    spark = CreateSparkSession()
    print("当前数据文件读取路径为:\n %s" % Path )
    print("开始读取数据，整理后拆分为训练集和测试集")
    train_df,test_df = ETL_Data(Path,spark)
    vecAssembler = vecAssembler()
    print("数据整理完毕，开始进行训练和预测")
    print("\n========================开始执行决策树二元分类算法=============================" + \
          "\n训练参数为:" + \
          "\n\t maxDepth = [5,10,15,20]" + \
          "\n\t maxBins = [10,15,20,25]" + \
          "\n\t impurity = ['gini','entropy']")
    Classifier(algorithm="dtc")
    print("\n========================开始执行随机森林二元分类算法===========================" + \
          "\n训练参数为:" + \
          "\n\t maxDepth = [5,10,15,20]" + \
          "\n\t maxBins = [10,15,20,25]" + \
          "\n\t numTrees = [10,20,30]" + \
          "\n\t impurity = ['gini','entropy']")
    Classifier(algorithm='rfc')
    print("\n========================开始执行决策树回归算法================================" + \
          "\n训练参数为:" + \
          "\n\t maxDepth = [5,10,15,20]" + \
          "\n\t maxBins = [10,15,20,25]")
    Regressor(algorithm='dtr')
    print("\n========================开始执行梯度提升决策树算法=============================" + \
          "\n训练参数为:" + \
          "\n\t maxDepth = [5,10,15,20]" + \
          "\n\t maxBins = [10,15,20,25]" + \
          "\n\t maxIter = [10,20]") 
    Regressor(algorithm='gbtr')
    print("========================企业财务困境预测结束==================================")
    
# # ==============================决策树二元分类DecisionTreeClassifier=======================
# 
# def dtClassifier():
#     dtClassifier = DecisionTreeClassifier(labelCol='Financial Distress01',\
#                                         featuresCol='Features')
#     paramGrid = ParamGridBuilder().addGrid(dtClassifier.impurity,["gini","entropy"]) \
#                 .addGrid(dtClassifier.maxDepth,[5,10,15,20]) \
#                 .addGrid(dtClassifier.maxBins,[10,15,20,25]).build()
#     evaluator = BinaryClassificationEvaluator( \
#                     rawPredictionCol='rawPrediction', \  
#                     labelCol='Financial Distress01', \
#                     metricName='areaUnderROC')           
#     dtTVS = TrainValidationSplit(estimator = dtClassifier,evaluator=evaluator,
#                                estimatorParamMaps = paramGrid,trainRatio=0.7)
#     dtTVS_pipeline = Pipeline(stages=[vecAssembler,dtTVS])
#     dtTVS_models = dtTVS_pipeline.fit(train_df)
#     dtTVS_predict = dtTVS_models.transform(test_df)
#     auc = evaluator.evaluate(dtTVS_predict)
#     
#     dtCV = CrossValidator(estimator=dtClassifier,evaluator=evaluator,
#                     estimatorParamMaps = paramGrid,numFolds=3)
#     dtCV_pipeline = Pipeline(stages=[vecAssembler,dtCV])
#     dtCV_models = dtCV_pipeline.fit(train_df)
#     dtCV_predict = dtCV_models.transform(test_df)
#     auc_ = evaluator.evaluate(dtCV_predict)
#     return classifier
# # ==============================随机森林二元分类RandomForestClassifier=======================
# def rfClassifier():
#     rfClassifier = RandomForestClassifier(labelCol = 'Financial Distress01',\
#                                           featuresCol='Features')
#     paramGrid = ParamGridBuilder().addGrid(rfClassifier.impurity,["gini","entropy"]) \
#                 .addGrid(rfClassifier.maxDepth,[5,10,15,20]) \
#                 .addGrid(rfClassifier.maxBins,[10,15,20,25]) \
#                 .addGrid(rfClassifier.numTrees,[10,20,30]).build()
#     evaluator = BinaryClassificationEvaluator( \
#                     rawPredictionCol='rawPrediction', \
#                     labelCol='Financial Distress01', \
#                     metricName='areaUnderROC') 
#     
#     rfTVS = TrainValidationSplit(estimator = rfClassifier,evaluator=evaluator,\
#                                  estimatorParamMaps = paramGrid,trainRatio=0.7)
#     rfTVS_pipeline  = Pipeline(stages=[vecAssembler,rfTVS])
#     rfTVS_models = rfTVS_pipeline.fit(train_df)
#     rfTVS_predict = rfTVS_models.transform(test_df)
#     auc = evaluator.evaluate(rfTVS_predict)
#     
#     rfCV = CrossValidator(estimator=rfClassifier,evaluator=evaluator,
#                     estimatorParamMaps = paramGrid,numFolds=3)
# 
#     rfCV_pipeline = Pipeline(stages=[vecAssembler,rfCV])
#     rfCV_models = rfCV_pipeline.fit(train_df)
#     rfCV_predict = rfCV_models.transform(test_df)
#     auc = evaluator.evaluate(rfCV_predict)
#     return classifier
# 
# # ==============================决策树回归DecisionTreeRegressor=======================
# 
# def dtReg():
#     dtReg = DecisionTreeRegressor(labelCol='Financial Distress',featuresCol='Features')
# 
#     reg_evaluator = RegressionEvaluator(labelCol='Financial Distress', \
#                                         predictionCol = 'prediction', \
#                                         metricName='rmse')
#     paramGrid = ParamGridBuilder().addGrid(dtReg.maxDepth,[5,10,15,20]) \
#                               .addGrid(dtReg.maxBins,[10,15,20,25]).build()
#     dtRegTVS = TrainValidationSplit(estimator = dtReg,evaluator=reg_evaluator,
#                                estimatorParamMaps = paramGrid,trainRatio=0.7)
#     dtRegTVS_pipeline  = Pipeline(stages=[vecAssembler,dtRegTVS])
#     dtRegTVS_models = dtRegTVS_pipeline.fit(train_df)
#     dtRegTVS_predict = dtRegTVS_models.transform(test_df)
#     rmse = reg_evaluator.evaluate(dtRegTVS_predict)
#     
#     dtRegCV = CrossValidator(estimator=dtReg,evaluator=reg_evaluator,
#                     estimatorParamMaps = paramGrid,numFolds=3)
# 
#     dtRegCV_pipeline = Pipeline(stages=[vecAssembler,dtRegCV])
#     dtRegCV_models = dtRegCV_pipeline.fit(train_df)
#     dtRegCV_predict = dtRegCV_models.transform(test_df)
#     rmse = reg_evaluator.evaluate(dtRegCV_predict)
# 
# # ==============================梯度提升决策树回归GBTRegressor=======================
# def gbtReg():
#     gbtReg = GBTRegressor(labelCol='Financial Distress',featuresCol='Features')
#     reg_evaluator = RegressionEvaluator(labelCol='Financial Distress', \
#                                         predictionCol = 'prediction', \
#                                         metricName='rmse')
#     paramGrid = ParamGridBuilder().addGrid(gbtReg.maxDepth,[5,10,15,20]) \
#                               .addGrid(gbtReg.maxBins,[10,15,20,25])  \
#                               .addGrid(gbtReg.maxIter,[10,30]).build()
# 
#     gbtRegTVS = TrainValidationSplit(estimator = gbtReg,evaluator=reg_evaluator,
#                                estimatorParamMaps = paramGrid,trainRatio=0.7)
#     gbtRegTVS_pipeline  = Pipeline(stages=[vecAssembler,gbtRegTVS])
#     gbtRegTVS_models = gbtRegTVS_pipeline.fit(train_df)
#     gbtRegTVS_predict = gbtRegTVS_models.transform(test_df)
#     rmse = reg_evaluator.evaluate(gbtRegTVS_predict)
#     
#     gbtRegCV = CrossValidator(estimator=gbtReg,evaluator=reg_evaluator,
#                     estimatorParamMaps = paramGrid,numFolds=3)
# 
#     gbtRegCV_pipeline = Pipeline(stages=[vecAssembler,gbtRegCV])
#     gbtRegCV_models = gbtRegCV_pipeline.fit(train_df)
#     gbtRegCV_predict = gbtRegCV_models.transform(test_df)
#     rmse = reg_evaluator.evaluate(gbtRegCV_predict)
    
    

