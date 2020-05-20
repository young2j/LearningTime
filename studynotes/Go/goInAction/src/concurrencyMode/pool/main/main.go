package main

import (
	"log"
	"io"
	"math/rand"
	"sync"
	"sync/atomic"
	"time"
	"concurrencyMode/pool"
)

const (
	maxGoroutines = 25
	pooledResources = 2
)

//共享资源
type dbConnection struct {
	ID int32
}

//Close 实现io.Closer
func (dbConn *dbConnection) Close() error  {
	log.Println("Close: Connection",dbConn.ID)
	return nil
}

//连接id
var idCounter int32

//需要时创建连接
func createConnection() (io.Closer,error)  {
	id := atomic.AddInt32(&idCounter,1)
	log.Println("Create: New Connection",id)

	return &dbConnection{id},nil
}

func main(){
	var wg sync.WaitGroup
	wg.Add(maxGoroutines)

	p,err := pool.New(createConnection,pooledResources)
	if err!=nil{
		log.Println(err)
	}

	for query:=0;query<maxGoroutines;query++{
		go func (q int)  {
			performQuery(q,p)
			wg.Done()
		}(query)
	}
	wg.Wait()

	log.Println("shutdown program.")
	p.Close()
}

func performQuery(query int,p *pool.Pool)  {
	conn,err := p.Acquire()
	if err!=nil{
		log.Println(err)
		return
	}
	
	defer p.Release(conn)

	//模拟查询等待
	time.Sleep(time.Duration(rand.Intn(1000))*time.Millisecond)
	log.Printf("QID[%d] CID[%d]\n",query,conn.(*dbConnection).ID)
}
