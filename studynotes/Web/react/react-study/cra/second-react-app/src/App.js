import React, { Component } from 'react'
import {Route,Switch} from 'react-router-dom'
import { Admin} from './pages'
import {ProductRoute,Routes} from './routes'


export default class App extends Component {
  render() {
    return (
      <Admin>
          <Switch>
            {
              ProductRoute.map(route=>{
              return <Route 
                        key={route.path} 
                        path={route.path} 
                        render={(routeProps)=>{
                          return <route.component {...routeProps}/>
                        }}/>
            })
          }
          {
            Object.values(Routes).map(route=>{
              return <Route key={route.path} path={route.path} component={route.component} />
            })
          }
          </Switch>
      </Admin>
    )
  }
}