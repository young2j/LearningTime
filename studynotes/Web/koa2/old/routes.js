/**
 * 嵌套路由
 */

const Router = require('koa-router')

const forums = new Router()
const posts = new Router()

posts.prefix('/posts')

posts.get('/', (ctx, next) => {
    //...
});
posts.get('/:pid', (ctx, next) => {
    //...
});

forums.use('/forums/:fid/posts', posts.routes(), posts.allowedMethods());


module.exports = forums