import {combineReducers} from 'redux'
import { 
    ADD_TODO, 
    TOGGLE_TODO, 
    SET_VISIBILITY_FILTER, 
    VisibilityFilters 
} from '../actions/actions';

/*
   reducer: function (previousState,action) => newState
1。 保持 reducer 纯净非常重要。永远不要在 reducer 里做这些操作：

    修改传入参数；
    执行有副作用的操作，如 API 请求和路由跳转；
    调用非纯函数，如 Date.now() 或 Math.random()。

2. 在 Redux 应用中，所有的 state 都被保存在一个单一对象中。
3.  注意:
    1.不要修改 state。
    2.在 default 情况下返回旧的 state。遇到未知的 action 时，一定要返回旧的 state。
*/


/*  用一个reducer更新state整体
const initState = {
    visibilityFilter: 'SHOW ALL',
    todos: [
        {
            text: 'consider using redux',
            completed: true
        },
        {
            text: 'keep all state in a single tree',
            completed: false
        }
    ]
}

function toDoReducer(state = initState, action) {
    switch (action.type) {
        case SET_VISIBILITY_FILTER:
            return Object.assign({}, state, {
                visibilityFilter: action.filter
            })
        case ADD_TODO:
            return Object.assign({}, state, {
                todos: [
                    ...state.todos,
                    {
                        text: action.text,
                        completed: false
                    }
                ]
            })
        case TOGGLE_TODO:
            return Object.assign({}, state, {
                todos: state.todos.map((todo, index) => {
                    if (index === action.index) {
                        return Object.assign({}, todo, {
                            completed: !todo.completed
                        })
                    }
                    return todo
                })
            })
        default:
            return state
    }
}
 */

 // 分解reducer，每个 reducer 只负责管理全局 state 中的一部分
const {SHOW_ALL} = VisibilityFilters

function visibilityFilter(state=SHOW_ALL,action){
    switch (action.type) {
        case SET_VISIBILITY_FILTER:
            return action.filter
        default:
            return state
    }
}

function todos(state=[],action){
    switch (action.type) {
        case ADD_TODO:
            return [
                ...state,
                {
                    text:action.text,
                    completed:false
                }
            ]
        
        case TOGGLE_TODO:
            return state.map((todo,index) => {
                if (index===action.index) {
                    return Object.assign({},todo,{
                        completed:!todo.completed
                    })
                }
                return todo
            })
        default:
            return state
    }
}

const todoApp = combineReducers({
    visibilityFilter,
    todos
})

export default todoApp

//等价于
// export default function todoApp(state={},action){
//     return {
//         visibilityFilter: visibilityFilter(state.visibilityFilter,action),
//         todos: todos(state.todos,action)
//     }
// }
