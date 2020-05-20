import React, { Component } from 'react'
import * as actions from  '../../actions'


export default class CartList extends Component {
    constructor(){
        super()
        this.state={
            cartList:[]
        }
    }

    getState = () => {
        this.setState({
            cartList: this.props.store.getState().cart
        })
    }

    componentDidMount(){
        this.getState()
        this.props.store.subscribe(
            this.getState
        )
    }
    render() {            
        return (
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>名称</th>
                        <th>数量</th>
                        <th>单价</th>
                        <th>购买数量</th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {
                    this.state.cartList.map(item => {
                        return(
                            <tr key={item.id}>
                                <td>{item.id}</td>
                                <td>{item.name}</td>
                                <td>{item.amount}</td>
                                <td>{item.price}</td>
                                <td>{item.buy}</td>
                                <td>
                                    <button onClick={()=>this.props.store.dispatch(actions.add(item.id))}>+</button>
                                </td>
                                <td>
                                    <button onClick={() => this.props.store.dispatch(actions.sub(item.id))}>-</button></td>
                            </tr>
                            )
                        }
                    )
                }
                </tbody>
            </table>
        )
    }
}
