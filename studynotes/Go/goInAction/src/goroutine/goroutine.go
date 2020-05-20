package main

import (
	"fmt"
	"runtime"
	"sync"
)

/*
 通过defer修改函数的执行时间。
 如果某个goroutine长时间占用逻辑处理器，调度器会暂停该routine的执行，从而给其他routine运行的机会。
 使用多个逻辑处理器，并不意味着性能更好。
 并发不是并行。并发只同时管理多个任务；当有多个逻辑处理器且可以同时让每个goroutine都运行在一个物理处理器上，goroutine才会并行运行。
*/

func main()  {
	runtime.GOMAXPROCS(1) //分配一个逻辑处理器(对应一个线程)给调度器使用
	// runtime.GOMAXPROCS(runtime.NumCPU()) //12

	var wg sync.WaitGroup //用来记录并维护运行的goroutine
	wg.Add(2) //增加两个需要等待的goroutine

	fmt.Println("starting...")

	//goroutine1 
	go func(){
		defer wg.Done() //func函数执行完毕退出时通知main函数，该任务已完成。(即需要等待的goroutine减少1)

		for count:=0;count<3;count++{
			for char:='a';char<'a'+26;char++{
				fmt.Printf("%c",char)
			}
		}
	}()
	
	//goroutine2
	go func ()  {
		defer wg.Done()

		for count:=0;count<3;count++{
			for char:='A';char<'A'+26;char++{
				fmt.Printf("%c",char)
			}
		}
	}()


	fmt.Println("waiting...")
	
	wg.Wait() //只要wg计数大于0，Wait就会阻塞

	fmt.Println("\nterminating program")

}
