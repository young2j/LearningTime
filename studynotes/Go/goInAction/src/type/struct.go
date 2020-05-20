package main

import "fmt"

//声明结构体
type user struct {
	name string
	email string
	age int
	man bool
}

//
type admin struct {
	person user
	access string
}


//零值初始化结构体
var sam user


//这样声明后duration 和 int64 不是一个类型，go编译器不会做隐式转换
type duration int64

func main()  {
	//字面量声明并初始化结构体
	lisa := user{
		name: "Lisa",
		email: "xxx@xx.com",
		age: 21,
		man: false,
	}
	
	john := user{"john","xxx@xx.com",12,true} //不使用字段名，按顺序使用结构类型的值

	fmt.Println(lisa) //{Lisa xxx@xx.com 21 false}
	fmt.Println(john) //

	boss := admin{
		person: user{
			name: "boss",
			email: "boss@666.com",
			age: 50,
			man: true,
		},
		access: "super",
	}

	fmt.Println(boss)

	// var dur duration
	// dur = int64(1000)  会报错
}

