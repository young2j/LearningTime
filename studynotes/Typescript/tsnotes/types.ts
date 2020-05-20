//-----bool-----
let yes:boolean = true
//string
let a: string = "字符串变量"
//-----number-----
let b: number = 1

//----symbol----
let uuid:symbol = Symbol()
//-----Array-----
let numberArr: number[] = [1,2,3]
let numberArrGeneral: Array<number> = numberArr //泛型写法
let strArr: string[] = ['a','b','c']
let strArrGeneral: Array<string> = strArr

//-----Tuple-----
let tuple:[string, number , boolean, number[]]
tuple = ['',0,false,[0,1]]

//-----enum-----
//默认从0开始编号,可自行修改
enum Color{
    Red,//默认Red=0
    Green,
    Blue
}
let color: Color = Color.Green //通过枚举名获得编号
console.log('color:',color); // output=> 1


//枚举名=枚举值，自定义编号
enum Colors {
    Red=1,
    Green, //也为2,但取2时是Blue
    Blue=2
}
let colorValue:Colors = Colors.Green
console.log('colorValue:',colorValue)
let colorName:string = Colors[2] //通过编号取枚举名
console.log('colorName:',colorName);//output=> 'Blue'

//-----Any-----
let notSure: any = 2
notSure = true
let notSureArr: any[] = [1,'',false]
notSureArr[0]='string'

//-----null undefined-----
let n:null = null
let u:undefined = undefined

//-----void-----
function returnVoid():void {
    console.log("void表示没有任何类型")
}
const returnVoidArrow = ():void => {
    console.log("箭头函数版")
}

//----never----
// 特性1: 通常在方法里和抛出异常throw搭配使用
// 特性2: never是所有类型的子类型，因此可以把never类型值赋给任意类型变量。
// 特性3: never没有子类型，因此所有类型的值都不能赋给never类型变量
//表示永远不存在值的类型，有两种应用情况:
//1.抛出异常
function error(message:string):never{
    throw new Error(message)
}
function fail() {
    error("推断返回类型为never")
}
//2.存在无法到达的终点，即永远不会有返回值
function infiniteLoop():never {
    while(true){}
}

//----object----
let obj:Object = {} 
let o:object = {}
o = null 
// o = 42

//类型断言=>相当于类型转换
let sentence:any = "it is a good day."
let len1:number = (<string>sentence).length //尖括号语法
let len2:number = (sentence as string).length //as语法,两种等价但jsx只能用它


//----interface----
//作用：是对 值(对象、函数、类) 所具有的结构 进行类型检查。就是一种约束。
//--1、对象--
interface Person{
    name:string; //必须
    age:number; //必须
    gender?:string; //可有可无
    readonly height:number; //只读，初始化后不可再修改
    //与const的区别：变量用const，属性用readonly
    [propName: string]: any;//表示可以有任意数量的属性
}
const knownPerson = (person:Person)=>{
    console.log(`${person.name} has been ${person.age} years old.`)
}

let xiaoMing:Person = {
    name:'xiaoMing',
    age:16,
    height:150,//xiaoMing.height=180会出错
}
knownPerson(xiaoMing)

//--2、函数变量--
interface PrintFunc{
    (name:string,age:number):boolean;
}
let myPrintFunc:PrintFunc = function(name:string,age:number) { //参数名可以不一样，但类型必须一致
    return age>18
}

let hisPrintFunc:PrintFunc = (name,age)=>age>18 //可以省略类型，自动推断


//--3、类--
interface IClock{
    currentTime: Date; //约定必须实现的类属性
    setTime(d:Date) //约定必须实现的类方法
}

class Clock implements IClock {//类去应用定义的接口
    private timeZone:string
    currentTime:Date
    setTime(d:Date){
        this.currentTime = d
    }
    constructor(h:number,m:number){}
}

interface IUtcClock extends Clock{//接口去继承类
    changeTime():void 
    //注意：接口会继承类的private和protected成员，意味着这个接口只能被类本身或其子类实现implements
}

class UtcClock extends Clock implements IUtcClock{
    changeTime(){}
}
// class ErrUtcClock implements IUtcClock{
//     changeTime(){}
// } 这个就是错的



//--4、混合类型--
interface Mix{
    name:string; //object
    (age:number):boolean; //function
    eat():void //method
}
function getMix():Mix {
    let mix = <Mix>function(age:number){return age>18}
    mix.name = 'xiaoMing'
    mix.eat = ()=>{}
    return mix
}
let m = getMix()
m(16)
m.name = 'xiaoWang'
m.eat()



//--interface的可索引签名：定义索引返回的类型--
//=> 可以同时使用两种类型的索引，但是数字索引的返回值必须是字符串索引返回值类型的子类型。 
//=> 这是因为当使用 number来索引时，JavaScript会将它转换成string然后再去索引对象。
//1、数字number索引
interface StringArr{
    [index:number]:string //表示通过索引必须返回string类型
}
let strArray:StringArr = ['a','b']
let eleA:string = strArray[0]

//2、字符串string索引
interface numberObj{
    [index:string]:number;//表示通过索引必须返回number类型
    length:number; //ok
    // name:string //错误，类型与索引返回类型不一致
}

//--interface的继承--
interface Line{
    name:string
}
interface Triangle{
    points:number
}
interface Square{
    area:number
}

interface Shape extends Line,Triangle,Square {
    shape: string
}
let polygon = <Shape>{}
polygon.name = "polygon"
polygon.points = 4
polygon.area = 998
polygon.shape = 'square'

