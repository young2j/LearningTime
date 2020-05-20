const Router = require('koa-router')

//子路由home
let home = new Router()
home.get('/index',async (ctx)=>{
    //获取get查询字符串
    method = ctx.method //===ctx.request.method
    url = ctx.url //===ctx.request.url
    query = ctx.query  //===ctx.request.query
    querystring = ctx.querystring //===ctx.request.querystring
    ctx.body = {
        method,
        url,
        query,
        querystring,
    }
}).get("/index/:id",async (ctx)=>{
    //获取get动态路由参数
    method = ctx.method
    url = ctx.url 
    params = ctx.params
    ctx.body = {
        method,
        url,
        params,        
    }
}).get("/form",async (ctx)=>{
    ctx.body = `
    <form action="/page/form" method='POST'>
        name:<input name="name" value="xxx" type="text">
        age:<input name="age" value="18" type="text">
        birth<input name="birth" value="2001" type="text">
        <button type='submit'>submit</button>
    </form>
    `
})

home.redirect('/','/index')




//子路由page
let page = new Router()
page.get('/404',async (ctx)=>{
    ctx.body = '找不着'
})

page.post('/form',async (ctx)=>{
    formData = ctx.request.body //获取formData
    ctx.body = formData
    //设置cookie
    ctx.cookies.set( //(name,value,options)
        'name',
        'xxx',
        {
            domain:'localhost', 
            path:'/page/form',//默认'/'
            maxAge: 10 * 60 * 1000, // cookie有效时长
            expires: new Date('2019-07-15'),  // cookie失效时间
            httpOnly: false,  // 是否只用于http请求中获取
            overwrite: false  // 是否允许重写
        }
    )
})



//装载所有子路由，加载在一个统一的router中
let router = new Router()
router.use(home.routes(),home.allowedMethods()) //不指定前缀
router.use('/page',page.routes(),page.allowedMethods()) //给page所有路由添加前缀/page



//最后在app中加载路由中间件
module.exports = router