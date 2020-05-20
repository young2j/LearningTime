package main

import "fmt"

/*
map 没有容量或者任何限制
*/

//nil map
var dict map[string]int

func main() {
	dict1 := map[string]string{}
	dict2 := make(map[string]string)

	dict1["black"] = "#000"
	dict2["black"] = "#000"
	//dict["black"] = 0 // error,nil map不能存储键值对 

	value,exists := dict1["black"]
	zero,no := dict1["white"] //不存在的key，值会返回一个零值，string的零值为""

	if exists {
		fmt.Println(value)
	}

	if !no{
		fmt.Printf("zero:%v,no:%v \n",zero,no)
	}

	fmt.Println(dict)
	fmt.Println(dict1)
	fmt.Println(dict2)

	//for
	for key,value := range dict2{
		fmt.Printf("key:%s, value:%s \n",key,value)
	}

	//delete
	delete(dict2,"black")
}
