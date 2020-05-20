package main

import (
	"log"
	"os"
	"io"
	"io/ioutil"
	)

var (
	Trace *log.Logger
	Info  *log.Logger
	Warn  *log.Logger
	Error *log.Logger
)


func init()  {
	// log.SetPrefix("TRACE: ") //设置前缀
	// log.SetFlags(log.Ldate | log.Lmicroseconds | log.Llongfile) //设置日志格式

	file,err := os.OpenFile("errors.txt",os.O_CREATE|os.O_WRONLY|os.O_APPEND,0666)
	if err!=nil{
		log.Fatalln("Failed to open error log file:",err)
	}

	Trace = log.New(ioutil.Discard,"TRACE: ",log.Ldate|log.Ltime|log.Lshortfile)
	Info = log.New(os.Stdout,"INFO: ",log.Ldate|log.Ltime|log.Lshortfile)
	Warn = log.New(os.Stdout,"WARN: ",log.Ldate|log.Ltime|log.Lshortfile)
	Error = log.New(io.MultiWriter(file,os.Stderr),"ERROR: ",log.Ldate|log.Ltime|log.Lshortfile)


}

func main() {
	// log.Println("std message") //标准日志记录器
	// log.Fatalln("fatal message") // 等于Println() + os.Exit(1)
	// log.Panicln("panic message") //等于Println() + panic-打印调用栈并os.Exit(2)
	Trace.Println("something standard.")
	Info.Println("something special.")
	Warn.Println("something warning.")
	Error.Println("something error.")
}