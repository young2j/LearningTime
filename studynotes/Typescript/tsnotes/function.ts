//Function
let func: Function = ()=>{}

//完整的函数类型写法
let myAdd:(a:number,b:number,c?:number)=>number = //定义函数类型：参数类型和返回值类型
function(x:number,y:number,z?:number):number { //定义的具体函数
    if(z){
        return x+y+z
    }
    return x+y
}
//推断类型
let myAdd_:(a:number,b:number)=>number = //定义函数类型：参数类型和返回值类型
function(x,y) { //自动类型推断
    return x+y
}

//可以省略函数类型定义
let hisAdd = function(a:number,b:number):number{
    return a+b
}

//默认参数
function addWithDefaultParam(a:number,b:number,c=10):number {
    return a+b+c
}
addWithDefaultParam(5,5)
//默认参数可以放在必须参数前面，但是在调用传参时，对应位置必须传入undefined
const addWithDefaultParam_ = (c=10,a:number,b:number):number => a+b+c
addWithDefaultParam_(undefined,5,5)

//剩余参数
function addWithRestParams(a:number,b:number,...c:number[]) {
    let sum = a+b
    c.forEach(num=>sum+=num)
    return sum
}
addWithRestParams(1,2,3,4)

//this指向
interface Card{
    suit: string;
    card:number
}
interface Deck{
    suits: string[]
    cards: number[]
    createCardPicker(this:Deck):()=>Card
}

let deck: Deck = {
    suits:["hearts", "spades", "clubs", "diamonds"],
    cards:Array(52),
    createCardPicker: function(this:Deck){
        // return function(){
        //     let pickedCard = Math.floor(Math.random()*52)
        //     let pickedSuit = Math.floor(pickedCard/13)
        //     return {
        //         suit:this.suits[pickedSuit], //this调用时指定
        //         card:pickedCard%13
        //     }
        // }

        //箭头函数能保存函数创建时的this值，而不是调用时的值
        return ()=>{
            let pickedCard = Math.floor(Math.random()*52)
            let pickedSuit = Math.floor(pickedCard/13)
            return {
                suit:this.suits[pickedSuit],
                card:pickedCard%13
            }
        }
    }
}

let cardPicker = deck.createCardPicker()
let pickedCard = cardPicker() //顶级的非方法式调用会将 this视为window/undefined，解决：使用箭头函数

console.log("card: "+ pickedCard.card + ' of ' + pickedCard.suit)


//重载
// 重载的pickCard函数在调用的时候会进行正确的类型检查。=>同样的函数名，不同的参数返回不同的值
let suits = ["hearts", "spades", "clubs", "diamonds"];

function pickCard(x: {suit: string; card: number; }[]): number;
function pickCard(x: number): {suit: string; card: number; };
function pickCard(x): any {
    // Check to see if we're working with an object/array
    // if so, they gave us the deck and we'll pick the card
    if (typeof x == "object") {
        let pickedCard = Math.floor(Math.random() * x.length);
        return pickedCard;
    }
    // Otherwise just let them pick the card
    else if (typeof x == "number") {
        let pickedSuit = Math.floor(x / 13);
        return { suit: suits[pickedSuit], card: x % 13 };
    }
}

let myDeck = [{ suit: "diamonds", card: 2 }, { suit: "spades", card: 10 }, { suit: "hearts", card: 4 }];
let pickedCard1 = myDeck[pickCard(myDeck)];
alert("card: " + pickedCard1.card + " of " + pickedCard1.suit);

let pickedCard2 = pickCard(15);
alert("card: " + pickedCard2.card + " of " + pickedCard2.suit);
