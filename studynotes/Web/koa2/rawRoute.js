const fs = require('fs')

const read = (view)=>{
    return new Promise((resolve,reject)=>{
        let viewUrl = `./views/${view}`
        fs.readFile(viewUrl,'binary',(err,data)=>{
            if(err){
                reject(err)
            } else {
                resolve(data)
            }
        })
    })
}

const route = async (url)=> {
    let view=null
    switch (url) {
        case '/':
            view = 'index.html'
            break;
        case '/index':
            view = 'index.html'
            break
        case '/404':
            view = '404.html'
            break
        default:
            view = 'index.html'
            break;
    }
    let html = await read(view)
    return html
}

module.exports = route