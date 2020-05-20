/*
pool:用于goroutine之间共享资源（比如数据库连接）
*/
package pool

import (
	"errors"
	"log"
	"io"
	"sync"
)

//共享资源池。被管理的资源必须实现io.Closer
type Pool struct {
	m 			sync.Mutex
	resources 	chan io.Closer
	factory		func() (io.Closer,error)
	closed 		bool
}

var ErrPoolClolsed = errors.New("Pool has been closed.")

//constructor
func New(fn func()(io.Closer,error), size uint) (*Pool,error) {
	if size<=0{
		return nil,errors.New("size value too small.")
	}

	return &Pool{
		factory: fn,
		resources: make(chan io.Closer,size),
	},nil
}


//从 Pool中请求一个资源
func (p *Pool) Acquire() (io.Closer,error) {
	select{
		//检查是否有空闲资源
	case r,ok := <- p.resources:
		log.Println("Acquire: Shared Resources.")
		if !ok {
			return nil,ErrPoolClolsed
		}
		return r,nil
		//无空闲资源，则请求新资源
	default:
		log.Println("Acquire: New Resources.")
		return p.factory()
	}
}

//将使用后的资源放回Pool
func (p *Pool) Release(r io.Closer)  {
	//保证本操作和close操作的安全
	p.m.Lock()
	defer p.m.Unlock()

	//如果Pool已关闭，则销毁资源
	if p.closed {
		r.Close()
		return
	}

	select {
		//资源放回队列
		case p.resources <- r:
			log.Println("Release: In Queue.")
		default:
			log.Println("Release: Closing")
			r.Close()
	}
}

//关闭Pool
func (p *Pool) Close()  {
	p.m.Lock()
	defer p.m.Unlock()

	if p.closed{
		return
	}

	p.closed = true

	close(p.resources) //清空通道资源前，先关闭通道，否则会发生死锁

	for r:= range p.resources{
		r.Close()
	}
}