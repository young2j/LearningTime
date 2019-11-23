title: nodeppt 学习笔记
speaker: None
url: https://github.com/ksky521/nodeppt
transition: cards
files: /js/demo.js,/css/demo.css,/js/zoom.js
theme: moon
usemathjax: yes

[slide]

# Nodeppt 学习笔记

<small>——杨双杰  2018年7月19日</small>

[slide]

## 安装

```shell
npm config ls [-l]
npm config set prefix "path"
npm config set cache "path"
npm install -g nodeppt
```

## 启动

```shell
nodeppt start -h
nodeppt start -d "F:\nodejs\node_modules\node_global\node_modules\nodeppt\ppts" -p 8080 -H 127.0.0.1 [-w -c -w]
```

### socket控制

```markdown
* 使用url参数controller=socket，然后按Q键
    http://127.0.0.1:8080/md/demo.md?controller=socket
* 使用start命令行,然后按Q键
    nodeppt start -c socket
* 默认使用postMessage多窗口控制
    http://127.0.0.1:8080/md/demo.md?_multiscreen=1
```

[slide]

## 事件绑定

使用函数`Slide.on`，目前支持`update`函数，即转场后的回调。示例代码：

```javascript
Slide.on('update', function(i, itemIndex, cls) {
//接受三个参数：
//* 当前slide的index
//* itemIndex当前slide进入的第几个build动画，从1开始
//* 方向pageup/pagedown
    Puff.add('#FFC524' /*colors[i % 6]*/ , ctx, 20, 700, width / 2, height / 2, width / 1.8, 400);
    clearInterval(timer);
    //第十三个有动效
    if (i === 13 || i === 14) {
        timer = setInterval(function() {
            Puff.draw(1);
        }, 1E3 / FPS);
    }
})
```

[slide]

## 打印导出ppt

* 使用`url?print=1`访问页面
* 使用shell命令行

```shell
nodeppt generate -h
nodeppt generate ./ppts/demo.md output_path -a //导出全部到指定文件夹
nodeppt ppt_path output_path -a //导出目录下所有ppt，并且生成ppt list首页
```

[slide]

## Nodeppt Markdown 语法

[slide]

## 配置

```markdown
title: nodeppt-markdown
speaker: 三水清
url: 可以设置链接，如https://github.com/ksky521/nodeppt
transition: 转场动画，如kontext
files: 引入js和css的地址，如果有的话~自动放在页面底部。如/js/demo.js,/css/demo.css,/js/zoom.js
theme: moon
usemathjax: yes
```

### transition(转场动效)

支持的`transition`包括：  {:&.flexbox.hleft}

<div class='columns3'>
<ul><li>kontext</li> <li>vkontext</li>  <li>circle</li>  <li>earthquake</li><li>cards</li> <li> glue</li>  
</ul>
<ul>
 <li>stick</li>  <li>move</li>  <li>newspaper</li>  <li>slide</li>  <li>slide2</li>  <li>slide3</li>  
</ul>
<ul >
 <li>horizontal3d</li>  <li>horizontal</li>  <li>vertical3d</li>  <li>zoomin</li>  <li>zoomout</li>  <li>pulse</li>
</ul>
</div>

[slide data-transition='zoomIn']

### theme

支持的`theme`包括：

<div class="columns6">
    <a href="?theme=color" class="label-danger">color</a>
    <a href="?theme=blue" class="label-primary">blue</a>
    <a href="?theme=dark" class="label-info">dark</a>
    <a href="?theme=green" class="label-success">green</a>
    <a href="?theme=light" class="label-warning">light</a> 
    <a href="?theme=moon" class="label-info">moon</a>
</div>

[slide data-transition='vertical3d']

## 目录关系

可以在`md`同级目录下创建`img`、`js`、`css`等文件夹，然后在`markdown`里面引用，`nodeppt`默认会先查找`md`文件同级目录下面的静态资源，没有再找默认的`assets`文件夹下静态内容 。

[slide]

## 分页

使用 &#91;slide&#93;作为每页ppt的间隔；

### 单页背景

添加单页背景，使用下面的语法：

```markdown
[ slide  style="background-image:url('/img/bg1.png')"]
# 这是个有背景的家伙
## 我是副标题
```

