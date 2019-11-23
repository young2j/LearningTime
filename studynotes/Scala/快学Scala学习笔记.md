<center><b>
    快学Scala学习笔记
</b></center>

# 第一章 基础

## 常用类型

scala有七种数值类型：`Byte、Char、Short、Int、Long、Float和Double、Boolean` ，与Java不同的是，这些都是类（Java有包装类）。Scala并不区分基本类型与引用类型。

Scala底层基于Java提供了`StringOps、RichInt、RichDouble、RichChar、BigInt、BigDecimal` 等类，提供了更多的方法。如：

```scala
1.toString()  //可以对数字执行方法
'hello'.intersect('world') //'hello'先被隐式转换为StringOps对象，接着StringOps类的intersect方法被调用。
1.to(10) //1首先被转换为RichInt，然后应用to方法，最终交出Range(1,2,3,4,5,6,7,8,9,10)
```

## 算术和操作符重载

Scala中`+-*/%` 等操作符实际上是方法：

```scala
a+b //等价于 a.+(b)
1.to(10) //等价于 1 to 10
'r'.to('u') //Range('r','s','t','u')
```

Scala中没有自增`++`和自减`--`操作。

## 方法调用

Scala中如果方法没有参数，就不需要使用括号，如：

```scala
“Bonjour”.sorted
```

使用以scala.开头的包时，可以省去scala前缀。如：

```scala
import scala.math._ //等同于 import scala.math._
math.sqrt(2) //等同于scala.math.sqrt(2)
```

## apply方法

Scala中字符串截取使用`s(4)` 而不是`s[4]`，其背后是StringOps的apply方法：`s.apply(4)`

```scala
(“Bonjour”.sorted)(3) //是 “Bonjour”.sorted.apply(3)的简写
```

伴生对象的apply方法：

```scala
BigInt("1234567890")//将字符串或数字转换为BigInt，是BigInt.apply("1234567890")的简写
Array(1,3,6,76) //调用的也是伴生对象Array的apply方法
```

# 第二章 控制结构和函数

## 条件表达式

Scala中表达式是有值的，可以将表达式赋值给变量：

```scala
val s =  if (x>0) 1 else -1 //等同于
Int s = x>0 ? 1:-1 //Java或C++三元运算符
```

表达式的值类型是两个分支类型的超类型，如：

```scala
if (x>0) "positive" else -1 //java.lang.String和Int的超类型是Any
```

如果esle缺失了，则引入一个`Unit`类，写作`()`：

```scala
if (x>0) 1 //等同于 
if (x>0) 1 else ()
//可以把()当做表示"无有用值"的占位符，可看做void，但void没有值，Unit是一个表示"无"的值。
```

##  块表达式和赋值

Scala中`{}`块包含一系列表达式，块中最后一个表达式的值就是块的值。如：

```scala
val d = {val a=1;val b=2;a+b}
```

在Scala中，赋值操作本身是没有值的，或者严格的说，赋值操作的值是`Unit`类，即`()`:

```scala
x=y=1 //连续赋值是没有意义的，y=1 的值是()
```

## 输入和输出

```scala
print('age:')
println(42) //等同于

println('age:'+42)

printf("Hello,%s! You are %d years old.%n",name,age) //C风格
print(f"Hello,$name! You are ${age+0.5}%7.2f years old")//字符串插值
print(s"Hello,%{name}!You are ${age+0.5} years old") //s前缀，不能有格式化指令%7.2f

print(raw"\n Hello") //输出\n，不会换行
print("$$$name") //输出$号，需要两个$$
```

从控制台读取输入:

```scala
scala.io.StdIn.readLine/readInt/readDouble/readByte/readShort/readLong/readFloat/readBoolean/readChar

import scala.io
val name = StdIn.readLine("your name:") //readLine带一个参数作为提示字符串
```

## 循环

```scala
while (n>0) {
    r = n*r
    n -= 1
} //while 循环
for (i <- 1 to n) {
    r = r*i
} //for 循环
```

Scala没有continue和break来退出循环，当需要退出循环时：

```scala
import scala.util.control.Breaks._
breakable{
    for (...) {
        if (...) break; //退出breakable代码块
        ...
    }
}
```

高级for循环：

