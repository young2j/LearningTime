import ApolloClient, { gql } from 'apollo-boost'


const gqlClient = new ApolloClient({
    uri:'http://localhost:4000/graphql'
})


export const getProductsList = gql`
    {
        products{
            name,
            id
        }
    }
`

export const getProduct = gql`
    query($id:ID){
        product(id:$id){
            id,
            name,
            category,
            company{
                id,
                name,
                establishd,
                products{
                    name,
                    id
                }
            }
        }
    }
`


export const getCompanyList = gql`
    {
        companies{
            name,
            id
        }
    }
`
export const addProduct = gql`
    mutation($name:String!,$category:String!,$companyId:ID!){
        addProduct(name:$name,category:$category,companyId:$companyId){
            name,
            id
        }
    }
`





export default gqlClient