const path = require('path')
const webpack = require('webpack')

const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin')
// const CopyWebpackPlugin = require('copy-webpack-plugin')
// const CleanWebpackPlugin = require('clean-webpack-plugin')

module.exports = {
    mode:'development',
    entry:'./src/index.js',//单文件
    // entry:['./src/index.js','./src/index2.js'],//多文件
    // entry:{
    //     src:'./src/index.js',
    //     src2:'./src2/index.js'
    // },//多入口

    output:{
        path:path.resolve(__dirname,'build'),
        filename:'[name].js' //多出口
    },
    devServer:{
        contentBase:'./public', //本地服务器服务的资源目录
        host:'localhost', //主机
        port:8080, //端口
        open:true, //自动打开网页
        hot:true,//模块热替换
    },
    module:{
        rules:[
            {
                test:/\.css$/,
                use:[
                'style-loader',
                //     {
                //     loader: MiniCssExtractPlugin.loader,
                //     options: {
                //       esModule: true,
                //     },
                //   },
                  'css-loader'] //'style-loader'=>MiniCssExtractPlugin.loader=>'style-loader'<hmr>
            },
            {
                test:/\.less$/,
                use:['style-loader','css-loader','less-loader',
                {
                    loader:'postcss-loader',
                    options:{
                        plugins:[
                            require('autoprefixer')
                        ]
                    }
                }
            ]
            },
            {
                test:/\.(jpg|jpeg|gif|png)$/,
                use:[{
                    loader:'file-loader',
                    options:{
                        name:'[name].[hash8].[ext]',
                        publicPath:'',//图片引入路径 url('publicPath/.jpg')
                        outputPath:''//图片输出路径
                    }
                }]
            },
            // {
            //     test:/\.(eof|svg|ttf|woff|woff2)$/,
            //     use:'file-loader',
            //     options:{
            //         outputPath:'./fonts'
            //     }
            // },
    //----------html引入图片-----------------
            {
                test:/\.(html)$/,
                use:{
                    loader:'html-loader',
                    options:{
                        attrs:['img:src','img:data-src'] //处理图片src
                    }
                }
            },
    //-------------babel转译------------------
    // npm install babel-loader @babel/core @babel/preset-env -D
    //两种配置规则
    //1.添加.babelrc 
    //2.use:[{options}]
            {
                test:/\.js$/,
                exclude:/node_modules/,
                // use:'babel-loader'
                use:{
                    loader:'babel-loader',
                    options:{
                        presets:["@babel/preset-env"]
                    }
                }
            }
        ]
    },
    //----------------js插件---------使用jQuery
    // resolve:{
    //     alias:{
    //         jQuery:path.resolve(__dirname,'./js/jquery.min.js')
    //     }
    // },
    plugins:[
        // new webpack.ProvidePlugin({
        //     jQuery:'jQuery'
        // }),
        new HtmlWebpackPlugin({
            template:'./public/index.html',
            filename:'[name].html',
            minify:{
                minimize:true,
                removeAttributeQuotes:true,
                removeComments:true,
                minifyCSS:true,
                minifyJS:true,
                removeEmptyElements:true,
                collapseWhitespace:true
            },
            hash:true
        }),
        new MiniCssExtractPlugin({
            filename:'/css/index.css'
        }),
        new OptimizeCssAssetsPlugin({
            assetNameRegExp:/\.css$/g, //匹配需优化的资源
            cssProcessor:require('cssnano'), //优化处理器
            cssProcessorPluginOptions: {  //传递给优化处理器的插件
                preset: ['default', { discardComments: { removeAll: true } }], //去除注释
              },
            canPrint: true //可以console.log
        }),
        // new CopyWebpackPlugin([
        //     {
        //         from:__dirname+'/public/assets',
        //         to:__dirname+'/build/assets'
        //     }
        // ]),
        // new CleanWebpackPlugin(['build']),

        new webpack.NamedModulesPlugin(),
        new webpack.HotModuleReplacementPlugin()
    ]
}