```scala
for (i <- 1 to 3;j <- 1 to 3){
    print(f"${10*i+j}%3d")
}

for (i <- 1 to 3;j <- 1 to 3 if i!=j) {
    print(f"${10*i+j}%3d")
} //为生成器带上守卫--以if开头的Boolean表达式。

for (i <- 1 to 10; n = 4-i;j <- n to 3) {
    print(f"${10*i+j}%3d")
} //可以在循环中引入更多定义

for (i <- 1 to 10) yield i%3 //for 推导式--循环体以yield开始。 
```

## 函数

```scala
def fac(n:Int):Int = {
    if (n<0) 1 else n*fac(n-1)
} //递归函数必须指定返回类型

def fac(n:Int=5):Int ={
    if (n<0) 1 else n*fac(n-1)
} // 将参数n改为默认参数

def sum(n:Int*)={
    var res = 0
    for (i <- n) res += i
    res 
} //变长参数--类型必须为Seq，如下写法是不对的：
val s = sum(1 to 5) //1 to 5 是Range类，应该追加:_*
val s = sum(1 to 5:_*) //告诉编译器参数被当做参数序列Ｓｅｑ处理

def recursiveSum(args:Int*) = {
    if (args.length==0) 0
    else args.head + recursiveSum(args.tail:_*)
} //:_*常在递归定义中使用
```

参数类型为Object的Ｊava方法时，需要手工对基本类型进行转换，例如`MessageFormat.format`:

```scala
val str = MessageFormat.format("the answer to {0} is {1}","everything",42.asInstanceOf[AnyRef])
```

## 过程

函数在声明时，不要`=`，返回类型就是`Unit`，这样的函数成为过程。过程不返回值，调用它仅仅是为了它的副作用。

```scala
def box(s:String) {//没有＝号
    val border = "-" * (s.length+2)
    print(f"$border%n|$s|%n$border%n")
} //等同于显示声明Unit类型

def box(s:String):Unit = {
    val border = "-" * (s.length+2)
    print(f"$border%n|$s|%n$border%n")
}
```

## 懒值

```scala
lazy val file  = scala.io.Source.fromFile("/usr/share/words").mkString
//懒值的初始化会被推迟，直到首次对它取值
```

## 异常

```scala
//抛出异常
if (x>0) {
    sqrt(x)
} else throw new IllegalArgumentException("x should not be negative")

//捕获异常
val url = new URL("http://...").openStream()
try{
    process(url)
} catch {
    case _:MalformedURLException => println(s"Bad URL:$url") //不需要使用捕获的异常对象，可以使用——来替代变量名
    case ex:IOException => ex.printStackTrace()
}　finally {
    url.close()
}
```

# 第三章　数组相关操作

## 定长数组

```scala
val nums = new Array[Int](10) //10个整数数组，所有元素初始化为０
val str = new Array[String](10) //10个字符串数组，所有元素初始化为ｎｕｌｌ
```

## 变长数组

```scala
import scala.collection.mutable.ArrayBuffer
val b = ArrayBuffer[Int]() //或者
val b = new ArrayBuffer[Int]

b += 1 //在尾端追加１
b += (1,3,5,7) //在尾端追加数组(1,3,5,7)。等同于
b.append(1,3,5,7)　//在线追加,是一个过程
b ++= Array(8,13,21) //可以用++操作符追加任何集合

b.trimEnd(5) //移除尾端５个元素，是一个很高效的操作
b.insert(2,6) //在下标２之前插入元素６
b.insert(2,6,7,8) //在下标２之前插入元素６，７，８
b.remove(2) //移除下标为２的元素
b.remove(2,3) //从下标２的位置开始移除连续３个元素

.toArray  .toBuffer //数组与数组缓冲相互转化
```

## 遍历数组

```scala
for (i<- 0 until a.length) println(s"$i:$a(i)") //等同于
for (i<- a.indices)　println(s"$i:$a(i)")

for (i<- 0 until a.length by 2) println(s"$i:$a(i)") //by指定遍历步长
for (i<- 0 until a.length by -1) println(s"$i:$a(i)") //从数组尾端开始遍历，等同于
for (i<- a.indices.reverse) println(s"$i:$a(i)")
```

## 数组转换for/yield

```scala
val a = Array(2,3,5,7,11)

val res = for (e<-a if e%2==0) yield 2*e //使用守卫，去除奇数，偶数翻倍。等同于
val res = a.filter(_ % 2==0).map(2*_)

val res = for (e<-a if e>=0) yield e //保留所有非负元素。或者通过下标处理如下

val posToRemove = for (i<-a.indices if a(i)<0) yield i
val res = for (i<-posToRemove.reverse) a.remove(i)
```

