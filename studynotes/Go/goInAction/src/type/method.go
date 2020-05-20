package main

import "fmt"

type person struct {
	name string
	email string
}

//实现一个方法——使用 值接收者 进行声明,调用时会使用这个值的副本来执行
func (p person) notify()  {
	fmt.Printf(
		"%s's email is %s\n",
		p.name,p.email)
}

//实现一个方法——使用 指针接收者 进行声明，调用时共享指针接收者指向的值
func (p *person) changeEmail(email string){
	p.email = email
	fmt.Printf("%s's email has changed to %s \n",p.name,p.email)
}

/*
一般规则：新增或者删除某个值，使用值接收者；修改某个值，使用指针接收者。
		但根本在于类型的本质，原始本质使用值接受者；非原始本质使用指针接收者。
		例外：需要让类型的值符合某个interface时，即便时非原始本质也可以使用值接受者声明方法。
引用类型：切片slice、映射map、通道channel、接口interface、函数func 【字符串string】
引用类型创建的变量称为header，是一个指向底层数据结构的指针。

*/


func main()  {
	xiaoMing := person{"xiaoming","xxx@xx.com"} //值变量

	xiaoMing.notify()
	xiaoMing.changeEmail("9090950@haha.com") 
	//Go编译器处理为
	(&xiaoMing).changeEmail("&&&&&@&&.com")

	xiaoHong := &person{"xiaohong","yyy@yy.com"} //指针变量
	xiaoHong.notify()
	//Go编译器处理为
	(*xiaoHong).notify()
	xiaoHong.changeEmail("9090950@haha.com")

}