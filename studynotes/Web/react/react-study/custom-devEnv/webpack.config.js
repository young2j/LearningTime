const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
    entry:{
        main:'./src/index.js',
        // test:'./src/test.js'
    },        
    output:{
        path:path.resolve(process.cwd(),'dist'),
        filename:'static/js/[name].[chunkHash:8].js'
    },
    plugins:[
        new HtmlWebpackPlugin({
            title:'webpack-plugin',
            template:'public/index.html'
        }),
        new MiniCssExtractPlugin({
            filename:'static/css/[name].[chunkHash:8].css'
        })
    ],
    module:{
        rules:[
            {
                test: /\.css$/,
                use: [
                    // 'style-loader',
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'postcss-loader',
                ]
            },            
            {
                test:/\.less$/,
                use:[
                    // 'style-loader',
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'postcss-loader',
                    {
                        loader:'less-loader',
                        options:{}
                    }
                ]
            },
            {
                test: /\.(jpg|png|gif)$/,
                use: [
                    {
                        loader:'file-loader',
                        options:{
                            name:'static/images/[name].[ext]',
                            // outputPath:'static/images',
                            publicPath:'/'
                        }
                    }
                ]
            },            
        ]
    },
    devServer:{
        port:3000,
        open:true
    },

}