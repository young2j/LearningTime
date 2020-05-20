import React, { Component } from 'react'
import CartList from './components/CartList'

export default class App extends Component {
    
    render() {
        return (
            <div>
               <CartList store={this.props.store}/> 
            </div>
        )
    }
}
