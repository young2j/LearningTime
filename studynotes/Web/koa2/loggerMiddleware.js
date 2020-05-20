
// module.exports = async (ctx,next) =>{
//     console.log(ctx.method+'-'+ctx.url)
//     await next()
// }
// app.js
// app.use(logger)

module.exports = ()=>{
    return async (ctx,next) =>{
        console.log(ctx.method+'-'+ctx.url)
        console.log(ctx.request.url===ctx.url) //true
        await next()
    }
}

