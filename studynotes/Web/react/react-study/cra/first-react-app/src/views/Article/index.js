import React, { Component } from 'react'

import { 
    Card,
    Button,
    Table, 
    Tag,
    message, 
    Modal,
    Tooltip
} from 'antd'

import moment from 'moment'
import XLSX from 'xlsx'

import {getArticles,deleteArticle} from '../../requests'



const columnNames = {
    id:'编号',
    title:'标题',
    author:'作者',
    browseAmount:'浏览量',
    createAt:'创建时间',
    content:'文章内容',
    activeAt:'最近活动时间'
}


export default class Article extends Component {
    constructor(){
        super()
        this.state={
            dataSource: [],
            columns: [],
            total:0,
            isLoading:true,
            offset:0,
            limit:10,

            content:'',
            visible:false,
            okButtonProps:{loading:false},
            recordID:''
        }
    }


    toExcel=()=>{
        console.log(this.state.dataSource);
        const sheet = XLSX.utils.json_to_sheet(this.state.dataSource) //{header:Object.values(columnNames)}
        const wb = XLSX.utils.book_new()
        XLSX.utils.book_append_sheet(wb, sheet,'articles')
        XLSX.writeFile(wb, new Date().toLocaleDateString() + 'articles.xlsx')
    }

    deleteOK = ()=>{
        this.setState({
            okButtonProps:{loading:true},
        })
        deleteArticle(this.state.recordID)
          .then(resp=>{              
              message.success(resp.data.msg)
          })
          .then(
              ()=>this.setState({
                  visible:false,
                  okButtonProps:{loading:false}
              })
          )
          .finally(
              ()=>this.getData()
          )
    }

    deleteCancel =()=>{
        this.setState({
            visible:false
        })
    }
    deleteClick(record){
        this.setState({
            content: "《" + record.title + "》",
            visible: true,
            recordID:record.id
        })        
        // const modal = Modal.confirm({
        //     title: '你确定要删除：',
        //     content: "《"+record.title+"》",
        //     okText: '是的',
        //     okType: 'danger',
        //     cancelText: '按错了',
        //     closable:true,
        // })

        // modal.update({
        //     onOk() {
        //         modal.update({
        //             okButtonProps:{loading:true},
        //             visible:true
        //         })

        //         deleteArticle(record.id)
        //             .then(resp => {
        //                 message.success(resp.msg)
        //             })
        //     }
        // })
    }

    editClick = (record)=>{
        // this.props.history.push({
        //     pathname:`/admin/article/edit/${record.id}`,
        //     state:{
        //         title:record.title
        //     }
        // })
        this.props.history.push(`/admin/article/edit/${record.id}`)
            
    }

    getData = ()=>{
        getArticles()
            .then(resp => {                
                const columnKeys = Object.keys(resp.data.list[0])
                const columns = columnKeys.map(item=>{
                    if (item==='activeAt'){
                        return {
                                title: columnNames[item],
                                key: item,
                                render: (text, record) => {
                                        const { activeAt } = record
                                        return moment(activeAt).format('YYYY年MM月DD日 hh时mm分ss秒')
                                    }
                            }
                        }
                    if (item==='browseAmount'){
                        return  {
                            title: columnNames[item],
                            key: item,
                            render: (text, record)=>{
                                const {browseAmount} = record
                                return (
                                  <Tooltip 
                                     placement="topLeft" 
                                     title={browseAmount>5000? '>5000':'<5000'} 
                                     arrowPointAtCenter>
                                     <Tag color={browseAmount>5000? 'red':'green'}>{browseAmount}</Tag>
                                  </Tooltip>
                                )
                            }
                        }
                    }
                    return {
                        title:columnNames[item],
                        dataIndex:item,
                        key:item,
                        ellipsis: (item==='content')
                    }
                })
                
                columns.push({
                    title:'操作',
                    key:'operate',
                    render:(record)=> {
                        return (<Button.Group>
                                    <Button size='small' type='primary' onClick={this.editClick.bind(this,record)}>编辑</Button>
                                    <Button size='small' type='danger' onClick={this.deleteClick.bind(this,record)} >删除</Button>
                                </Button.Group>)
                    }
                }) //添加编辑列
                
                // console.log(columns);
                if (!this.updater.isMounted(this)) return //中断Ajax请求，组件被销毁就不能再setState了
                this.setState({
                    total: resp.data.total,
                    dataSource:resp.data.list,
                    columns:columns
                })
            })
            .catch(err=> message.error(err))
            .finally(()=>{
                this.setState({        
                    isLoading: false
                 })
                }
            )
    }

    pageChange = (page,pageSize)=>{
        this.setState({
            offset:pageSize*(page-1),
            limit:pageSize
        },()=>{
            this.getData()
        })
    }

    showSizeChange = (current,size)=>{
        this.setState({
            offset:0,
            limit:size
        },()=>{
            this.getData()
        })
    }

    componentDidMount(){
        this.getData()
    }

    render() {
     
        return (
            <Card 
              title="文章列表" 
              bordered={false}
              extra={<Button type='primary' onClick={this.toExcel}>导出Excel</Button>}
              >
                <Table 
                  dataSource={this.state.dataSource} 
                  columns={this.state.columns} 
                  pagination={{
                      current:this.state.offset/this.state.limit+1,
                      total:this.state.total,
                      hideOnSinglePage:true,
                      showQuickJumper:true,
                      showSizeChanger:true,
                      onChange:this.pageChange,
                      onShowSizeChange:this.showSizeChange,
                      pageSizeOptions:['10','20','30','50','100']
                  }}
                  rowKey={record=>record.id}
                  size='middle'
                  loading={this.state.isLoading}
                />
                <Modal
                    title='你确定要删除：'
                    okText='是的'
                    okType='danger'
                    cancelText='按错了'
                    visible={this.state.visible}
                    okButtonProps={this.state.okButtonProps}
                    onOk={this.deleteOK}
                    onCancel={this.deleteCancel}
                >
                    <p>{this.state.content}</p>
                </Modal>
            </Card>
            
        )
    }
}
