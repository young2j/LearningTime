import axios from 'axios'

// export default function ajax(url,data={},method='GET'){
//     if (method==='GET'){
//         return axios.get(url,{
//             params:{
//                 ...data
//             }
//         })
//     } else {
//         return axios.post(url,data)
//     }
// }

const isDev = process.env.NODE_ENV === 'development'
const ajax = axios.create({
    baseURL: isDev ? 'http://rap2api.taobao.org/app/mock/236247' : ''
})



//----------用户登录----------
export const loginVerify = (userInfo) => {
    return ajax.post('/api/v1/login', userInfo)
}

