<h1 style='text-align:center'><code>pyautogui</code></h1>
# 保护措施

```python
pyautogui.FAILSAFE = True #如果失控了，需要中断PyAutoGUI函数，就把鼠标光标放在屏幕左上角。要禁用这个特性，就把FAILSAFE设置成False

pyautogui.PAUSE = 2.5 #可以为所有的PyAutoGUI函数增加延迟。默认延迟时间是0.1秒。

pyautogui.MINIMUM_DURATION = 0.1 #默认事件持续时间0.1s
```

# 鼠标事件`MouseEvent`

* 坐标系原点`(0,0)`在左上角。水平为x，垂直为y。
* 如果屏幕像素是`1920×1080`，那么右下角的坐标是`(1919, 1079)`
```python
pyautogui.position()#鼠标当前的坐标位置
```

> 示例：实时刷新光标位置

```python
import pyautogui
print('Press Ctrl-C to quit')
try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: {} Y: {}'.format(*[str(x).rjust(4) for x in [x, y]])
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\n')
```
## `moveEvent`

```python
pyautogui.moveTo(x,y,duration) #绝对移动
pyautogui.moveRel(xOffset,yOffset,duration) #相对移动
```

## `clickEvent`

```python
pyautogui.click(x=moveToX,y=moveToY,clicks=num_of_clicks,interval=seconds,button='left/middle/right/') #点击——等价于
pyautogui.leftClick(x,y,interval,duration)
pyautogui.rightClick()
pyautogui.middleClick()
pyautogui.doubleClick(x,y,button,interval,duration)
pyautogui.tripleClick()
```

## `scrollEvent`

* 在OS X和Linux平台上，PyAutoGUI还可以用`hscroll()`实现水平滚动。
* `scroll()`函数是`vscroll()`的一个包装（`wrapper`），执行竖直滚动。

```python
pyautogui.scroll(clicks=amount_to_scroll, x=moveToX, y=moveToY) #amount_to_scroll参数表示滚动的格数。正数则页面向上滚动，负数则向下滚动。x,y表示先移动到xy位置再滚动。

pyautogui.mouseDown(x=moveToX, y=moveToY, button='left') #鼠标按下left
pyautogui.mouseUp(x=moveToX, y=moveToY, button='left') #鼠标松开left
```

## `dragEvent`

```python
pyautogui.dragTo(x,y,duration,button)
pyautogui.dragRel(x,y,duration,button)
```

## ` Tween / Easing function`

* 光标移动特效`PyTweening module`

* PyAutoGUI有30种缓动/渐变函数，可以通过`pyautogui.ease*?`查看

  ```python
  #  开始很慢，不断加速
  pyautogui.moveTo(100, 100, 2, pyautogui.easeInQuad)
  #  开始很快，不断减速
  pyautogui.moveTo(100, 100, 2, pyautogui.easeOutQuad)
  #  开始和结束都快，中间比较慢
  pyautogui.moveTo(100, 100, 2, pyautogui.easeInOutQuad)
  #  一步一徘徊前进
  pyautogui.moveTo(100, 100, 2, pyautogui.easeInBounce)
  #  徘徊幅度更大，甚至超过起点和终点
  pyautogui.moveTo(100, 100, 2, pyautogui.easeInElastic)
  ```

# 键盘事件`keyboardEvent`

```python
pyautogui.typewrite('hello world',interval) #输入内容
pyautogui.typewrite(['left','right','backspace','enter','f1']) #按下功能按键
pyautogui.KEYBOARD_KEYS #查看所有按键

pyautogui.hotkey('ctrl','v') #组合热键

pyautogui.press() #按下松开,可传入[],依次按下多个键
pyautogui.keyDown() #按下
pyautogui.keyUp() #松开
```

# 弹窗事件`messageBoxEvent`

```python
pyautogui.alert(text='警告消息，点击按钮后返回按钮上的文字内容',title='',button='OK')

pyautogui.confirm(text='确认消息，点击按钮后返回按钮上的文字内容',title='',buttons=['Ok','Cancel']) #确认与取消按钮
pyautogui.confirm(text='确认消息，点击按钮后返回按钮上的文字内容',title='',buttons=range(10)) #多个按钮

pyautogui.prompt(text='输入窗口，输入完毕点击OK返回输入的内容，点击Cancel返回None'，title='',default='')
pyautogui.password(text=''，title='',default='') #输入密码，显示为*，输入完毕点击OK返回输入的内容，点击Cancel返回None
```

# 屏幕事件`ScreenEvent`

```python
pyautogui.size() #屏幕分辨率(宽高)
pyautogui.onScreen(x,y) #点x，y是否在屏幕上
```

## `screenshotEvent`

* PyAutoGUI用Pillow/PIL库实现图片相关的识别和操作
* 在Linux里面，你必须执行`sudo apt-get install scrot`来使用截屏特性

```python
pyautogui.screenshot('path/to/.png',region=(x,y,width,height))

pyautogui.locateOnScreen('path/to/.png') #定位图片位置——返回(最左x坐标，最顶y坐标，宽度，高度);若没找到图片会返回None
pyautogui.center(pyautogui.locateOnScreen()) #截取中心位置==locateCenterOnScreen()

pyautogui.locateAllOnScreen('path/to/.png') #寻找所有相似图片，并返回一个生成器
pyautogui.locateCenterOnScreen('pahth/to/.png') #返回图片在屏幕上的中心XY轴坐标值
```

* 像素匹配

```python
#要获取截屏某个位置的RGB像素值，可以用Image对象的getpixel()方法：
im = pyautogui.screenshot()
im.getpixel((100, 200))

#也可以用PyAutoGUI的pixel()函数，是之前调用的包装：
pyautogui.pixel(100, 200)
#如果你只是要检验一下指定位置的像素值，可以用pixelMatchesColor()函数，把X、Y和RGB元组值穿入即可：
pyautogui.pixelMatchesColor(100, 200, (255, 255, 255))

#tolerance参数可以指定红、绿、蓝3种颜色误差范围：
pyautogui.pixelMatchesColor(100, 200, (248, 250, 245), tolerance=10)
```

## `getwindowEvent`

```python
pyautogui.getActiveWindow()
pyautogui.getAllWindows()
pyautogui.getWindowsAt()
pyautogui.getWindowsWithTitle()

win.move(x, y)
win.resizeTo(width, height)
win.maximize()
win.minimize()
win.restore()
win.close()
win.position() # returns (x, y) of top-left corner
win.moveRel(x=0, y=0) # moves relative to the x, y of top-left corner of the window
win.clickRel(x=0, y=0, clicks=1, interval=0.0, button=’left’) # click relative to the x, y of top-left corner of the window
```

