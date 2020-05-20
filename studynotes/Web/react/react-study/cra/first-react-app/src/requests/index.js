import axios from 'axios'
import { message } from 'antd'



const isDev = process.env.NODE_ENV==='development'
const service = axios.create({
    baseURL: isDev ? 'http://rap2api.taobao.org/app/mock/236247':''
})

service.interceptors.request.use((config)=>{
    // console.log('config:',config);
    config.data = Object.assign({}, config.data,{
        // authToken:window.localStorage.getItem('authToken')
        authToken:'123'
    })
    
    return config
})

service.interceptors.response.use((resp)=>{
    // console.log('resp:',resp)
    if (resp.data.code===200){
        return resp.data
    }else{
        message.error(resp.data.errMsg)
    }
})

//-------------获取文章列表------------------
export const getArticles = (offset=0,limit=10) =>{
    return service.get('/api/v1/articleList',{
        offset,
        limit
    })
}

//-----------删除文章---------------
export const deleteArticle=(id)=>{
    return service.delete(`/api/v1/article/${id}`)
}

//----------获得一篇文章------------
export const getOneArticle=(id)=>{
    return service.get(`/api/v1/article/${id}`)
}

//----------修改一篇文章------------
export const modifyOneArticle=(id,formData)=>{
    return service.post(`/api/v1/article/${id}`,formData)
}

//---------获得通知消息----------
export const getNotifications=()=>{
    return service.get('/api/v1/notifications')
}

//----------用户登录----------
export const loginVerify=(userInfo)=>{
    return service.post('/api/v1/login',userInfo)
}