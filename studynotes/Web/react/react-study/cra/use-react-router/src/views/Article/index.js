import React, { Component } from 'react'
import { Link } from 'react-router-dom'

export default class Article extends Component {
    render() {
        return (
            <div>
                <Link to="/article/1">文章一</Link>
                <Link to={{
                    pathname: "/article/2",
                    state:{
                        from:'article'
                    }
                }}>文章二</Link>  
            </div>
        )
    }
}

//将to写为{}隐式传参，location会增加state参数：this.props.location.state
