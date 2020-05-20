const { override, fixBabelImports, addLessLoader,addDecoratorsLegacy} = require('customize-cra')
const modifyVars = require('./theme')


module.exports = override(
    fixBabelImports('import', {
        libraryName: 'antd',
        libraryDirectory: 'es',
        // style: 'css',
        style:true,
        }),
    addLessLoader({
    javascriptEnabled: true,
        modifyVars
    }),
    addDecoratorsLegacy()
)