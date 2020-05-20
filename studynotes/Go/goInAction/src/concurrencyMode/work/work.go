/*
work：
	使用无缓冲通道并发控制一组工作
*/

package work

import (
	"sync"
)

//worker必须满足接口类型才能使用工作池。
type Worker interface {
	Task()
}

//pool提供一个goroutine池，可以完成任意提交的Worker任务
type Pool struct {
	work chan Worker
	wg sync.WaitGroup
}

func New(maxGoroutines int) *Pool {
	p := Pool{
		work: make(chan Worker),
	}
	p.wg.Add(maxGoroutines)

	for i:=0;i<maxGoroutines;i++{
		go func ()  {
			for w:=range p.work {
				w.Task()
			}
			p.wg.Done()	
		}()
	}

	return &p
}


//提交工作到工作池
func (p *Pool) Run(w Worker) {
	p.work <- w
}

//停止工作
func (p *Pool) Shutdown() {
	close(p.work)
	p.wg.Wait()
}