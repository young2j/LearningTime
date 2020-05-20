import React, { Component } from 'react'
import { withRouter } from 'react-router-dom'
import {adminRouter} from '../../routes'
import { connect } from 'react-redux'

import { 
  Layout,
  Menu,
  Icon,
  Dropdown,
  Avatar,
  Badge
} from 'antd'

import logo from './logo.png'
import './frame.less'
import { getNotificationsList,logout } from '../../actions'


const { Header, Content, Sider } = Layout

const mapStateToProps = state=>{
  return {
    noticesNotReadCount:state.notifications.list.filter(item=>item.hasRead===false).length,
    user:state.user
  }
}



@connect(mapStateToProps,{getNotificationsList,logout})
@withRouter
class Frame extends Component {
   
  componentDidMount(){
    this.props.getNotificationsList()
  }

  handleMenuClick = ({ key })=>{
    // console.log({ item, key, keyPath, domEvent });
    if (key==='/login'){
      this.props.logout()
    } else{
      this.props.history.push(key)   
    }
  }
  render() {
    // console.log(this.props);
    
    const menus = adminRouter.filter(route => route.isNav === true)     
    return (
        <Layout style={{minHeight:'100%'}}>
          <Header className="header custom-header">
            <div className="logo custom-logo"> 
              <img src={logo} alt="logo"/>
            </div>
            <div>
              <Dropdown overlay={
                <Menu onClick={this.handleMenuClick}>
                  <Menu.Item key='/admin/notifications'>
                    <Badge dot={Boolean(this.props.noticesNotReadCount)}>
                    通知中心
                    </Badge> 
                  </Menu.Item>
                  <Menu.Item key='/admin/settings'>
                    个人设置
                  </Menu.Item>
                  <Menu.Item key='/login'>
                    退出登录
                  </Menu.Item>
                </Menu>
                }>
                <div style={{display:'flex',alignItems:'center'}}>
                  <Avatar src={this.props.user.avatar} /> 
                  <span>欢迎你，{this.props.user.username}</span>
                  <Badge count={this.props.noticesNotReadCount} offset={[-10,-8]}>
                  <Icon type="down" />
                  </Badge>                  
                </div>
              </Dropdown>
            </div> 
          </Header>
          <Layout>
            <Sider width={200} style={{ background: '#fff' }}>
              <Menu
                mode="inline"
                defaultSelectedKeys={this.props.location.pathname}
                onClick={this.handleMenuClick}
                style={{ height: '100%', borderRight: 0 }}
              >
                {
                  menus.map(item =>{
                    return (
                      <Menu.Item
                        key={item.pathname} 
                      ><Icon type={item.iconType} />
                        {item.title}
                      </Menu.Item>
                    )
                  })
                }
              </Menu>
            </Sider>
            <Layout style={{ padding: '16px' }}>
              <Content
                style={{
                  background: '#fff',
                  margin: 0,
                }}
              >
                {this.props.children}
              </Content>
            </Layout>
          </Layout>
        </Layout>
    )
  }
}

export default Frame