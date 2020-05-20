import React, { Component } from 'react'
import { Empty } from 'antd'

export default class NoAccess extends Component {
    render() {
        return (
            <Empty style={{position:'relative',top:'25%'}}description='你没有权限查看'></Empty>
        )
    }
}
