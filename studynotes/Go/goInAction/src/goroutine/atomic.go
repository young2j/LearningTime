package main 

import (
	"fmt"
	"runtime"
	"sync"
	"sync/atomic"
)


var (
	counter2 int64
	wg sync.WaitGroup
)

func main(){
	wg.Add(2)

	go incCounter2()
	go incCounter2()

	wg.Wait()

	fmt.Println("final counter2=",counter2)
}


func incCounter2() {
	defer wg.Done()

	for count:=0;count<2;count++{
		atomic.AddInt64(&counter2,1)
		runtime.Gosched()
	}
}