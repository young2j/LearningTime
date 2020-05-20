package main

import "fmt"

/*
通过嵌入类型，
	可以使得与内部类型相关的标识符提升到外部类型上；
	外部类型可以声明与内部类型同名的标识符来override字段或者方法，此时内部类型的实现就不会提升。，
*/

type notifier interface {
	notify()
}

type user struct {
	name string
	age int
}

func (u *user) notify(){
	fmt.Printf("%s has %d years old.\n",u.name,u.age)
}

type admin struct { //外部类型
	user //嵌入类型
	role string
}

func sendNotify(n notifier){
	n.notify()
}

func main() {
	ad := admin {
		user: user{"stranger",25},
		role:"admin",
	}

	ad.user.notify()
	ad.notify()

	sendNotify(&ad.user)
	sendNotify(&ad)
}

