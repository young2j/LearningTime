package main 

import (
	"sync"
	"fmt"
	"time"
	"math/rand"
)

/*
有缓冲通道：
 1.不要求goroutine之间同时完成发送和接收；
 2.只有在通道中没有可用缓冲区时，发送动作才会阻塞；
 3.只有通道中没有值可以接收时，接收动作才会阻塞。
*/

const (
	numberGoroutines = 4
	taskLoad = 10 
) //常量

var wg sync.WaitGroup

func init(){
	rand.Seed(time.Now().Unix())
}

func main(){

	tasks :=make(chan string,taskLoad)
	wg.Add(numberGoroutines)

	for gr:=0;gr<numberGoroutines;gr++{
		go worker(tasks,gr) //从channel不断接收值
	}

	for post:=0;post<=taskLoad;post++{
		tasks <- fmt.Sprintf("Task: %d",post) //往channel不断发送值
	}

	close(tasks) //关闭channel

	wg.Wait()
}

func worker(tasks chan string,gr int){
	defer wg.Done()

	for {
		task,ok := <- tasks
		if !ok {
			fmt.Printf("Worker %d shutdown.\n",gr)
			return
		}

		fmt.Printf("Worker %d started %s.\n",gr,task)

		//模拟一段工作的时间
		sleep := rand.Int63n(100)
		time.Sleep(time.Duration(sleep)*time.Millisecond)

		//
		fmt.Printf("Worker %d finished %s.\n",gr,task)
	}
}