const HtmlWebpackPlugin = require('plugin'); //npm install
const webpack = require('webpack');
const path = require('path');

module.exports = {
	mode : 'production', //development
	/*
	entry: './entry.js',
	单入口等同于
	entry:{
		main:'./entry.js'
		}
	 */
	entry:{
		app:'./src/app.js', //应用程序入口
		vendors:'./src/vendors.js', //第三方库入口
		//多页面应用程序
		pageOne:'./src/pageOne/index.js',
		pageTwo:'./src/pageTwo/index.js',
		pageThree:'./src/pageThree/index.js',
	},

	output: {
		path: path.resolve(__dirname, 'dist'),
		filename: '[name].js', //[name]占位符，与entry中的key一致
	},

	module: {
		rules: [
			{ 
				test: /\.css$/, 
			 	use: [
					  {loader: "style-loader"},
					  {loader:"css-loader", options:{modules:true} }
					  ]
			},
			{test: /\.txt$/, use: 'raw-loader'},
			{test: /\.ts$/, use: 'ts-loader'},

		]
	},

	plugins: [
		new webpack.BannerPlugin('This file is created by ysj'),
		new HtmlWebpackPlugin({template:'./src/index.html'})
	]
}