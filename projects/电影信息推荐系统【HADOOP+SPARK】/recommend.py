'''=================SparkRDD+SparkML:基于ALS算法的电影推荐引擎===============
 * 一、运行环境
 *     1.ubuntu-18.04
 *     2.hadoop-3.0.1 + spark-2.3.1
 *     3.jdk1.8 + python3.6
       4.IDE：notebook+eclipse
 * 二、数据来源
 *    开源数据：从https://grouplens.org/datasets/movielens/上下载
 * 三、项目简介
 *   通过用户对电影的历史评分数据，利用sparkML的协同过滤算法和sparkRDD编程创建基于人和基于物的推荐引擎
 * 四、执行过程如下
 '''
 
from pyspark.mllib.recommendation import MatrixFactorizationModel, ALS
import sys

from SparkContext import CreateSparkContext

def SetPath(sc):
    if sc.master[0:5]=="local":
        Path = "file:/home/hadoop/eclipse-workspace/FilmRecommend/"
    else:
        Path = "hdfs://ubuntu:9000/sparkproject/FilmRecommend/"
    return Path

def PrepareData(sc):
    # ratings.csv
    print('读取评分数据文件ratings.csv')
    ratData = sc.textFile(Path+'/data/ml-latest-small/ratings.csv')
    print('评分数据共有%i条记录' % (ratData.count()-1))
    ratRDD = ratData.map(lambda line: line.split('\t')) \
                    .map(lambda x:(x[0].split(',')))  \
                    .map(lambda y:(y[0],y[1],y[2])) 
#     print('整理后的数据格式为',ratRDD.take(5))
    header = ratRDD.first()
    ratRDD = ratRDD.filter(lambda x:x!=header)

    # 数据简单统计
    numUsers = ratRDD.map(lambda x:x[0]).distinct().count()
    numMovies = ratRDD.map(lambda x:x[1]).distinct().count()
    print('参与评价的总人数为：',numUsers,'\n被评价的总电影数为：',numMovies)
    
    #movies.csv
    print('\n读取电影数据文件movies.csv,映射为字典{id:name}')
    movData = sc.textFile(Path+'data/ml-latest-small/movies.csv')
    print('共有%i部电影' % movData.count())
    movRDD = movData.map(lambda line:line.split('\t')) \
                .map(lambda x :x[0].split(','))  \
                .map(lambda y:(y[0],y[1]))
    header_ = movRDD.first()
    movRDD = movRDD.filter(lambda z: z!=header_).collectAsMap()
    return ratRDD,movRDD

def SaveModels(sc):
    try:
        model.save(sc,Path+'ALSmodel')
        print('Model存储在%s下，名为ALSmodel' % Path)
    except Exception:
        print('Model在%s下已存在，请删除再保存' % Path)

def LoadModel(sc):
    try:
        model = MatrixFactorizationModel.load(sc,Path+'ALSmodel')
        print('载入ALS模型成功')
    except Exception:
        print('找不到ASLmodel,请确保是否进行了训练')
    return model

def Recommend(model):
    if sys.argv[1] =="U":
        movies = model.recommendProducts(int(sys.argv[2]),10)
        for m in movies:
            print("向用户%s推荐: %s\t推荐评分: %.2f" % \
                  (m[0],movRDD[str(m[1])],m[2]))
    elif sys.argv[1] =="M":
        movieId = sys.argv[2]
        users = model.recommendUsers(int(movieId),10)
        print("把电影%s(id:%s)推荐给以下用户:" % \
              (movRDD[str(movieId)],movieId))
        for u in users:
            print("用户%s\t推荐评分: %.2f" % (u[0],u[2]))

if __name__=='__main__':
    if len(sys.argv)!=3: #程序文件名、两个参数
        print('请输入2个参数')
        exit(-1)
    sc = CreateSparkContext()
    Path = SetPath(sc)
    print('==========准备数据==========')
    ratRDD,movRDD = PrepareData(sc)
    print('==========模型训练==========')
    print('开始训练ALS推荐算法，参数为rank=5，iterations=20，lambda_=0.1')
    model = ALS.train(ratRDD,10,10,0.1)
    print('==========模型存储==========')
    SaveModels(sc)
    print('==========载入模型==========')
    model=LoadModel(sc)
    print('==========进行推荐==========')
    Recommend(model)
