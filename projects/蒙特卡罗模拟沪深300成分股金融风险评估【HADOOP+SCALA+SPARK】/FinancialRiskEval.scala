/*=================基于蒙特卡罗模拟沪深300成份股金融风险评价===============
 * 一、运行环境
 * 	1.ubuntu-18.04
 * 	2.spark-2.3.1
 * 	3.jdk1.8 + scala-2.12.3
 * 	4.python3.6
 *  5.IDE:spark-shell + eclipse
 * 二、数据来源
 * 	利用python脚本从Tushare上下载所需数据，包含322572个样本：
 *  1.沪深300成分股日交易数据
 *  2.市场因素：上证综指、深证成指、国债指数日交易数据
 *  3.时间跨度五年：2013-7-31至2018-7-31
 * 三、项目简介
 *  通过蒙特卡罗模拟对市场因子进行随机采样，进而模拟出市场因子的各种变化，
 *  然后建立对沪深300股票收益的线性回归模型，最后计算出风险价值VaR与条件
 *  风险价值CVaR，对投资风险进行评价。
 * 四、执行过程如下
 * */
//==================1.用python脚本下载tushare的股票数据================

//python tushare_data.py

//准备Spark环境
//import org.apache.spark.sql.SparkSession
//val spark = SparkSession.builder().getOrCreate()
//import spark.implicits._

//==================2.读取并处理下载的tushare的股票数据================
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.io.File

def readTushare(file:File):Array[(LocalDate,Double)]={
  val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")
  val lines = scala.io.Source.fromFile(file).getLines().toSeq
  lines.tail.map { line =>
    val cols = line.split(",")
    val date = LocalDate.parse(cols(1),formatter)
    val close = cols(3).toDouble
    (date,close)
  }.toArray
}
//val dir = "/home/hadoop/eclipse-workspace/FinacialRiskEval/data/"
val dir = "F:/Java/eclipse/workspace/FinancialRiskEval/data/"
val hs300Dir = new File(dir + "hs300/")
val hs300Files = hs300Dir.listFiles()
val hs300Stocks = hs300Files.iterator.map(readTushare)

val hsindexDir = new File(dir + "hsindex/")
val hsindexFiles = hsindexDir.listFiles()
val hsIndex = hsindexFiles.iterator.map(readTushare)

//==================3.将股票数据时期统一为2013-7-31至2018-7-31日==========
val start = LocalDate.of(2013,7,31)
val end = LocalDate.of(2018,7,31)

def unionPeriod(data:Array[(LocalDate,Double)],
  start:LocalDate,end:LocalDate):Array[(LocalDate,Double)] = {
    var trimmed = data.dropWhile(_._1.isBefore(start)).takeWhile(x => 
      x._1.isBefore(end) || x._1.isEqual(end))
    if (trimmed.head._1 !=start){
      trimmed = Array((start,trimmed.head._2)) ++ trimmed
    }
    if (trimmed.last._1 != end){
      trimmed = trimmed ++ Array((end,trimmed.last._2))
    }
    trimmed
  }

//==================对缺失值进行填补======================================
import scala.collection.mutable.ArrayBuffer
import org.joda.time.{Days,DateTime}

//def fillValue(data:Array[(LocalDate,Double)],
//    start:LocalDate,end:LocalDate):Array[(LocalDate,Double)] = {
//  var cur = data.map {x =>
//    val dateTime = DateTime.parse(x._1.toString)
//    (dateTime,x._2)
//  }.toArray
//  val filled = new ArrayBuffer[(DateTime,Double)]()
//  var curDate = DateTime.parse(start.toString)
//  val End = DateTime.parse(end.toString)
//  while (curDate isBefore End) {
//    if (cur.tail.nonEmpty && cur.tail.head._1 == curDate) {
//      cur = cur.tail
//    }
//  filled += ((curDate,cur.head._2))
//  curDate = curDate.plusDays(1)
//  if (curDate.dayOfWeek().get > 5) {
//    curDate = curDate.plusDays(2)
//    }
//  }
//  val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")
//  filled.map { x=>
//    val localDate = LocalDate.parse(x._1.toString,formatter)
//    (localDate,x._2)
//  }.toArray
//}
def fillValue(data:Array[(LocalDate,Double)],
    start:LocalDate,end:LocalDate):Array[(LocalDate,Double)] = {
  var cur = data
  val filled = new ArrayBuffer[(LocalDate,Double)]()
  var curDate = start
  while (curDate isBefore end) {
    if (cur.tail.nonEmpty && cur.tail.head._1 == curDate) {
      cur = cur.tail
    }
  filled += ((curDate,cur.head._2))
  curDate = curDate.plusDays(1)
  if (curDate.getDayOfWeek().getValue() > 5) {
    curDate = curDate.plusDays(2)
    }
  }
  filled.toArray
}

