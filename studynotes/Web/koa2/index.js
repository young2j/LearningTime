const path = require('path')
const Koa = require('koa')
const app = new Koa()

// //静态资源加载服务
// const static = require('koa-static')
// app.use(static(
//     path.join(__dirname,"./views")
// ))




//form表单数据解析中间件——koa本身没有获取post请求form数据的api
const bodyparser = require('koa-bodyparser')
//bodyparser会将post请求的form数据解析到ctx.request.body中
app.use(bodyparser())




//自定义日志中间件
const logger = require('./loggerMiddleware')
//加载自定义日志中间件
app.use(logger())



//koa原生路由实现
// const rawRoute = require('./rawRoute')
//原生路由
/* app.use(async (ctx,next)=>{
    let url = ctx.request.url
    await next()
    let html = await rawRoute(url)
    ctx.body = html
}) 
*/


//第三方路由中间件
const router = require('./koaRouter')
//加载路由中间件
app.use(router.routes()).use(router.allowedMethods())



/* //--------------使用session----------------------
const session = require('koa-session-minimal')
const MysqlSession = require('koa-mysql-session')

// 配置存储session信息的mysql
let store = new MysqlSession({
  user: 'root',
  password: 'abc123',
  database: 'koa_demo',
  host: '127.0.0.1',
})

// 存放sessionId的cookie配置
let cookie = {
  maxAge: '', // cookie有效时长
  expires: '',  // cookie失效时间
  path: '', // 写cookie所在的路径
  domain: '', // 写cookie所在的域名
  httpOnly: '', // 是否只用于http请求中获取
  overwrite: '',  // 是否允许重写
  secure: '',
  sameSite: '',
  signed: '',

}

// 使用session中间件
app.use(session({
  key: 'SESSION_ID',
  store: store,
  cookie: cookie
}))
//------------------------------------ */



//----------------------------------
app.listen(3000,()=>{
    console.log("sever running on port 3000")
})

