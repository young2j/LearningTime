import React, { Component } from 'react'
import { withRouter  } from 'react-router-dom'

class GoHomeButton extends Component {
    goHome = () => {
        this.props.history.push({
            pathname: '/home',
            state: {
                id: this.props.match.params.id
            }
        })
    }

    render() {
        console.log(this.props);        
        return (
            <div>
                <button onClick={this.goHome}>回到首页</button>
            </div>
        )
    }
}

export default withRouter(GoHomeButton)

//只有Route包裹的组件才会有相关的路由参数，这时使用withRouter可获得路由参数