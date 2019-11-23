# HTML

### 特殊符号

| 特殊符号 | 符号码  |
| -------- | ------- |
| 空格     | &nbsp ; |
| "        | &quot ; |
| <        | &lt ;   |
| >        | &gt ;   |
| &copy;   | &copy ; |
| &reg;    | &reg ;  |

## 超链接<a>

| 标记      | 描述           |
| --------- | -------------- |
| href      | 链接地址       |
| name      | 链接名         |
| title     | 提示文字       |
| target    | 链接的目标窗口 |
| accessKey | 链接热键       |

## 图片标记<img>

| 属性          | 说明     |
| ------------- | -------- |
| src           | 图像源   |
| alt           | 提示文字 |
| width、height | 宽高     |
| border        | 边框     |
| vspace        | 垂直间距 |
| hspace        | 水平间距 |

## 列表标记

| 标记         | 描述             |
| ------------ | ---------------- |
| <ul>         | 无序列表         |
| <ol>         | 有序列表         |
| <dir>        | 目录列表         |
| <dl>         | 定义列表         |
| <dt>、<dd>   | 定义列表的子标记 |
| <menu>       | 菜单列表         |
| <li>         | 列表项标记       |
| 1,a,A,i,I    | 有序列表类型     |
| square、disc | 无序列表类型     |

## 表格标记

| 标记    | 描述       |
| ------- | ---------- |
| <table> | 表格       |
| <thead> | 表首       |
| <th>    | 表头       |
| <tr>    | 行标记     |
| <td>    | 单元格标记 |
| <tbody> | 表体标记   |
| <tfoot> | 表尾标记   |

## 表单标记<form>

### 表单属性

| 属性    | 描述                         |
| ------- | ---------------------------- |
| action  | 真正处理表单数据的脚本或程序 |
| name    | 名称属性                     |
| method  | 提交方式属性                 |
| enctype | 编码方式属性                 |
| target  | 目标显示方式属性             |

enctype属性的取值范围

| 属性取值                          | 描述                                 |
| --------------------------------- | ------------------------------------ |
| Test/plain                        | 纯文本                               |
| application/x-www-form-urlencoded | 默认编码形式                         |
| multipart/form-data               | MIME编码，上传文件的表单必须选择该项 |

target属性的取值范围

| 属性取值 | 描述                       |
| -------- | -------------------------- |
| _blank   | 返回的信息显示在新窗口中   |
| _parent  | 返回的信息显示在父级窗口中 |
| _self    | 返回的信息显示在当期窗口中 |
| _top     | 返回的信息显示在顶级窗口中 |

### 输入标记<input>

#### name属性

#### type属性

| 取值     | 描述     |
| -------- | -------- |
| text     | 文本域   |
| password | 密码域   |
| radio    | 单选按钮 |
| checkbox | 复选框   |
| button   | 普通按钮 |
| submit   | 提交按钮 |
| reset    | 重置按钮 |
| image    | 图形域   |
| hidden   | 隐藏域   |
| file     | 文件域   |

##### 文本域text、密码域password属性

| 取值      | 描述           |
| --------- | -------------- |
| name      | 名称           |
| maxlength | 最大输入字符数 |
| size      | 宽度           |
| value     | 默认值         |

## 文本区域标记<textarea>

| 属性  | 描述       |
| ----- | ---------- |
| name  | 名称       |
| rows  | 行数       |
| cols  | 列数       |
| value | 文本默认值 |

## 菜单和列表标记<select><option>

| 属性     | 描述       |
| -------- | ---------- |
| name     | 名称       |
| size     | 显示的数目 |
| multiple | 支持多选   |
| value    | 选项值     |
| selected | 默认选项   |

# 图形图像处理

## fillStyle和strokeStyle

```javascript
context.fillStyle = 'orange';
context.fillStyle = '#FFA500';
context.fillStyle = 'rgb(255,165,0)';
context.fillStyle = 'rgba(255,165,0,1)';
strokeStyle同上
```

## 透明度

```javascript
globalAlpha = transparency value
```

## 线型

```javascript
lineWidth = value #线宽
lineCap = type # 线端
lineJoin = type #连接端
miterLimit = value 
```

| lineJoin | 属性：round、bevel、miter(默认) |
| -------- | ------------------------------- |
| lineCap  | 属性：butt(默认)、round、square |

