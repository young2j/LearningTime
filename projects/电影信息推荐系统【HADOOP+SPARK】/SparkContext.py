from pyspark import SparkContext
from pyspark import SparkConf

def CreateSparkContext():
    '''
    spark配置：
    1.显示在spark或 hadoop-yarn UI界面的App名称
    2.设置不显示spark执行进度以免界面太乱
    '''
    sparkConf = SparkConf().setAppName('FilmRecommend')  \
            .set('spark.ui.showConsoleProgress','false') 
    sc = SparkContext(conf=sparkConf)
    print('master='+sc.master)
    SetLogger(sc) #设置不要显示太多信息
    SetPath(sc) # 设置文件读取路径
    return sc

def SetLogger(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)
    logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)

def SetPath(sc):
    global Path
    if sc.master[0:5]=="local":
        Path = "file:/home/hadoop/eclipse-workspace/FilmRecommend/"
    else:
        Path = "hdfs://ubuntu:9000/sparkproject/FilmRecommend/"

if __name__=='__main__':
    print('开始执行 FilmRecommend')
    sc = CreateSparkContext()
    
    print('开始读取数据文件...')
    textFile = sc.textFile(Path+"data/words.txt")
    print("该数据文件共%s行" % textFile.count())
    
    countsRDD = textFile.flatMap(lambda line:line.split(' ')) \
                .map(lambda x:(x,1)).reduceByKey(lambda x,y:x+y)
    print('文字统计共%s项数据' % countsRDD.count())
    
    print('保存至文本文件output')
    try:
        countsRDD.saveAsTextFile(Path+'data/output')
    except Exception as e:
        print('输出目录已存在，请先删除原有目录')
    sc.stop()        
        
        
        
        
        
        
        