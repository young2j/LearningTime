```javascript
npm install npm -g //更新npm
npm install package [--save-dev]//本地安装
npm install package -g //全局安装
npm uninstall package
npm list package /-g
npm search package
npm update package
npm info package

npm cache clear

npm init //创建模块 会生成package.json文件
npm adduser //添加用户
npm publish //发布
npm unpublish package@version
```

| 名称                      | 描述                                                         | 简写         |
| :------------------------ | :----------------------------------------------------------- | :----------- |
| npm install xxx           | 安装xxx模块，但不记录到package.json里                        | npm i xxx    |
| npm install --save xxx    | 安装xxx模块，并且记录到package.json里，字段对应的dependency，是产品环境必须依赖的模块 | npm i -s xxx |
| npm install --save-de xxx | 安装xxx模块，并且记录到package.json里，字段对应的dev-dependency，是开发环境必须依赖的模块，比如测试类的（mocha、chai、sinon、zombie、supertest等）都在 | npm i -D xxx |
| npm install --global xxx  | 全局安装xxx模块，但不记录到package.json里，如果模块里package.json有bin配置，会自动链接，作为cli命令 | npm i -g xxx |

