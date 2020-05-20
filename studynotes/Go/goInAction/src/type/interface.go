package main
import "fmt"

/*
接口interface: 
	用来定义行为的类型
	这些行为不通过接口直接实现，而是通过用户定义类型(实体类型)的方法实现

接口值的数据结构：
	包含两个指针:一个指向内部表iTable的指针 + 一个指向所存储值的指针
	iTable包含 所存储值的类型和方法集

*/


//接口1
type notifier interface {
	notify()
}

//接口2
type birthTip interface{
	birth()
}

//实体类型
type user struct {
	name string
	age int
}

//使用指针接收者实现一个方法，只有指向那个类型的指针(&user)才能实现对应的接口.值(user)会取址失败
func (u *user) notify() {
	fmt.Printf("%s has %d years old.\n",u.name,u.age)
}

//使用值接收者实现一个方法，那个类型的值(user)和指针(&user)都可以实现对应的接口
func (u user) birth()  {
	fmt.Printf("today is %s's birthday.\n",u.name)
}

//
func sendNotify(n notifier) {
	n.notify()
}

//声明接口变量
var n notifier
var b birthTip
var bp birthTip

func main()  {
	u := user{"xiaoMing",12}
	sendNotify(&u)
	// sendNotify(u) //error

	n = &user{"xiaoWang",16} //采用实体指针赋值接口值
	n.notify()

	b = user{"xiaoHong",18} //采用实体值赋值接口值
	b.birth()

	bp = &user{"laoWang",38} //采用实体指针赋值接口值
	bp.birth()
}


