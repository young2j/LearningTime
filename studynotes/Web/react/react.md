# 创建一个react-app

```shell
npx create-react-app app-name 
# npm ERR! Unexpected end of JSON input while parsing near '...l-preset-env":"^1.6.0'
# 版本问题，执行
npm cache clean --force
```

```shell
npm start
    # Starts the development server.

npm run build
    # Bundles the app into static files for production.

npm test
    # Starts the test runner.

npm run eject # 暴露出配置项，进而自定义配置。但【注：1.不可逆；2.需要先提交git，否则报错】
    # Removes this tool and copies build dependencies, configuration files
    #and scripts into the app directory. If you do this, you can’t go back!

# We suggest that you begin by typing:
  cd study-app
  npm start
```
```shell
npm install redux react-redux react-router-dom antd react-app-rewired customize-cra less less-loader babel-plugin-import -D
```
# 配置开发环境

```shell
npm init
npm i webpack webpack-cli [-g -D]
# package.json:
# 'scripts':
# 'build': webpack [--mode development --mode production] --config pathto/webpack.config.js

npm i html-webpack-plugin -D#自动生成html
npm i mini-css-extract-plugin -D#自动提取css为单独文件,MiniCssExtractPlugin.loader替代style-loader
npm i webpack-dev-server  -D#本地服务器
npm run dev #接上步运行本地服务器

npm install less-loader less --save-dev # .less文件预处理器
npm i postcss-loader autoprefixer -D # css自动前缀，增强兼容性;结合browerslist使用
npm i file-loader --save-dev # 文件加载器，如图片文件.jpg/.png/.gif等
npm i url-loader --save-dev # 不能处理时，默认采用file-loader。file-loader

npm install babel-cli@6 babel-preset-react-app@3 #安装JSX预处理器

npm install react-app-rewired -D #支持react HOC装饰器写法
npm install customize-cra -D #自定义rewired配置

npm install redux -D
npm install redux-thunk -S
npm install react-router-dom -S
```

```shell
npm config get registry
npm config set registry https://registry.npm.taobao.org
```

```shell
#MAC/linux环境：临时设置
$ PORT=8081 npm start

#如果想设置一次永久生效，使用下面的命令。
$ export PORT=8081  
$ npm start

# Window系统环境
set PORT=8081
npm start
```