### 单页上下布局

```markdown
[ slide ]
## 主页面样式
### ----是上下分界线
----
nodeppt是基于nodejs写的支持 **Markdown!** 语法的网页PPT
nodeppt：https://github.com/ksky521/nodeppt
```

[slide]

### 单页动画设置

在md文件顶部可以设置全局转场动画`transition`;

如果要设置单页的转场动画，可以通过下面的语法

```markdown
[ slide  data-transition="vertical3d"]
## 这是一个vertical3d的动画
```

### 单条动画

在列表第一条加上` { :&.动画类型 }`

目前支持的单条动画效果包括：

* moveIn {:&.moveIn}

* fadeIn {:&.fadeIn}

* bounceIn {:&.bounceIn}

* rollIn {:&.rollIn}

* zoomIn {:&.zoomIn}

[slide]

### 页内动效

**magic标签的earthquake动效**

[magic data-transition="earthquake"]

<div>

<div class='text-warning'>图片点击可全屏</div>

<img src="http://pic34.photophoto.cn/20150202/0005018384491898_b.jpg" height=200>

</div>

<div>

<div class='text-success'>图片点击禁止全屏</div>

<img src="http://pic.58pic.com/58pic/11/41/90/31U58PIC3wK.jpg" class="no-screenfull" height=200>

</div>

[/magic]

[slide]

[magic data-transition="cover-circle"]

**magic 标签的cover-circle动效**

<img src="http://pic34.photophoto.cn/20150202/0005018384491898_b.jpg">

[/magic]

[slide]

## 插入html代码

如果需要完全DIY ppt内容，可以**直接使用** html标签。

支持markdown和html混编，例如： {:&.flexbox.vleft}

```html
<div class="file-setting">
    <p>这是html</p>
</div>
<p id="css-demo">这是css样式</p>
<p>具体看下项目中 ppts/demo.md 代码</p>
<script>
    function testScriptTag(){

    }
    console.log(typeof testScriptTag);
</script>
<style>
#css-demo{
    color: red;
}
</style>
```

[slide]

### 支持.class/#id/自定义属性样式

------

```html
使用：.class{:.class}
使用：#id{:#id}
组合使用：{:.class.class2 width="200px"}
父元素样式使用&：{:&.class}
```

### text

------

<span class="text-danger">.text-danger</span> <span class="text-success">.text-sucess</span><span class="text-primary">.text-primary</span>

<span class="text-warning">.text-warning</span><span class="text-info">.text-info</span><span class="text-white">.text-white</span><span class="text-dark">.text-dark</span>

<span class="blue">.blue</span><span class="blue2">.blue2</span><span class="blue3">.blue3</span><span class="gray">.gray</span><span class="gray2">.gray2</span><span class="gray3">.gray3</span>

<span class="red">.red</span><span class="red2">.red2</span><span class="red3">.red3</span>

<span class="yellow">.yellow</span><span class="yellow2">.yellow2</span><span class="yellow3">.yellow3</span><span class="green">.green</span><span class="green2">.green2</span><span class="green3">.green3</span>

[slide]

### label and link

<span class="label label-primary">.label.label-primary</span>

<span class="label label-warning">.label.label-warning</span>

<span class="label label-danger">.label.label-danger</span>

<span class="label label-default">.label.label-default</span>

<span class="label label-success">.label.label-success</span>

<span class="label label-info">.label.label-info</span>

<a href="#">link style</a> 

<mark>mark</mark>

[slide]

### button

<button class="btn btn-default">.btn .btn-default</button> 

 <button class="btn btn-primary">.btn.btn-lg.btn-primary</button>

 <button class="btn btn-warning">.btn.btn-waring</button> 

<button class="btn btn-success">.btn.btn-success</button> 

<button class="btn btn-danger">.btn.btn-danger</button>

<button class="btn btn-lg btn-default">.btn.btn-lg.btn-default</button> 

<button class="btn btn-xs btn-success">.btn.btn-xs.btn-success</button>

 <button class="btn btn-sm btn-primary">.btn.btn-sm.btn-primary</button> 

<button class="btn btn-rounded btn-warning">.btn.btn-rounded.btn-waring</button> 

 <button class="btn btn-danger" disabled="disabled">disabled.btn.btn-danger</button>

