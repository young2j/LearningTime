import actionTypes from './actionTypes'
import {getNotifications,loginVerify} from '../requests'


//-----------------------------通知中心----------------------
const startMark = ()=>{
    return {
        type: actionTypes.START_MARK
    }
}

const finishMark =()=>{
    return {
        type:actionTypes.FINISH_MARK
    }
}


export const markNotificaion = id=>dispatch=>{
    dispatch(startMark())
    setTimeout(
        ()=>{ 
          dispatch({
            type:actionTypes.MARK_NOTIFICATION,
            payload:{
                id
            }
          })
         dispatch(finishMark())
        },1000)
}


export const markAllNotificaion = ()=>dispatch=>{
    dispatch(startMark())
    setTimeout(
        () => {
            dispatch({
                 type: actionTypes.MARK_ALL_NOTFICATIONS,
                })
            dispatch(finishMark())
        }, 1000)
}


export const getNotificationsList = ()=>dispatch=>{
    dispatch(startMark())
    getNotifications()
      .then(resp=>{
          dispatch({
              type:actionTypes.GET_NOTIFICATIONS_LIST,
              payload:resp.list
          })
          dispatch(finishMark())
      })
}

//-------------------登录页---------------------

export const loginStart = ()=>{
    return {
        type:actionTypes.START_LOGIN
    }
}
// export const loginSuccess = ()=>{
//     return {
//         type:actionTypes.LOGIN_SUCCESS
//     }
// }
export const loginFailed = ()=>{
    window.localStorage.removeItem('userInfo')
    window.sessionStorage.removeItem('userInfo')


    return {
        type:actionTypes.LOGIN_FAILED
    }
}

export const login=(userInfo)=>dispatch=>{
    dispatch(loginStart())
    loginVerify(userInfo)
      .then(resp=>{
          if (resp.code===200){
              if (userInfo.remember){
                  window.localStorage.setItem('userInfo', JSON.stringify(resp.data))
              } else {
                  window.sessionStorage.setItem('userInfo', JSON.stringify(resp.data))
              }
              dispatch({
                  type:actionTypes.LOGIN_SUCCESS,
                  payload:resp.data
              })
          } else{
              dispatch(loginFailed())
          }
      })

}

export const logout = ()=> dispatch=>{
    dispatch({
        type:actionTypes.LOGOUT
    })
}