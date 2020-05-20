const mongoose = require('mongoose')
const Schema = mongoose.Schema

const productSchema = new Schema({
    name:String,
    category:String,
    companyId:String
})

module.exports = mongoose.model('Product', productSchema)