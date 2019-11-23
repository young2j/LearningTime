// import React from 'react'
// import ReactDOM from 'react-dom'
// import { Provider } from 'react-redux'
// import { createStore } from 'redux'
// import rootReducer from './reducers'
// import App from './App'
// import {
//     Router, Route
// } from 'react-router'

// import {createBrowserHistory} from 'history'
// import {syncHistoryWithStore} from 'react-router-redux'

// let store = createStore(rootReducer)
// const browerHistory = createBrowserHistory()
// const history = syncHistoryWithStore(browerHistory,store)

// ReactDOM.render(
//     <Provider store={store}>
//         <Router history={history}>
//             <Route path="/(:filter)" component={App}/>
//         </Router>
//     </Provider>,
//     document.getElementById('root')
// )

import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import { createStore } from 'redux'
import rootReducer from './reducers'
import App from './App'



let store = createStore(rootReducer)


ReactDOM.render(
    <Provider store={store}>
        <App/>
    </Provider>,
    document.getElementById('root')
)