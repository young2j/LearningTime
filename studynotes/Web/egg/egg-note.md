# egg cli
```shell
mkdir egg-example && cd egg-example
npm init egg --type=simple # --type=ts 生成ts项目
npm i
npm run dev
```

# egg 目录约定
> app/
* view: 模板视图
* controller： 处理业务逻辑
* model：orm，定义数据模型
* service： 与数据库打交道，查询、请求数据
* extend: 扩展
* schedule：定时任务
> config/
* plugin: 插件

