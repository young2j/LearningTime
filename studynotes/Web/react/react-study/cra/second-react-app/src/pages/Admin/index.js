import React, { Component } from 'react'
import { Redirect } from 'react-router-dom'
import { Layout} from 'antd';


import storageUtils from '../../utils/storageUtils'
import { LeftNav,Header } from '../../components'


const {Content, Sider,Footer} = Layout;



export default class Admin extends Component {
    componentDidMount(){

    }
    render() {
        const hasUserInfo = storageUtils.getUser()
        if (!hasUserInfo) {
            return <Redirect to='/login' />
        }

        return (
                <Layout style={{height:"100%"}}>
                  <Sider >
                    <LeftNav/>    
                  </Sider>
                  <Layout>
                     <Header/>
                      <Content style={{backgroundColor:"#fff"}}>{this.props.children}</Content>
                     <Footer style={{textAlign:"center"}}>&copy;React+Redux+Axios开发SPA应用</Footer>
                  </Layout>
                </Layout>
        )
    }
}
