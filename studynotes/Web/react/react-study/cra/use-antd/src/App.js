import React, { Component } from 'react'
import { 
  Button,
  Spin,
  Timeline,
  Icon
} from 'antd'




export default class App extends Component {

  render() {
    return (
      <div>
          <Button type='primary'><Spin>点击按钮</Spin></Button>
        <Timeline>
          <Timeline.Item>Create a services site 2015-09-01</Timeline.Item>
          <Timeline.Item>Solve initial network problems 2015-09-01</Timeline.Item>
          <Timeline.Item dot={<Icon type="clock-circle-o" style={{ fontSize: '16px' }} />} color="red">
            Technical testing 2015-09-01
        </Timeline.Item>
          <Timeline.Item>Network problems being solved 2015-09-01</Timeline.Item>
        </Timeline>         
      </div>
    )
  }
}
