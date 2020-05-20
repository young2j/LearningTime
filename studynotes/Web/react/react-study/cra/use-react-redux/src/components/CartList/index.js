import React, { Component } from 'react'
// import * as actions from  '../../actions'
import { add,sub,subAsync } from '../../actions'
import { connect } from 'react-redux'

class CartList extends Component {

    render() {   
        console.log(this.props);
                 
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
                    this.props.cartList.map(item => {
                        return(
                            <tr key={item.id}>
                                <td>{item.id}</td>
                                <td>{item.name}</td>
                                <td>{item.amount}</td>
                                <td>{item.price}</td>
                                <td>{item.buy}</td>
                                <td>
                                    <button onClick={()=>this.props.add(item.id)}>+</button>
                                </td>
                                <td>
                                    <button onClick={() => this.props.subAsync(item.id)}>-</button></td>
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

const mapStateToProps = state => {
    // console.log('state:',state)
    return {
        cartList:state.cart 
    }
}

// const mapDispatchToProps = dispatch => {
//     return {
//         add: id=>dispatch(add(id)),
//         sub: id=>dispatch(sub(id))
//     }
// }
// export default connect(mapStateToProps,mapDispatchToProps)(CartList)


export default connect(mapStateToProps,{add,sub,subAsync})(CartList) 


//Provider 會給this.props附加store:undefined
//connect 會給this.props附加dispatch方法
//mapStateToProps 會給this.props附加reducer返回的New State
// mapDispatchToProps 會將附加給this.props的dispatch方法替換為具體的actions
//mapDispatchToProps 可直接傳入actions對象，內部自動dispatch