// module.exports = (config)  => {
//     //不使用custom-cra
//     return config
// }


const {override,addDecoratorsLegacy} = require('customize-cra')
module.exports = override(
    addDecoratorsLegacy()
)