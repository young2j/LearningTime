//----交叉类型--- type1 & type2 & type3
function extend<T,U>(first:T,second:U):T&U {
    let result = <T&U>{}
    for(let id in first){
        (<any>result)[id] = (<any>first)[id]
    }
    for (let id in second){
        if(!result.hasOwnProperty(id)){
            (<any>result)[id] = (<any>second)[id]
        }
    }
    return result
}

class Person {
    constructor(public name:string){}
}

interface Loggable{
    log():void
}

class ConsoleLogger implements Loggable{
    log(){
        //...
    }
}

let xiaoZ = extend(new Person('xiaoZ'),new ConsoleLogger())
console.log(xiaoZ.name)
xiaoZ.log()

//----联合类型---- type1 | type2 | type3
function unionTypeFunc(a:string,b:string|number) {
    //...
}

//只能访问联合类型的共有成员
interface Bird{
    fly()
    layEggs()
}
interface Fish{
    swim()
    layEggs()
}
function getSmallPet():Fish|Bird {
    //...
    return
}
let pet = getSmallPet()
pet.layEggs() //ok
// pet.fly() //error
// 使用类型断言：
if((<Fish>pet).swim){
    (<Fish>pet).swim()
}else{
    (<Bird>pet).fly()
}

//使用identifier！去除null或undefined
function removeNullOrUndefined(name:string|null):string{
    function innerFn(epithet:string):string{
        // return name.charAt(0) + '. the ' + epithet //error, 'name' is possibly null
        return name!.charAt(0) + '. the ' + epithet
    }
    name = name || 'Bob'
    return innerFn("great")
}


//----类型别名----和接口相似，但
//1.类型别名不会新建一个类型，只是创建了一个新的 名字引用(也就是指向原始类型)；接口创建了一个新的名字；
//2.类型别名不能被extends和implements；接口可以

type Name = string
type NameResolver = () => string
type NameOrResolver = Name | NameResolver
type Container<T> = { value: T}
type Tree<T> = {
    value:T,
    left: Tree<T>,
    right: Tree<T>
}
//只能从三种允许的字符中选择其一，其它值则会产生错误
type stringsAlias = "ease-in" | "ease-out" | "ease-in-out" 
type numsAlias = 1 | 2 | 3


//----可辨识特征、可辨识标签----
interface Square {
    kind: "square"; //
    size: number;
}
interface Rectangle {
    kind: "rectangle"; //
    width: number;
    height: number;
}
interface Circle {
    kind: "circle"; //
    radius: number;
}

type shape = Square | Rectangle | Circle;
function area(s: shape) {
    switch (s.kind) {
        case "square": return s.size * s.size;
        case "rectangle": return s.height * s.width;
        case "circle": return Math.PI * s.radius ** 2;
    }
}

//----索引类型----
// keyof T => 索引类型查询操作符，结果为T上公共属性名的联合类型
// T[K] => 索引访问操作符

function pluck<T,K extends keyof T>(o:T,names:K[]):T[K][]{
    return names.map(n=>o[n])
}
interface Index {
    name: string
    age: number
}
let index:Index = {
    name:'John',
    age:35
}
let tkArr:string[] = pluck(index,['name'])
