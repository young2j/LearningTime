package main

import (
	"fmt"
	"sync"
	"runtime"
)

var (
	counter3 int
	wg sync.WaitGroup

	mutex sync.Mutex
)

func main(){
	wg.Add(2)

	go incCounter3()
	go incCounter3()

	wg.Wait()

	fmt.Println("final counter=",counter3)
}

func incCounter3(){
	defer wg.Done()

	for count:=0;count<2;count++{

		mutex.Lock()
		{
			value := counter3
			
			runtime.Gosched()
			
			value++
			
			counter3 = value
		}
		mutex.Unlock()
	}
}