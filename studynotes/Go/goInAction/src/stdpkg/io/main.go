package main

import (
	"fmt"
	"bytes"
	"os"
)

func main() {
	var b bytes.Buffer
	b.Write([]byte("hello "))
	fmt.Fprintf(&b,"world.") //字符串拼接
	b.WriteTo(os.Stdout)
}