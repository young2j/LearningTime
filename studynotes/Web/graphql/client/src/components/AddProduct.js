import React, { Component } from 'react'
import { graphql} from 'react-apollo'
import compose from 'lodash.flowright'

import { getCompanyList,addProduct, getProductsList } from '../graphql'


class AddProduct extends Component {
    constructor(){
        super()
        this.state = {
            name:'',
            category:'',
            companyId:''
        }
    }

    displayCompanies(){
        // console.log(this.props);
        const data = this.props.getCompanyQuery
        if (data.loading){
            return (<option>正在加载...</option>)
        } else {
            return data.companies.map(company=>{
                return (
                    <option value={company.id}
                     key={company.id} 
                    >
                        {company.name}
                    </option>)
            })
        }
    }

    onSubmit=(e)=>{
        e.preventDefault()
        // console.log(addProduct); //Object
        // console.log(this.props.addProductMutation()) // Promise
        
        this.props.addProductMutation({
            variables:{
                name:this.state.name,
                category:this.state.category,
                companyId:this.state.companyId
            },
            refetchQueries:[{query:getProductsList}]
        })

        // console.log(this.props);
        
    }

    render() {
        return (
            <form action="add-product" onSubmit={this.onSubmit}>
                <div className="field">
                    <label htmlFor="">产品名称:</label>
                    <input type="text" onChange={e=>this.setState({name:e.target.value})}/>
                </div>
                <div className="field">
                    <label htmlFor="">产品类别:</label>
                    <input type="text" onChange={e=>this.setState({category:e.target.value})}/>
                </div>
                <div className="field">
                    <label htmlFor="">所属公司:</label>
                    <select name="" id="" onChange={e=>this.setState({companyId:e.target.value})}>
                        <option value="">选择一个公司</option>
                        {this.displayCompanies()}
                    </select>
                </div>
                <button>+</button>
            </form>
        )
    }
}

export default compose(
    graphql(getCompanyList,{name:'getCompanyQuery'}),
    graphql(addProduct,{name:'addProductMutation'})
)(AddProduct)
