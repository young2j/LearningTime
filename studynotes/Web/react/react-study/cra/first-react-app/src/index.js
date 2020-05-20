import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom'
import { Provider } from 'react-redux'

import App from './App';
import './index.less'
import { mainRouter } from './routes'
import store from './store'


ReactDOM.render(
    <Provider store={store}>
        <Router>
            <Switch>
                <Route path='/admin' render={(routerProps) => {
                    //render:to access verification
                    return <App {...routerProps} />
                }} />
                {
                    mainRouter.map(route => {
                        return <Route key={route.pathname} path={route.pathname} component={route.component} />
                    })
                }
                <Redirect to='/admin' from='/' exact/>
                <Redirect to='/404' />
            </Switch>
        </Router>
    </Provider>,
    document.getElementById('root')
)

