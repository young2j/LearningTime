import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router,Route,Switch,Redirect } from 'react-router-dom'

import App from './App';
import './index.less'
import {mainRouter} from './routes'


ReactDOM.render(
    <Router>
        <Switch>
            <Route path='/' render={(routerProps)=>{
                //render:to access verification
                return <App {...routerProps} />
            }} />
            {
                mainRouter.map(route=>{
                    return <Route key={route.pathname} path={route.pathname} component={route.component} />
                })
            }
            <Redirect from='/' to='/admin' exact/>
            <Redirect to='/404'/>
        </Switch>
    </Router>,
    document.getElementById('root')
)

