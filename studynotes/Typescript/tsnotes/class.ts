class Greeter{
    greeting:string
    constructor(message:string){
        this.greeting = message
    }
    greet(){
        console.log('Hello '+ this.greeting)
    }
}

let greeter = new Greeter('typescript')
greeter.greet()


class Animal {
    static pet:string = 'The pet' //静态属性
    readonly category:string //只读属性必须在声明时或构造函数里被初始化
    public name:string //publilc是默认的，可以不写
    private isSuper?:boolean //private私有，外部不可访问，子类不可访问;?可选
    protected speed:number=10 //protected受保护的，外部不可访问，子类可访问
    //constructor标记为protected表示不能在类外实例化
    protected constructor(theName:string){
        this.category = 'animal'
        this.name=theName
    } 
    move(distanceInMeters:number=0){
        console.log(`${Animal.pet} ${this.name} moved ${distanceInMeters}m at the speed of ${this.speed}m/s`)
    }
}
class Dog extends Animal{
    //如果要在构造器里使用this，必须先调用super()
    constructor(name:string){
        super(name)
        this.speed = 12 //可访问受保护的speed
    }
    move(distanceInMeters=10){
        super.move(distanceInMeters)
    }
    bark(){
        console.log('woof!woof!')
    }
}
class Cat extends Animal{
    constructor(name:string){super(name)}
    move(distanceInMeters=12){
        super.move(distanceInMeters)
    }
    miao(){
        console.log('miao!miao!')
    }
}
const dog = new Dog('dog')
const cat = new Cat('cat')
dog.bark()
dog.move()
cat.miao()
cat.move()

