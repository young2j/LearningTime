/*
runner模式：
	调度后台任务，监视程序执行时间。
*/

package runner

import (
	"os"
	"os/signal"
	"time"
	"errors"
)

type Runner struct {
	interrupt chan os.Signal //信号通道
	complete chan error  //错误通道，标识任务是否成功完成
	timeout <-chan time.Time //超时时间通道接收者
	tasks []func(int) //一组以索引顺序依次执行的函数
}

var ErrorTimeout = errors.New("received timeout.")

var ErrorInterrupt = errors.New("received interrupt.")

//构造Runner
func New(d time.Duration) *Runner {
	return &Runner{
		interrupt: make(chan os.Signal,1), //buffered channel
		complete: make(chan error), //unbuffered channel
		timeout: time.After(d), // time.After() 从通道中返回当前时间
	}
}

//添加一个任务——以int为ID的函数
func (r *Runner) Add(tasks ...func(int)){
	r.tasks = append(r.tasks,tasks...)
}

// 开启任务
func (r *Runner) Start() error {
	signal.Notify(r.interrupt,os.Interrupt) //接收所有中断信号

	//用不同的goroutine执行不同的任务
	go func() {
		r.complete <- r.run()
	}()

	//
	select {
		//当任务处理完成时发出信号
	case err:= <- r.complete:
		return err
		//当任务失败时发出信号
	case <- r.timeout:
		return ErrorTimeout	
	}
}

//运行任务
func (r *Runner) run() error{
	for id,task := range r.tasks {
		//检测中断信号
		if r.gotInterrupt(){
			return ErrorInterrupt
		}

		//执行任务
		task(id)
	}
	return nil 
}
//验证是否中断

func (r *Runner) gotInterrupt() bool{
	select {
		case <- r.interrupt:
			signal.Stop(r.interrupt) //停止接收后续信号
			return true
		
		default:
			return false
	}
}