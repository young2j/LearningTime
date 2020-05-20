const mongoose = require('mongoose')
const Schema = mongoose.Schema

const companySchema = new Schema({
    name: String,
    establishd:Number
})

module.exports = mongoose.model('Company',companySchema)