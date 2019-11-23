import { createStore } from 'redux'
import todoAPP from './reducers'
import {
    addTodo,
    toggleTodo,
    setVisibilityFilter,
    VisibilityFilters
} from './actions/actions'

//let store = createStore(reducer, window.STATE_FROM_SERVER)

let store = createStore(todoAPP)

//打印初始状态
console.log(store.getState())

// subscribe(listener) 注册监听器;返回一个函数就注销监听器
const unsubscribe = store.unsubscribe( ()=>{
    console.log(store.getState())
})

//发起一系列action
store.dispatch(addTodo('text'))
store.dispatch(toggleTodo(0))
store.dispatch(setVisibilityFilter(VisibilityFilters.SHOW_COMPLETED))

//停止监听state更新
unsubscribe()