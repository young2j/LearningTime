package main

import (
	"fmt"
	"runtime"
	"sync"
)

/*
 两个或多个goroutine同时访问(读或写)某个共享资源，在没有同步的情况下，就会形成竞争状态，称为竞态race condition.
 要保证同一时刻只有一个goroutine对共享资源进行读或写操作：
  1. 使用原子函数atomic [atomic.go]
  2. 使用互斥锁mutex [mutex.go]
  3. 使用通道channel [channel.go]

  go build -race //编译时检查是否存在rc
*/

var (
	counter1 int
	wg sync.WaitGroup
)

func main() {
	wg.Add(2)

	go incCounter1()
	go incCounter1()


	wg.Wait()
	fmt.Println("final counter1=",counter1) //2. should be 4
}

func incCounter1()  {
	defer wg.Done()

	for count:=0;count<2;count++{
		value := counter1

		runtime.Gosched() //当前goroutine从线程退出，放回队列，即主动切换goroutine

		value++

		counter1 = value
	}
}
