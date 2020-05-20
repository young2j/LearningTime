import React, { Component,createRef } from 'react'
import { 
    Card,
    Row,
    Col
} from 'antd'

import echarts from 'echarts'


import './dashbord.less'

export default class DashBoard extends Component {
    constructor(){
        super()
        this.chartRef = createRef()
    }

    genChart = () => {
        this.chart = echarts.init(this.chartRef.current)

        // 指定图表的配置项和数据
        const option = {
            title: {
                text: 'ECharts 入门示例'
            },
            tooltip: {},
            legend: {
                data: ['销量']
            },
            xAxis: {
                data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
            },
            yAxis: {},
            series: [{
                name: '销量',
                type: 'bar',
                data: [5, 20, 36, 10, 10, 20]
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        this.chart.setOption(option);
    }
    
    componentDidMount(){
        this.genChart()
    }

    render() {

        // console.log('#' + (Math.random() * 0xffffff << 0).toString(16));
        
        return (
            <>
            <Card 
              title='概览'
              bordered={false}
            >
                <Row gutter={[32, 24]}>
                    <Col className='col-board'
                      span={6} 
                      offset={1} 
                      style={{backgroundColor:'#'+(Math.random()*0xffffff<<0).toString(16)}}>
                          1
                    </Col>
                    <Col className='col-board'
                      span={6} 
                      offset={1} 
                      style={{backgroundColor:'#'+(Math.random()*0xffffff<<0).toString(16)}}>
                          2
                    </Col>
                    <Col className='col-board'
                      span={6} 
                      offset={1} 
                      style={{backgroundColor:'#'+(Math.random()*0xffffff<<0).toString(16)}}>
                          3
                    </Col>
                </Row>
            </Card>
            <Card
                title='条形图'
                bordered={false}
            >            
              <div ref={this.chartRef} style={{height:'400px'}}/>
            </Card>
            </>
        )
    }
}
