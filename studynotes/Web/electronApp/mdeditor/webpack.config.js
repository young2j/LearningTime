const path = require('path')

module.exports = {
  target:"electron-main",
  entry:"./main.js",
  output:{
    path:path.join(__dirname,"./build"),
    filename:'main.js'
  },
  node:{
    __dirname:false
  }
}