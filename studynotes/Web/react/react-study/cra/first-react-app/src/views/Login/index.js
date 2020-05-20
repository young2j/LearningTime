import React, { Component } from 'react'
import { connect } from 'react-redux'
import { Redirect } from 'react-router-dom'

import { Form, Icon, Input, Button, Checkbox,Card,Typography} from 'antd';

import './login.less'
import { login } from '../../actions'


const formItemLayout = {
    labelCol:{
        xs: { span: 24 },
        sm: { span: 8 },
        md:{span:4}
    },
    wrapperCol:{
        xs: { span: 24},
        sm: { span: 16},
        md: { span: 18},
    },
}


const mapStateToProps = state=>{
    return {
        user: state.user
    }
}

@connect(mapStateToProps,{login})
@Form.create()
class Login extends Component {
    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                values.authToken = '84a4B91E-CB15-1CcD-E352-7b73bBD6565b'
                // console.log(values);
                this.props.login(values)
            }
        });
    };

    render() {
        const { getFieldDecorator } = this.props.form;
        return (
            this.props.user.isLogin? 
            <Redirect to='/admin'/>
            :
            <Card title={
                <Typography.Title level={3}
                            style={{ textAlign: 'center' }}
                          >
                              欢迎登录
                          </Typography.Title>} 
                bordered={false} className='login-page'>
                                
                <Form onSubmit={this.handleSubmit} className="login-form" {...formItemLayout}>
                    <Form.Item label='用户名'>
                        {getFieldDecorator('username', {
                            rules: [{ required: true, message: 'Please input your username!' }],
                        })(
                            <Input
                                disabled={this.props.user.isLoading}
                                prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                placeholder="Username"
                            />,
                        )}
                    </Form.Item>
                    <Form.Item label='密码'>
                        {getFieldDecorator('password', {
                            rules: [{ required: true, message: 'Please input your Password!' }],
                        })(
                            <Input
                                disabled={this.props.user.isLoading}
                                prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                type="password"
                                placeholder="Password"
                            />,
                        )}
                    </Form.Item>
                    <Form.Item wrapperCol={{offset:4}}>
                        {getFieldDecorator('remember', {
                            valuePropName: 'checked',
                            initialValue: true,
                        })(<Checkbox>记住我</Checkbox>)}
                        <a className="login-form-forgot" href="#">
                            忘记密码？
                        </a>
                        <Button  loading={this.props.user.isLoading}
                          type="primary" htmlType="submit" className="login-form-button">
                            登录
                        </Button>
                            或者 <a href="#">立即注册！</a>
                    </Form.Item>
                </Form>
            </Card>
        );
    }
}

export default Login