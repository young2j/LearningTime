package main

import (
	"encoding/json"
	"fmt"
	"log"
	// "net/http"
)

type (
	gResult struct {
		GsearchResultClass string `json:"GsearchResultClass"` //tag:将json文档与结构类型的字段一一映射起来
		UnescapedURL	   string `json:"unescapedUrl"`
		URL				   string `json:"url"`
		VisibleURL		   string `json:"visibleUrl"`
		CachedURL 		   string `json:"cachedURL"`
		Title			   string `json:"title"`
		TitleNoFormatting  string `json:"titleNoFormatting"`
		Content			   string `json:"content"`
	}

	gResponse struct {
		ResponseData struct {
			Result []gResult `json:"results"`
		} `json:"responseData"`
	}
)

//string形式存在的json，需要将string转换为[]byte,并用json.Unmarshal进行反序列化
var JSON = 	`{
	"GsearchResultClass": "GsearchResultClass",
	"UnescapedURL": "unescapedUrl",
	"URL": "url",
	"VisibleURL": "visibleUrl",
	"CachedURL": "cachedURL",
	"Title": "title",
	"TitleNoFormatting": "titleNoFormatting",
	"Content": "content"
}`


func main()  {
	uri := "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=8&q=golong"

	resp,err := http.Get(uri)
	if err!=nil{
		log.Println("ERROR:",err)
		return
	}

	defer resp.Body.Close()
	
	var gr gResponse
	err = json.NewDecoder(resp.Body).Decode(&gr) //将google返回的json数据解码到gr变量
	if err!=nil{
		log.Println("ERROR:",err)
		return
	}
	fmt.Println(gr)

	//----------------------解码
	var strjson gResult
	//或声明为一个map
	// var strjson map[string]interface{} //go中任何类型都实现了一个空接口
	e := json.Unmarshal([]byte(JSON),&strjson)
	if e!=nil{
		log.Println("ERROR:",e)
		return
	}
	fmt.Println(strjson)

	//--------------------编码
	data,er := json.MarshalIndent(strjson,"","	") //(interface{},prefix,indent)=>[]byte,error
	if er!=nil{
		fmt.Println("ERROR:",er)
		return
	}
	fmt.Println(string(data))
}