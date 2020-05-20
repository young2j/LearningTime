package main

import (
	"log"
	"time"
	"os"
	"concurrencyMode/runner"
)


const timeout = 3*time.Second

func main()  {
	log.Println("Starting work...")

	r:= runner.New(timeout)

	r.Add(createTask(),createTask(),createTask())

	if err:=r.Start(); err!=nil{
		switch err {
		case runner.ErrorTimeout:
			log.Println("Terminating due to timeout.")
			os.Exit(1)
		case runner.ErrorInterrupt:
			log.Println("Terminating due to interrupt.")
			os.Exit(2)
		}
	}

	log.Println("Process ended.")
}

func createTask()  func(int){
	return func (id int)  {
		log.Printf("Processor-task #%d.",id)
		time.Sleep(time.Duration(id)*time.Second)
	}
}

