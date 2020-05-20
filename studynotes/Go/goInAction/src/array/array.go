package main

import "fmt"

/*
声明并初始化为零值
*/
//[0,0,0,0,0]
var arr [5]int

//[ ]
var strArr [3]string

//[[0 0] [0 0]]
var ndarr [2][2]int

func main() {
	/*
		声明并初始化为字面量
	*/
	arr1 := [5]int{1, 2, 3, 4, 5}
	arr2 := [...]int{43, 434, 34, 24}
	arr3 := [5]int{1: 10, 3: 30}
	arr4 := [5]*int{1: new(int), 3: new(int)} //指针数组

	arr5 := [3]string{"1", "2", "3"}
	arr6 := [3]*string{new(string), new(string), new(string)}

	ndarr1 := [4][2]int{{0, 0}, {0, 1}, {1, 0}, {1, 1}} //[[0 0] [0 1] [1 0] [1 1]]
	ndarr2 := [4][2]int{1: {0, 1}, 2: {0: 1}}           //[[0 0] [0 1] [1 0] [0 0]]

	fmt.Println(arr)
	fmt.Println(arr1)
	fmt.Println(arr2)
	fmt.Println(arr3)
	fmt.Println(arr4[0] == nil) //true
	*arr4[1] = 0
	fmt.Println(arr4[1], *arr4[1], arr4[3]) //pointer,0,pointer
	*arr6[0] = "4"
	fmt.Println(strArr, arr5, *arr6[0])
	fmt.Println(ndarr)
	fmt.Println(ndarr1)
	fmt.Println(ndarr2)
}
