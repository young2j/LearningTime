import React, { Component,createRef } from 'react'
import {
    Card,
    Button,
    Form,
    Icon,
    Input,
    DatePicker,
    message,
    Spin
    } from 'antd'

import E from 'wangeditor'
import moment from 'moment'

import './editor.less'
import { getOneArticle,modifyOneArticle } from '../../requests'


@Form.create()
class Edit extends Component {
    constructor(){
        super()
        this.editorRef = createRef()
        this.state = {
            isLoading:true
        }
    }
    
    handleSubmit = e => {
        e.preventDefault()

        this.props.form.validateFields((err,values)=>{
            if (!err) {
                const formData = Object.assign({}, values,{
                    createAt: values.createAt.valueOf(),
                    activeAt: values.activeAt.valueOf(),
                })

                this.setState({
                    isLoading: true
                })
                modifyOneArticle(this.props.match.params.id,formData)
                  .then(resp=>{
                    if (resp.code===200){
                        message.success(resp.msg)
                    }
                  })
                  .catch(err=>{
                      message.error(`修改失败:${err}`)
                  })
                  .finally(
                      ()=>this.setState({
                          isLoading:false
                      })
                  )
            }
        })
    }

    onChange = (date, dateString) =>{
        console.log(date, dateString);
    }        
    
    mountEditor = () => {
        this.editor = new E(this.editorRef.current)
        this.editor.customConfig.onchange = (html)=>{
            this.props.form.setFieldsValue({
                content:html
            })      
        }
        this.editor.create()
    }
    
    componentDidMount(){
        this.mountEditor()
        getOneArticle(this.props.match.params.id)
          .then(resp=>{
              const {id,...data} =resp.data
              data.createAt = moment(data.createAt)
              data.activeAt = moment(data.activeAt)
              this.props.form.setFieldsValue(data)
              this.editor.txt.html(resp.data.content)
          })
          .finally(()=>
            this.setState({
              isLoading:false
          })
          )
    }

    render() {
        const {getFieldDecorator} = this.props.form
        const formItemLayout = {
            labelCol: {
                xs: { span: 24 },
                sm: { span: 5 },
            },
            wrapperCol: {
                xs: { span: 24 },
                sm: { span: 15 },
            },
        }
        // console.log(this.props.form);
        

        return (
            <Spin spinning={this.state.isLoading}>
            <Card 
              title='编辑文章'
              bordered={false}
              extra={
                  <div>
                    <Button type="primary" ghost onClick={this.handleSubmit}>保存</Button>&emsp;
                    <Button type="danger" ghost onClick={this.props.history.goBack}>取消</Button>
                  </div>
                }
            >
                <Form {...formItemLayout} onSubmit={this.handleSubmit} className="login-form">
                    <Form.Item label='标题' layout='inline'>
                        {getFieldDecorator('title', {
                            rules: [
                                { required: true, 
                                  message: '必须输入标题!' 
                                },{
                                    min:4,
                                    message:'文章标题至少4位'
                                }
                                
                            ],
                            initialValue:'论帅哥的自我修养'
                        })(
                            <Input
                                prefix={<Icon type="highlight" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                placeholder="Title"
                            />
                        )}
                    </Form.Item>
                    <Form.Item label='作者'>
                        {getFieldDecorator('author', {
                            rules: [
                                { 
                                  required: true,
                                  message: '请输入作者姓名!',
                                }
                            ],
                            initialValue:'帅哥'
                        })(
                            <Input
                                prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                type="text"
                                placeholder="Author"
                            />,
                        )}
                    </Form.Item>
                    <Form.Item label='浏览量'>
                        {getFieldDecorator('browseAmount', {
                                initialValue: '0'
                            })(
                                <Input
                                    prefix={<Icon type="eye" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                    placeholder="0"
                                />
                            )}
                    </Form.Item>
                    <Form.Item label='创建时间'>
                        {getFieldDecorator('createAt', {
                            rules: [
                                    { 
                                        required: true,
                                        message: '请选择创建时间',
                                    }
                                ],
                                initialValue: moment(new Date().getTime())
                            })(
                                <DatePicker showTime onChange={this.onChange} />,
                            )}
                    </Form.Item>
                    <Form.Item label='修改时间'>
                        {getFieldDecorator('activeAt', {
                            rules: [
                                    { 
                                        required: true,
                                        message: '请选择修改时间',
                                    }
                                ],
                                initialValue: moment(new Date().getTime())
                            })(
                                <DatePicker showTime onChange={this.onChange} />,
                            )}
                    </Form.Item>
                    <Form.Item label='文章内容'>
                        {getFieldDecorator('content', {
                            rules: [
                                {
                                    required: true,
                                    message: '',
                                },{
                                    min:50,
                                    message:'文章内容至少50个字！'
                                }
                            ],
                        })(
                            // <textarea name="" id="" cols="30" rows="10" placeholder='文章内容'></textarea>
                            // <div contentEditable
                            //   style={{
                            //       border:'1px solid #dedede',
                            //       height:'200px',
                            //       minHeight:'100px'}}>
                            // </div>
                            <div className='wang-editor' ref={this.editorRef}></div>
                        )}
                    </Form.Item>
                    <Form.Item wrapperCol={{offset:5}}>
                        <Button type="primary" htmlType="submit" className="login-form-button">
                            保存修改
                        </Button>
                    </Form.Item>
                </Form>
            </Card>
            </Spin>
        )
    }
}

export default Edit
