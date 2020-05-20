const express = require('express')
const graphqlHTTP = require('express-graphql')
const mongoose = require('mongoose')
const cors = require('cors')

const schema = require('./schema')

//connect to mongodb
const dbUrl = "mongodb://localhost:27017/graphQL"
mongoose.connect(dbUrl, { useNewUrlParser: true,useUnifiedTopology: true })
mongoose.connection.once('open', () => {
    console.log('数据库连接成功');
})


const app=express()
app.use(cors())
app.use('/graphql',graphqlHTTP({
    schema,
    graphiql:true
}))

app.listen(4000, ()=>{
    console.log('success listen 4000 port.'); 
})