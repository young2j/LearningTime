
//js: graphql/graphql-yoga
//py: graphene
const graphql = require('graphql')
const { 
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLString,
    GraphQLID,
    GraphQLInt,
    GraphQLList,
    GraphQLNonNull
} = graphql
const _ = require('lodash')


const {Product,Company} = require('../models')


//graphql object: 对应SQL表/mongo Document
const ProductType=new GraphQLObjectType({
    name:'Product',
    fields:()=>({
        id:{type:new GraphQLNonNull(GraphQLID)},
        name:{type:new GraphQLNonNull(GraphQLString)},
        category:{type:GraphQLString},
        company:{
            type:CompanyType,
            resolve(parent,args){ //parent指向product信息
                // return _.find(CompanyList,{id:parent.companyId})
                return Company.findById(parent.companyId)
            }
        }
    })
})

const CompanyType=new GraphQLObjectType({
    name:'Company',
    fields:()=>({
        id:{type:new GraphQLNonNull(GraphQLID)},
        name:{type:new GraphQLNonNull(GraphQLString)},
        establishd:{type:new GraphQLNonNull(GraphQLInt)},
        products:{
            type: new GraphQLList(ProductType),
            resolve(parent,args){
                // return _.filter(ProductList,{companyID:parent.id})
                return Product.find({companyId:parent.id})
            }
        }
    })
})


//query：相当于查询(Retrieve)的Routes
const RootQuery = new GraphQLObjectType({
    name:'RootQueryType',
    fields:{
        product:{
            type:ProductType,
            args:{id:{type:GraphQLID}},
            resolve(parent,args){
                //从数据库获取数据
                // return _.find(ProductList,{id:args.id})
                return Product.findById(args.id)
            }
        },
        company:{
            type:CompanyType,
            args:{id:{type:GraphQLID}},
            resolve(parent,args){
                // return _.find(CompanyList,{id:args.id})
                return Company.findById(args.id)
            }
        },
        products:{
            type: new GraphQLList(ProductType),
            resolve(parent,args){
                // return ProductList
                return Product.find({})
            }
        },
        companies:{
            type: new GraphQLList(CompanyType),
            resolve(parent,args){
                // return CompanyList
                return Company.find({})
            }
        }
    }
})


//mutation:相当于增删改(CUD)的Routes
const Mutation = new GraphQLObjectType({
    name:'Mutation',
    fields:{
        addCompany:{
            type:CompanyType,
            args:{
                name:{type:GraphQLString},
                establishd:{type:GraphQLInt}
            },
            resolve(parent,args){
                let company = new Company({
                    name:args.name,
                    establishd:args.establishd
                })
                return company.save()
            }
        },
        addProduct:{
            type:ProductType,
            args:{
                name: { type: GraphQLString },
                category: { type: GraphQLString },
                companyId: { type: GraphQLID }
            },
            resolve(parent,args){
                let product = new Product({
                    name:args.name,
                    category:args.product,
                    companyId:args.companyId
                })
                return product.save()
            }
            
        }
    }
})


//schema
module.exports = new GraphQLSchema({
        query: RootQuery,
        mutation:Mutation
    })