val stocks = hs300Stocks.map(unionPeriod(_,start,end)).map(fillValue(_,start,end))
val factors = hsIndex.map(unionPeriod(_,start,end)).map(fillValue(_,start,end))

//==================4.以两周为时间窗口计算股票收益==============================
def twoWeekReturns(data:Array[(LocalDate,Double)]):Array[Double] = {
  val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")
  val Data = data.map { x=>
      val localDate = LocalDate.parse(x._1.toString,formatter)
      (localDate,x._2)
  }.toArray
  Data.sliding(10).map{ window =>
    val next = window.last._2
    val prev = window.head._2
    (next-prev)/prev
  }.toArray
}

val stocksReturns = stocks.map(twoWeekReturns).toArray.toSeq
val factorsReturns = factors.map(twoWeekReturns).toArray.toSeq

//=============5.将市场因子矩阵转换为OLSMultipleLinearRegression需要的数组=========
def factorMatrix(factor:Seq[Array[Double]]):Array[Array[Double]] = {
  val mat = new Array[Array[Double]](factor.head.length)
  for (i <- factor.head.indices){
    mat(i) = factor.map(_(i)).toArray
  }
  mat
}

val factorMat = factorMatrix(factorsReturns)

//==================6.添加市场因子的附加特征：平方根和平方项==========================
def featurize(factorReturns:Array[Double]):Array[Double] = {
  val squaredReturns = factorReturns.map(x=>math.signum(x)*x*x)
  val squareRootedReturns = factorReturns.map(x=>math.signum(x)*math.sqrt(math.abs(x)))
  squaredReturns ++ squareRootedReturns ++ factorReturns
}

val factorFeatures = factorMat.map(featurize)

//==================7.进行线性回归计算因子权重========================================
import org.apache.commons.math3.stat.regression.OLSMultipleLinearRegression

def linearModel(instrument:Array[Double],
  factorMatrix:Array[Array[Double]]):OLSMultipleLinearRegression  = {
  val regression = new OLSMultipleLinearRegression()
  regression.newSampleData(instrument,factorMatrix)
  regression
}

val factorWeights = stocksReturns.
  map(linearModel(_,factorFeatures)).
  map(_.estimateRegressionParameters()).toArray

//  //==================8.绘制样本集的密度曲线==========================================

// import org.apache.spark.mllib.stat.KernelDensity    
// import org.apache.spark.util.StatCounter
// import breeze.plot._
// 
// def plotDistribution(samples:Array[Double]):Figure = {
//  val min = samples.min
//  val max = samples.max
//  val stddev = new StatCounter(samples).stdev
//  val bandwidth = 1.06*stddev * math.pow(samples.size,-0.2)//西尔弗曼经验法则
//  
//  val domain = Range.Double(min,max,(max-min)/100).toList.toArray
//  val kd = new KernelDensity().
//    setSample(samples.toSeq.toDS.rdd).
//    setBandWidth(bandwidth)
//  val densities = kd.estimate(domain)
//  val f = Figure()
//  val p = f.subplot(0)
//  p += plot(domain,densities)
//  p.xlabel = "Two Week Returns"
//  p.ylabel = "Density"
//  f
//  }

//==================9.查看市场因子的相关性=============================================
import org.apache.commons.math3.stat.correlation.PearsonsCorrelation

val factorCor = new PearsonsCorrelation(factorMat).getCorrelationMatrix().getData()
println("市场因子的皮尔森相关系数矩阵\n"+
    factorCor.map(_.mkString("\t\t")).mkString("\n\n"))

//==================10.计算市场因子样本的均值和协方差、查看正态分布情况===================
import org.apache.commons.math3.stat.correlation.Covariance
import org.apache.commons.math3.distribution.MultivariateNormalDistribution

val factorCov = new Covariance(factorMat).getCovarianceMatrix().getData()
val factorMeans = factorsReturns.map(factor=>factor.sum/factor.size).toArray
val factorsDist = new MultivariateNormalDistribution(factorMeans,factorCov)
factorsDist.sample()
factorsDist.sample()

//==================11.进行蒙特卡罗模拟实验==============================================

// -----计算单个金融工具的收益------
def instrumentTrialReturn(instrument:Array[Double],
	trial:Array[Double]):Double = {
  var instrumentTrialReturns = instrument(0)
  var i = 0
  while (i < trial.length) {
  	instrumentTrialReturns += trial(i) * instrument(i+1)
    i += 1
  }
  instrumentTrialReturns
}

