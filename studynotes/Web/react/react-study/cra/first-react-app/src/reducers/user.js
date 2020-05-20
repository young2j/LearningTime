import actionTypes from "../actions/actionTypes"

const userInfo = JSON.parse(window.localStorage.getItem('userInfo')) || 
                 JSON.parse(window.sessionStorage.getItem('userInfo'));
const initState={
    id:'',
    username:userInfo===null? '':userInfo.username,
    avatar:userInfo===null? '':userInfo.avatar,
    role: userInfo === null ? '' : userInfo.role,
    isLogin:Boolean(userInfo),
    isLoading:false
}

export default (state=initState,action)=>{
    switch(action.type){
        case actionTypes.START_LOGIN:
            return {
                ...state,
                isLoading:true
            }
        case actionTypes.LOGIN_SUCCESS:
            return {
                ...state,
                ...action.payload,
                isLoading:false,
                isLogin:true
            }
        case actionTypes.LOGIN_FAILED:
            return initState

        case actionTypes.LOGOUT:
            return {
                ...state,
                isLogin:false
            }
        default:
            return state
    }
}