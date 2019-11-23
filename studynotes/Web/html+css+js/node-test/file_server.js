'use strict'
var
    fs = require('fs'),
    url = require('url'),
    path = require('path'),
    http = require('http')

//file path
var root = path.resolve(process.argv[2] || '.')

console.log('Static root dir:'+ root)

// 创建服务器
var server = http.createServer(function (request,response) {
    var pathname = url.parse(request.url).pathname
    console.log('1:',request.url)
    console.log('2:',url.parse(request.url))
    console.log('3:',pathname)
    var filepath = path.join(root,pathname)
    console.log('4:',filepath)

    fs.stat(filepath,function(err,stats){
        if(!err && stats.isFile()) {
            console.log('200' + request.url)
            response.writeHead(200)
            fs.createReadStream(filepath).pipe(response) //response对象本身是一个Writable Stream
        } else {
            console.log('404' + request.url)
            response.writeHead('404')
            response.end('404 Not Found')
        }
    })
})

server.listen(8888)
console.log('Server is running at http://127.0.0.1:8888/')