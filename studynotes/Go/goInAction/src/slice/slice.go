package main

import "fmt"

/*
切片三元素：指针、长度len、容量cap
尽量保持长度和容量相等，可以避免append时改变其他切片和底层数组的值
*/
//nil 切片 len=cap=0
var nilSlice []int

func main() {
	//空切片
	nullSlice1 := make([]int, 0)
	nullSlice2 := []int{}
	//len:3 cap:5
	slice1 := make([]string, 3, 5)
	//len=cap=3
	slice2 := make([]int, 3)

	//len=cap=3
	slice3 := []int{1, 2, 3}

	//len=cap=6
	slice4 := []string{5: ""}

	//len=cap=5
	slice5 := []int{1, 2, 3, 4, 5}
	//len=2 cap=4
	slice5slice := slice5[1:3] //长度3-1；容量5-1 ，主要看头指针在索引1位置上，前面部分就看不到
	//len=3 cap=4
	slice5slice = append(slice5slice, 6) //[2,3,6],底层数组以及slice5都会变

	//len=6 cap=10
	newSlice5 := append(slice5, 100) //len小于1000，底层数组容量成倍增长；大于1000，增长25%

	//len=cap=2
	slice6 := slice5[1:3:3] // [i:j:k] len=j-i cap=k-i

	//切片合并
	appendSlice := append(slice5, slice5...)

	fmt.Println(nilSlice)
	fmt.Println(nullSlice1)
	fmt.Println(nullSlice2)

	fmt.Println(slice1)
	fmt.Println(slice2)
	fmt.Println(slice3)
	fmt.Println(slice4)

	fmt.Println(slice5, slice5slice)
	fmt.Println(slice5slice)
	fmt.Println(newSlice5)
	fmt.Println(slice6)

	fmt.Printf("%v\n", appendSlice)

	// range 返回value副本
	for index, value := range appendSlice {
		fmt.Printf("index: %d , Value: %d , Value-addr: %X , Elem-addr: %X \n",
			index, value, &value, &appendSlice[index])
	}

	//
	for index := 2; index < len(appendSlice)-2; index++ {
		fmt.Printf("index: %d , Value: %d , Elem-addr: %X \n",
			index, appendSlice[index], &appendSlice[index])
	}
	//
	ndSlice()
}
func ndSlice() {
	slice := [][]int{{10}, {10, 20}}
	slice[0] = append(slice[0], 50)
	fmt.Println(slice[0], slice[1])
}
