// var http = require('http');
// http.createServer(function(request,response){
// 	response.writeHead(200,{'Content-Type':'text/plain'});
// 	response.end('Hello world\n');
// }).listen(8888);
// console.log('sever running at http://127.0.0.1:8888/')

//阻塞式
var fs = require('fs');
var data = fs.readFileSync('text.txt');
console.log(data.toString());

// 非阻塞
var fs = require('fs');
fs.readFile('text.txt',function(err,data){
	if (err) return console.error(err);
	console.log(data.toString());
})