##  常用统计操作

```scala
val a = Array(2,43,5)
a.sum
a.mkString
a.mkString("and") //连接符
a.mkString("<","and",">")　//前缀，连接符，后缀
a.count(_>0) //统计大于０的元素个数

scala.util.Sorting.quickSort(a)//直接对数组进行快排

val b = ArrayBuffer("Marry","Bob","John")
b.max
b.min
b(1).containsSlice("B")

ArrayBuffer(3,5,2,5,32).sorted //生成的是副本，升序排列
ArrayBuffer(3,5,2,5,32).sortWith(_>_)　//提供一个比较函数，降序排列
```

## 多维数组

```scala
val matrix = Array.ofDim[Double](3,4) //３行４列

val matrix = new Arrray[Array[Int]](10)
for (i<-matrix.indices){
    matrix(i) = new Array[Int](i+1)
} //生成不规则数组
```

##　与Java互操作

想要调用一个带Ｏｂｊｅｃｔ参数的Ｊａｖａ方法，需要手工转换类型，如：

```scala
java.util.Arrays.binarySearch(Object[] a,Object key): //二分查找

val a = Array("Mary","had","a","little","lamb")
java.util.Arrays.binarySearch(a,"beef") //这样行不通

java.util.Arrays.binarySearch(a.asInstanceOf[Array[Object]],"beef") //强制转换

//或者直接用ｓｃａｌａ执行二分查找
import scala.collection.Searching._
val res = a.search("beef") 
```

# 第四章　映射和元组

## 构造映射

```scala
val scores = Map("Alice"->10,"Bob"->3,"Cindy"->8) //不可变映射，等同于
val scores = Map(("Alice",10),("Bob",3),("Cindy",8))

val scores = scala.collection.mutable.Map("Alice"->10,"Bob"->3,"Cindy"->8)//可变映射

val scores = scala.colletion.mutable.Map[String,Int]() //空映射
```

## 获取映射中的值

```scala
val BobScore = scores("Bob") //等同于Java的scores.get("Bob")
val BobScore = if (scores.contains("Bob")) scores("Bob") else 0 //contains判断是否含有键。更一般的写法是
val BobScore = scores.getOrElse("Bob",0)

val scores1 = scores.withDefaultValue(0) //给出不存在键的默认值
val scores2 = scores.withDefault(_.length)　//给出不存在键的取值函数
scores1.get("John") //给出默认值０
scores2.get("John")　// 给出默认取值"John".length，即４
```

## 更新映射中的值

在可变映射中

```scala
scores("Bob") = 7 //更新值
scores("Fred") = 10　//添加新键值对

scores += ("Bob"->7,"Fred"->10) //同时更新值与添加新键值对

scores -= "Alice" //移除键值对
```

在不可变映射中

```scala
val newScores = scores + ("Bob"->7,"Fred"->10) //创建新映射对象
var scores = scores //或使用var
scores += ("Bob"->7,"Fred"->10)
```

## 映射迭代

```scala
for ((k,v)<-scores) yield (v,k) //键值反转
scores.keySet //键集，Iterable类型
scores.values //值集，Iterable类型
```

##　已排序映射

```scala
val scores = scala.collection.mutable.SortedMap("Alice"->10,"Bob"->3,"Cindy"->8)//已按此顺序排序，遍历时顺序不会变
val scores = scala.collection.mutable.LinkedHashMap("Alice"->10,"Bob"->3,"Cindy"->8)//按插入顺序访问所有键
```

## 元组

对偶(键值对)是元组最简单的形态。

```scala
val t = (1,3.14,"Fred") //类型为Tuple3[Int,Double,java.lang.String]或者定义为(Int,Double,java.lang.String)

t._1 t._2 t._3 //访问组元，从１开始
val (first,second,_) = t //模式匹配，分别访问组元

//StringOps类的partition方法返回一个字符串对偶
"New York".partition(_.isUpper) //("NY","ew ork")
```

##　拉链操作

```scala
val  symbols = Array("<","-",">")
val counts = Array(2,10,2)
val pairs = symbols.zip(counts) // Array(("<",2),("-",10),(">",2))

pairs.toMap //将元组数组转换为映射Map
```

# 第五章　类













