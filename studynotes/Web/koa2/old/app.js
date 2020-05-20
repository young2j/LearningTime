const Koa = require('koa')
const Router = require('koa-router')
const forumsRouter = require('./routes')
/**
 * 实例app并设置属性:
 *  1.可将设置传递给构造函数。
 *  2.或可动态设置
 */
const app = new Koa({env:'development',proxy:true})
// app.proxy = true
const router = new Router({
    prefix:"/" //可设置统一url前缀
})


/**
 * 当一个中间件调用 next() 则该函数暂停并将控制传递给定义的下一个中间件。
 * 当在下游没有更多的中间件执行后，堆栈将展开并且每个中间件恢复执行其上游行为。
 */


//logger-middleware1
app.use(async (ctx,next)=>{
    await next() //暂停，控制权交由middleware2
    const rt = ctx.response.get("X-Response-time")
    console.log(`${ctx.method} ${ctx.url} - ${rt}`)
})


//set resptime-middleware2
app.use(async (ctx,next)=>{
    const start = Date.now()
    await next() //暂停，控制权交由middleware3
    const ms = Date.now()-start
    ctx.set('X-Response-Time',`${ms}ms`)
})


//response-middleware3
app.use(async ctx=>{
    ctx.body = "hello world."
})


//404-custom middleware4
app.use(async function pageNotFound(ctx,next){
    ctx.status = 400
    switch (ctx.accepts('html','json')) {
        case 'html':
            ctx.type = 'html'
            ctx.body = '<p>Page Not Found</p>'
            break;
        case 'json':
            ctx.body = {
                message: 'Page Not Found.'
            }
        default:
            ctx.type = 'text'
            ctx.body = 'Page Not Found.'
            break;
    }
})

//错误处理
app.on('error',(err,ctx)=>{
    console.log('server error',err,ctx)
})


//-------router--------------
//命名路由，可以快速复用router.url('root','user')=>"/root/user"
// router.url('user', { id: 3 }, { query: "limit=1" }) => "/users/3?limit=1"

router.get('root','/',(ctx,next)=>{
        ctx.body = 'hello world!.'
    })     
    .post('/users?name=xxx',(ctx,next)=>{
        ctx.query //{name:"xxx"}
        ctx.querystring //"name=xxx"
    })
    .put('/users/:id',(ctx,next)=>{
        return User.findOne(ctx.params.id).then(user=>{
                ctx.user = user
                next()
            })
        },
        ctx=>{
            console.log(ctx.user) 
        }
    ) //multiple middleware
    .del('/users/:id',(ctx,next)=>{
        //...
    })
    .all('/users/:id',(ctx,next)=>{
        //...
    })
//-------redirect
router.redirect('/login','/sign-in')
router.all('/login',(ctx,next)=>{
    ctx.redirect('/sign-in')
    ctx.status = 301
})
//-----------

//router middleware
router.use(session())
      .use(authorize())
router.use('/users',userAuth())
router.use(['/users','/admin'],userAuth())

//app加载路由中间件
app.use(router.routes())
    .use(router.allowedMethods()) 
//app加载子路由,也可由router加载
app.use(forumsRouter.routes())

//-----------------------


//port
const port = process.env.PORT || 3000
//是http.createServer(app.callback()).listen(3000)的语法糖
app.listen(port)

