import React, { Component } from 'react'
import { Menu,Icon } from 'antd'
import { Link,withRouter} from 'react-router-dom'

import './index.less'
import logo from '../../assets/images/logo.png'

const {SubMenu} = Menu;

@withRouter
class LeftNav extends Component {

    menuClick = ({key}) => {
        
        this.props.history.push(key)
    }
    

    render() {
        // console.log(this.props);
        
        return (
            <div className='left-nav'>
                <div className='left-nav-header'>
                    <Link to='/admin/home'><img src={logo} alt="logo"/></Link>
                </div>
                <Menu defaultSelectedKeys={['/admin/home']} 
                        mode="inline" 
                        onClick={this.menuClick}
                >
                    <Menu.Item key='/admin/home'>
                        <Icon type='home'/>
                        <span>首页</span>
                    </Menu.Item>
                    <SubMenu
                    key="/admin/product"
                    title={
                        <span>
                        <Icon type="user" />
                        <span>商品</span>
                        </span>
                    }
                    >
                    <Menu.Item key="/admin/product/category">品类管理</Menu.Item>
                    <Menu.Item key="/admin/product/goods">商品管理</Menu.Item>
                    </SubMenu>
                    <Menu.Item key="/admin/user">
                    <Icon type="user" />
                    <span>用户</span>
                    </Menu.Item>
                    <Menu.Item key="/admin/role">
                    <Icon type="team" />
                    <span>角色</span>
                    </Menu.Item>
                </Menu>
            </div>
        )
    }
}

export default LeftNav