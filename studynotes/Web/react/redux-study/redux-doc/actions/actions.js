//Action 把数据从应用传到store。是 store 数据的唯一来源。
//通过 store.dispatch() 将 action 传到 store。
//Action 本质上是 JavaScript 普通对象。action 内必须使用一个字符串类型的 type 字段来表示将要执行的动作。

//*************String action******************
const ADD_TODO = 'ADD_TODO'

//Object action
export const ADD_TODO = {
    type: ADD_TODO,
    index: 1, //添加一个 action index 来表示用户完成任务的动作序列号, 通过下标 index 来引用特定的任务？？
    text: '除了 type 字段外，action 对象的结构完全自己决定'
}

//************function action******************
function addTodo(index){  //actionCreator
    return {
        type: ADD_TODO,
        index
    }
}
dispatch(addTodo(index))
//或
const boundAddTodo = index=> dispatch(addTodo(index)) //绑定function action 
boundAddTodo(index) //达到自动dispatch

/*
===>flux
function addTodo(index) {
    const action = {
        type: 'ADD_TODO',
        index
    }
    dispatch(action) //Flux 实现中，当调用 action 创建函数时，一般会像这样触发一个 dispatch    
}
*/

//react - redux 提供的 connect() 方法通过bindActionCreators() 可以自动把多个 action 创建函数 绑定到 dispatch() 方法上。

/*
 * action 类型
 */

export const ADD_TODO = 'ADD_TODO';
export const TOGGLE_TODO = 'TOGGLE_TODO'
export const SET_VISIBILITY_FILTER = 'SET_VISIBILITY_FILTER'

/*
* object action
*/
export const VisibilityFilters = {
    SHOW_ALL: 'SHOW_ALL',
    SHOW_COMPLETED: 'SHOW_COMPLETED',
    SHOW_ACTIVE: 'SHOW_ACTIVE'
}

/*
 * actionCreator
 */

export function addTodo(text) {
    return { type: ADD_TODO, text }
}

export function toggleTodo(index) {
    return { type: TOGGLE_TODO, index }
}

export function setVisibilityFilter(filter) {
    return { type: SET_VISIBILITY_FILTER, filter }
}