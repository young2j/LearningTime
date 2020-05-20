package main

import (
	"log"
	"sync"
	"time"
	"concurrencyMode/work"
)

var names = []string {
	"xiaoMing",
	"xiaoHong",
	"xiaoWang",
	"xiaoZhang",
	"xiaoYang",
}

type namePrinter struct{
	name string
}


//implement Task interface
func (np *namePrinter) Task()  {
	log.Println(np.name)
	time.Sleep(time.Second)
}

func main(){
	p:=work.New(2) 

	var wg sync.WaitGroup
	wg.Add(100*len(names))

	for i:=0;i<100;i++{
		for _,name := range names{
			np:=namePrinter{
				name:name,
			}
			go func ()  {
				p.Run(&np)
				wg.Done()
			}()
		}
	}

	wg.Wait()

	p.Shutdown()
}

