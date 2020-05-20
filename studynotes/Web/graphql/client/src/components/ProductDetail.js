import React, { Component } from 'react'
import { graphql } from 'react-apollo'

import { getProduct } from '../graphql'

class ProductDetail extends Component {

    displayProductDetail(){
        // console.log(this.props);
        const {product} = this.props.data
        if (product){
            return (
                <div>
                    <h2>{product.name}</h2>
                    <p>{product.category}</p>
                    <p>{product.company.name}</p>
                    <p>该公司所有产品：</p>
                    <ul className="products">
                        {
                            product.company.products.map(item => {
                                return <li key={item.id}>{item.name}</li>
                            })
                        }
                    </ul>
                </div>
            )
            
        } else {
            return <div>未选择任何产品</div>
        }
    }
    

    render() {
        // console.log(this.props);
        return (
            <div className='product-detail'>
                <hr/>
                {this.displayProductDetail()}
                <hr/>
            </div>
        )
    }
}


export default graphql(getProduct,{
    options:(props)=>{ //this.props
        return {
            variables:{
                id:props.productId
            }
        }
    }
}
)(ProductDetail)