import React, { Component } from 'react'
import {
    Card,
    List,
    Avatar,
    Button,
    Badge,
    Spin
} from 'antd'

import { connect } from 'react-redux'
import {markNotificaion,markAllNotificaion} from '../../actions'




const mapStateToProps = state=>{
    return {
        notices: state.notifications,
    }
}



@connect(mapStateToProps,{markNotificaion,markAllNotificaion})
class Notifications extends Component {


    
    render() {
        // console.log(this.props.notices.isLoading);

        return (
        <Spin spinning={this.props.notices.isLoading}>
          <Card 
              title="通知中心"
              bordered={false}
              extra={
                <Button 
                 onClick={this.props.markAllNotificaion}                
                 disabled={this.props.notices.list.every(item=>item.hasRead===true)}
                >
                 全部标记为已读
                </Button>}
            >
            <List
                itemLayout="horizontal"
                dataSource={this.props.notices.list}
                renderItem={item => (
                    <List.Item 
                      extra={
                          item.hasRead ? 
                          null:<Button onClick={this.props.markNotificaion.bind(this,item.id)}>
                                标记为已读
                               </Button>
                            }
                        >
                        <List.Item.Meta
                            avatar={<Avatar src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png" />}
                            title={<Badge dot={!item.hasRead}>{item.title}</Badge>}
                            description={item.description}
                        />
                    </List.Item>)}
            />
          </Card>
          </Spin>
        )
    }
}

export default Notifications