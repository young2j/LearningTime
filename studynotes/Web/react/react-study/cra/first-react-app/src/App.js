import React, { Component } from 'react'
import { Route, Switch, Redirect } from 'react-router-dom'
import { connect } from 'react-redux'

import { adminRouter } from './routes'
import { Frame } from './components'

const mapStateToProps = state=>{
  return {
    user:state.user
  }
}

@connect(mapStateToProps)
class App extends Component {

  render() {
    return (
      this.props.user.isLogin?
      <Frame>
        <Switch>
          {
            adminRouter.map(route => {
              return (
                <Route
                key={route.pathname}
                path={route.pathname}
                exact={route.exact}
                render={(routeProps) => {
                  const hasAccess = route.roles.includes(this.props.user.role)
                  return  hasAccess? <route.component {...routeProps} />: <Redirect to='/admin/noaccess'/>
                }} />
                )
              })
            }
          
          <Redirect to={adminRouter[0].pathname} from='/admin' exact/>
          <Redirect to='/404' />
        </Switch>
      </Frame>
      : 
      <Redirect to='/login' />
    )
  }
}

export default App