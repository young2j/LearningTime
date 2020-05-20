import React, { Component } from 'react'
import { graphql } from 'react-apollo'

import { getProductsList } from '../graphql'
import ProductDetail from './ProductDetail'


class ProductList extends Component {
    constructor(){
        super()
        this.state = {
            selected:null
        }
    }
    displayProducts(){
        const data = this.props.data
        if (data.loading){
            return (<div>正在加载...</div>)
        } else {
            return data.products.map(product =>{
                return (<li key={product.id}
                            onClick={e=>this.setState({selected:product.id})}
                        >
                            {product.name}
                        </li>)
            })
        }
    }
    render() {
        return (
            <div>
                <ul id="product-list">
                    {this.displayProducts()}
                </ul>
                <ProductDetail productId={this.state.selected}/>
            </div>
        )
    }
}

export default graphql(getProductsList)(ProductList)
