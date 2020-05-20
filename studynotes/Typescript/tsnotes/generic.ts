//泛型：使用T来捕获输入参数的类型
function func1<T>(arg: T): T {
    return arg
}
//数组参数
function func2<T>(args: T[]): T[] {
    console.log(args.length)
    return args
}
//等同于
function func3<T>(args: Array<T>): Array<T> {
    console.log(args.length)
    return args
}


//泛型接口
interface GenericFn {
    <T>(arg: T): T
}
let myGenericFn: GenericFn = function <T>(arg: T): T { return arg }

//泛型接口参数
interface GenericFnWithParam<T> {
    (arg: T): T
}
let myGenericFnWithParam: GenericFnWithParam<number> = function <T>(arg: T): T { return arg }


//泛型类
class GenericClass<T>{
    name: T
    add: (x: T, y: T) => T
}
let myGenericClass = new GenericClass<string>()
myGenericClass.name = "genericClass"
myGenericClass.add = function(x,y){return x + y}

//泛型约束
interface Constraint {
    length: number
}
function genericFnWithConstraint<T extends Constraint>(arg:T) {
    console.log(arg.length)
}
// genericFnWithConstraint(4) //error
genericFnWithConstraint([4]) //ok


//在泛型中使用类类型
class BeeKeeper {
    hasMask: boolean;
}

class ZooKeeper {
    nametag: string;
}

class Animal {
    numLegs: number;
}

class Bee extends Animal {
    keeper: BeeKeeper;
}

class Lion extends Animal {
    keeper: ZooKeeper;
}

function createInstance<A extends Animal>(c: new () => A): A { //参数c是一个构造函数
    return new c();
}

createInstance(Lion).keeper.nametag;  // typechecks!
createInstance(Bee).keeper.hasMask;   // typechecks!