<button class="btn btn-success"><i class="fa fa-share mr5"></i></button>

[slide]

### icons: Font Awesome

------

<i class="fa fa-apple"></i>
<i class="fa fa-android"></i>
<i class="fa fa-github"></i>
<i class="fa fa-google"></i>
<i class="fa fa-linux"></i>
<i class="fa fa-css3"></i>
<i class="fa fa-html5"></i>
<i class="fa fa-usd"></i>
<i class="fa fa-pie-chart"></i>
<i class="fa fa-file-video-o"></i>
<i class="fa fa-cog"></i>

[slide]

### 插入iframe

使用`data-src`作为`iframe`的`url`，这样只有切换到当前页才会加载`url`内容

```html
<iframe data-src="http://www.baidu.com" src="about:blank;"></iframe>
```

<iframe data-src="http://www.baidu.com" src="about:blank;"></iframe>

[slide]

## 回调函数和事件

在页面中演示一些demo，除了上面的插入html语法外，还提供了`enter`和`leave`，分别用于：切入/切走当前ppt时，执行js函数。

例如： {:&.flexbox.vleft}

```markdown
[ slide data-on-leave="outcallback" data-on-enter="incallback"]
## 当进入此页，就执行incallback函数
## 当离开此页面，就执行outcallback函数
```

单个slide事件：build/enter/leave/keypress，事件统一在&#91;slide&#93;
中使用`data-on-X`来指定一个全局函数名

| build       | 当触发下一步操作的时会触发，event具有stop方法 |
| ----------- | --------------------------------------------- |
| keypress    | 在当前页面按键触发，event具有stop方法         |
| enter/leave | 进入/离开 此页面触发的事件，event无stop方法   |

[slide]

## 表格实例

> > 同markdown表格语法;blockquote也在这里演示 {:&.pull-right}

## 多窗口演示

### 双屏演示不out！

------

把页面网址改成 [url?_multiscreen=1](?_multiscreen=1)，支持多屏演示哦！

跟powderpoint/keynote一样的双屏功能，带有备注信息。

[slide]

## 远程执行函数

------

在多屏和远程模式中，可以使用`proxyFn`来远程执行函数。

```html
<script>
function globalFunc(){
}
</script>
<button onclick="Slide.proxyFn('globalFunc')" class="btn btn-default">远程执行函数</button>
```

<button onclick="Slide.proxyFn('globalFunc','args')" class="btn btn-default">测试远程执行函数</button>
<a href="?_multiscreen=1#33">在多屏中测试远程执行</a>

<script>
    function globalFunc(a){
        alert('proxyFn success: '+a+location.href);
    }
</script>
[slide]

## nodeppt快捷键介绍

---

### 快速翻页

1.  输入页码，然后enter
2.  使用O键，开启纵览模式，然后翻页

---

### 动效样式强调

这段话里面的**加粗**和*em*字体会动效哦~

按下【H】键查看效果

---

### 支持zoom.js

`alt`+鼠标点击放大，再次`alt+click`回复原状

---

[slide]

---

### 使用note做笔记

```markdown
[ note]
...笔记，查看请按N
[ /note]
```

[note]
做笔记，展示过程中使用n键显示与关闭

[/note]

---

### 使用画笔

按下键盘【P】键：按下鼠标左键，在此处乱花下看看效果。

按下键盘【B/Y/R/G/M】：更换颜色，按下【1~4】：更换粗细

按下键盘【C】键：清空画板

---

### 使用overview模式

按下键盘【O】键。看下效果。

在overview模式下，方向键下一页，【enter】键进入选中页

或者按下键盘【O】键，退出overview模式

----

[slide]

### 宽度不够？？

------

按下键盘【W】键，切换到更宽的页面看效果，第二次按键返回

 |less| sass | stylus
:-------|:------:|-------:|--------
环境 |js/nodejs | Ruby(这列右对齐) | nodejs(高亮) {:.highlight}
扩展名 | .less | .sass/.scss | .styl
特点 | 老牌，用户多，支持js解析 | 功能全，有成型框架，发展快 | 语法多样，小众
案例/框架 | [Bootstrap](http://getbootstrap.com/) | [compass](http://compass-style.org) [bourbon](http://bourbon.io) |

---

