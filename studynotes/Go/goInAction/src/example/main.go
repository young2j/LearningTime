package main
import (
	"log"
	"os"
	"example/matchers"
	"example/search"
)

func init(){
	log.SetOutput(os.Stdout)
}

func main(){
	search.Run("president")
}