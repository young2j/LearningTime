import React, { Component } from 'react'
import { Form, Icon, Input, Button,message} from 'antd'

import './login.less'
import logo from '../../assets/images/logo.png'
import {loginVerify} from '../../api'
import storageUtils from '../../utils/storageUtils'

@Form.create()
class Login extends Component {

    validateUserName = (rule,value,callback) => {
        if (value.length>12){
            callback('用户名最长12位')
        } else if (value.length<6) {
            callback("用户名至少6位")
        }
        callback() //验证通过    
    }
    

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields(async (err, values) => {
            if (!err) {
               const resp = await loginVerify(values)
                if (resp.status===200){
                    storageUtils.saveUser(resp.data.data)
                    this.props.history.replace('/')
                    message.success("登陆成功")
                } else {
                        message.error('登录失败')
                    }
                }
            })
    };
    render() {
        // console.log(this.props);
        
        const {getFieldDecorator} = this.props.form
        return (
            <div className='login'>
                <header className="login-header">
                    <img src={logo} alt="logo"/>
                </header>
                <section className="login-frame">
                <Form onSubmit={this.handleSubmit} className="login-form">
                    <h2>用户登录</h2>
                    <Form.Item>
                      {getFieldDecorator('username', {
                          rules: [
                              { required: true, 
                                message: 'Please input your username!' 
                              },{
                                  validator:this.validateUserName
                              }
                            ]
                      })(
                          <Input
                          prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                          placeholder="用户名"
                          />,
                      )}
                    </Form.Item>
                    <Form.Item>
                      {getFieldDecorator('password', {
                          rules: [
                              { 
                                  required: true, 
                                  message: 'Please input your Password!' 
                                },{
                                    min:4,
                                    message:'密码最少四位'
                                },{
                                    max:12,
                                    message:"密码最多12位"
                                },{
                                    pattern:/^[0-9A-Za-z_]+$/,
                                    message:"密码只能为数字、字母与下划线"
                                }
                            ],
                      })(
                          <Input
                          prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                          type="password"
                          placeholder="密码"
                          />,
                      )}
                    </Form.Item>
                    <Form.Item>
                      <Button type="primary" htmlType="submit" className="login-form-button">
                        登录
                      </Button>
                    </Form.Item>
                </Form>
                </section>
            </div>
        )
    }
}

export default Login