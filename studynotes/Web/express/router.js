const express = require('express')
const router = express.Router()

//自定义路由中间件
//router level middleware
const timeLog = (req,res,next)=>{
    console.log('TimeNow:',Date.now())
    next()
}

router.use(timeLog) //未挂在path的中间件，对每一个请求都起作用
router.use((req, res, next)=> {
    if (!req.headers['x-auth']) return next('router') //next('router')将控制权交给下一个router实例，即跳出目前的router实例
    next()
  })


//定义路由
router.get('/',(req,res)=>{
    res.send('home page')
})

router.get('/user/:id',(req,res,next)=>{
    if(req.params.id==='0') next('route') //next('route')将控制权交给app.METHOD() or router.METHOD()中间件
    else next()
},(req,res,next)=>{
    res.send('user id is not 0')
})

router.get('/user/:id',(req,res,next)=>{
    res.send('user page')
})

router.get('/about',(req,res)=>{
    res.send('about page')
})


module.exports = router