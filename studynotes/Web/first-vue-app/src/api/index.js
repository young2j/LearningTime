import axios from 'axios'
import { Loading, Message } from 'element-ui'
import router from '../router'

let loading
const startLoading = () => {
  loading = Loading.service({
    lock: true,
    text: '拼命加载中...',
    background: 'rgba(0, 0, 0, 0.6)'
  })
}

const endLoading = () => {
  loading.close()
}

// 请求拦截
axios.defaults.baseURL = 'http://rap2api.taobao.org/app/mock/244873'
axios.interceptors.request.use(config => {
  startLoading()
  if (localStorage.Token) {
    config.headers.Authorization = localStorage.Token
  }
  return config
}, err => {
  return Promise.reject(err)
})

// 响应拦截
axios.interceptors.response.use(response => {
  endLoading()
  return response.data
}, err => {
  endLoading()
  Message.error(err.response.data)
  // 错误跳转
  const { status } = err.response
  if (status === 401) {
    Message.error('Token失效，请重新登录.')
    localStorage.removeItem('Token')
    router.push('/login')
  }
  return Promise.reject(err)
})

export default axios