// ----计算单个金融工具的平均收益-----
def trialReturn(trial:Array[Double],
    instruments:Seq[Array[Double]]):Double = {
  var totalReturn = 0.0
  for (instrument <- instruments) {
  	totalReturn += instrumentTrialReturn(instrument,trial)
  }
  totalReturn / instruments.size
}

// ----采用Mersenne Twister 对多元正太进行随机采样----
import org.apache.commons.math3.random.MersenneTwister

def trialReturns(seed:Long,numTrials:Int,
	instruments:Seq[Array[Double]],factorMeans:Array[Double],
	factorCov:Array[Array[Double]]):Seq[Double] = {
  val rand = new MersenneTwister(seed)
  val multivariateNormal = new MultivariateNormalDistribution(rand,factorMeans,factorCov)
  val trialReturns = new Array[Double](numTrials)
  for (i <- 0 until numTrials) {
  	val trialFactorReturns = multivariateNormal.sample()
  	val trialFeatures = featurize(trialFactorReturns)
  }
  trialReturns
}

// ------生成随机数种子组成的RDD-----
val parallelism = 1000
val baseSeed = 1496

val seeds = (baseSeed until baseSeed + parallelism)
val seedDS = seeds.toDS().repartition(parallelism)

val numTrials = 1000000
val trials = seedDS.flatMap(
	trialReturns(_,numTrials / parallelism,factorWeights,factorMeans,factorCov))

trials.cache()

// ----计算VaR-----
import org.apache.spark.sql.Dataset

def fivePercentVaR(trials:Dataset[Double]):Double = {
	val quantiles = trials.stat.approxQuantile("value",Array(0.05),0.0)
	quantiles.head
}

val valueAtRisk = fivePercentVaR(trials)
//println(valueAtRisk)

// ----计算CVaR------
def fivePercentCVaR(tirals:Dataset[Double]):Double ={
	val topLosses = trials.orderBy("value").
	  limit(math.max(trials.count().toInt / 20,1))
	topLosses.agg("value" -> "avg").first()(0).asInstanceOf[Double]
}

val conditionalValueAtRist = fivePercentCVaR(trials)
//print(conditionalValueAtRist)

//==================12.回报分布可视化===============================================
import org.apache.spark.sql.functions
import org.apache.spark.mllib.stat.KernelDensity    
import org.apache.spark.util.StatCounter
import breeze.plot._
 
def plotDistribution(samples:Dataset[Double]):Figure = {
	val (min,max,count,stddev) = samples.agg(
	  functions.min($"value"),
	  functions.max($"value"),
	  functions.count($"value"),
	  functions.stddev_pop($"value")
	 ).as[(Double,Double,Long,Double)].first()
	val bandwidth = 1.06 * stddev * math.pow(count,-0.2)
	val domain = Range.Double(min,max,(max-min) / 100).toList.toArray
	val kd = new KernelDensity().setSample(samples.rdd).setBandwidth(bandwidth)
	val densities = kd.estimate(domain)
	val f = Figure()
	val p = f.subplot(0)
	p += plot(domain,densities)
	p.xlabel = "Two Week Returns"
	p.ylabel = "Density"
	f   
}

//==================13.结果评估=================================================
// ----计算置信区间-------
def bootstrapCI(tirals:Dataset[Double],
	computeStat:Dataset[Double]=>Double,
	numResamples:Int,prob:Double):(Double,Double) ={
  val stats = (0 until numResamples).map { i => 
    val resample = trials.sample(true,1.0)
 	  computeStat(resample)
 }.sorted
  val lowerIndex = (numResamples*prob / 2 - 1).toInt
  val upperIndex = math.ceil(numResamples*(1-prob/2)).toInt
  (stats(lowerIndex),stats(upperIndex))
}

bootstrapCI(trials,fivePercentVaR,100,.05)
bootstrapCI(trials,fivePercentCVaR,100,.05)

// ----Kupiec的失败频率检验法：计算损失超过VaR的次数。备择假设VaR是合理的。----
var failures = 0
for (i <- stocksReturns.head.indices){
	val loss = stocksReturns.map(_(i)).sum / stocksReturns.size
	if (loss < valueAtRisk) {
		failures += 1
	}
}
println(f"失败次数为:$failures")

val total = stocksReturns.size
val confidenceLevel = 0.05
val failureRatio = failures.toDouble / total
val logNumber = ((total-failures) * math.log1p(-confidenceLevel) + 
	failures * math.log(confidenceLevel))
val logDenom = ((total-failures) * math.log1p(-failureRatio) + 
	failures * math.log(failureRatio))
val tStat = -2 * (logNumber-logDenom)

import org.apache.commons.math3.distribution.ChiSquaredDistribution
val p = 1 - new ChiSquaredDistribution(1.0).cumulativeProbability(tStat)

print(f"t值为$tStat,\np值为$p")






