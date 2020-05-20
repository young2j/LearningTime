package main 

import (
	"fmt"
	"sync"
	"time"
	"math/rand"
)

/*
无缓冲通道：
 1.要求发送goroutine和接收goroutine同时准备好，才能完成发送和接收操作；
 2.如果没有同时准备好，会导致先发送或接收的goroutine阻塞等待；
 3.发送和接收的交互行为其本身是同步的。
*/
var wg sync.WaitGroup

func init () {
	rand.Seed(time.Now().UnixNano())
}

func main()  {

	court := make(chan int) //无缓冲整型通道

	wg.Add(2)

	//两个routine同时准备好
	go player("A",court)
	go player("B",court)

	court <- 1

	wg.Wait()
	
}

func player(name string, court chan int){
	defer wg.Done()

	for {
		ball,ok := <- court 
		if !ok {
			fmt.Printf("Player %s won.\n",name)
			return 
		}

		n := rand.Intn(100) //一个100以内的随机整数
		if n%13 == 0{
			fmt.Printf("Player %s missed.\n",name)
			close(court) //关闭通道
			return 
		}
		fmt.Printf("Player %s hit %d.\n",name,ball)
		ball++
		court <- ball
	}
}
