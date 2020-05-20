const express = require('express')
const app = express()
const childrouter = require('./router')

//开放静态资源访问
//built-in level middleware
app.use('/static',express.static('public'))
app.use(express.static('files'))


//路由 
//application level middleware
app.get('/',(req,res)=>{
    data = {
        method: req.method,
        url:req.url,
        protocol:req.protocol
    }
    res.send(data)
})

app.post('/',(req,res)=>{})

app.all('/secret',(req,res,next)=>{
    console.log('secret section') 
    next() //pass control to the next handler
},(req,res)=>{
    res.send('get control from last handler')
})

app.get('/users/:userId/books/:bookId',(req,res)=>{
    res.send(req.params) //{userId:,bookId:}
})

let cb0 = (req,res)=>{next()}
let cb1 = (req,res)=>{next()}
let cb2 = (req,res)=>{}
app.get('/cb-array-like',[cb0,cb1,cb2])


//chainable route
app.route('/book')
  .get((req, res)=> {
    res.send('Get a random book')
  })
  .post((req, res)=> {
    res.send('Add a book')
  })
  .put((req, res)=> {
    res.send('Update the book')
  })

//加载子路由
app.use('/prefix',childrouter)

//error level middleware
app.use((err,req,res,next)=>{
    console.error(err.stack)
    // res.status(500).send('something broke!')
    next(err)
    //Notice that when not calling “next” in an error-handling function, 
    //you are responsible for writing (and ending) the response. 
    //Otherwise those requests will “hang” and will not be eligible for garbage collection.
})


app.listen(5000,()=>{
    console.log('server running on port 3000.')
})