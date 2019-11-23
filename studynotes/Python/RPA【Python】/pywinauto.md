<h1 style="text-align:center;"><code>pywinauto</code></h1>

> 中文文档：<https://www.kancloud.cn/gnefnuy/pywinauto_doc/>

# backend

* `win32 API`
* `uia- MS UI Automation`

# entry point

```python
pywinauto.application.Application #作用范围是一个进程，如一般的桌面应用程序都为此类。
pywinauto.application.Desktop #Desktop的作用范围可以跨进程。主要用于像win10的计算器这样包含多个进程的程序。--很少见
```

#  start/connect process

```python
Application().start(self, cmd_line, timeout=app_start_timeout) #开启一个程序
Application().connect(self,path,process,handle,title,title_re,class_name) #连接一个已开启的程序
Application().connect(self,title_re,class_name)#组合参数会传递给pywinauto.findwindows.find_elements()
```

# location

## window/dialog location

```python
from pywinauto.application import Application
app = Application().start(r"F:\SublimeText3\sublime_text.exe")

# title
app.window(title='sublime') #dialog对象
app.sublime
app.windows() #dialogs对象

title_zh = u'中文title' #中文要转为Unicode编码
app.title_zh #可能报错
app['title_zh'] # 中文最好这么写，等同于app.window(best_match='tile_zh')

# key words
app.window(class_name='PX_WINDOW_CLASS').draw_outline(color='red') #画出轮廓以便准确定位
app.window(class_name='PX_WINDOW_CLASS').is_dialog() #判断是否为dialog对象
```

<table>
<thead>
<tr>
<th>可传参数</th>
<th>对应属性名称备注</th>
</tr>
</thead>
<tbody>
<tr>
<td>class_name</td>
<td>ClassName</td>
</tr>
<tr>
<td>class_name_re</td>
<td>正则匹配window Classname</td>
</tr>
<tr>
<td>title	Name</td>
<td>Window窗口名</td>
</tr>
<tr>
<td>title_re</td>
<td>正则匹配窗口名</td>
</tr>
<tr>
<td>best_match</td>
<td>模糊匹配类似的title</td>
</tr>
<tr>
<td>handle</td>
<td>句柄</td>
</tr>
<tr>
<td>framework_id</td>
<td>FrameworkId（一般情况下FrameworkId不是唯一的）</td>
</tr>
<tr>
<td>process</td>
<td>ProcessId，进程id（注意：每次启动后，进程id都会变）</td>
</tr>
<tr>
<td>control_id</td>
<td>control_id</td>
</tr>
<tr>
<td>control_type</td>
<td>ControlType（）</td>
</tr>
<tr>
<td>auto_id</td>
<td>AutomationId</td>
</tr>
</tbody>
</table>

## control location

* 对于常见的窗口程序，需要操作的控件有输入框(`Edit`)、按钮(`Button`)、复选框(`CheckBox`)、单选框(`RadioButton`)、下拉列表(`ComboBox`)。

```python
app.window().print_control_identifiers() # 使用该方法显示会话窗口的所有控件属性
# title
app['window_tile']['control_title'] #中文最好这么写
app.window_tile.control_title

# 层级
app.window().window() # 如下是同一个窗体
app.window(title_re='.* - 记事本$').window(class_name='edit') #多层次的描述指定一个窗口
app.window(title_re='.* - 记事本$',class_name='edit') #使用组合参数指定一个窗体

app.window().child_window()

# wpath
app.window().children()[1].children()[0]
```

# methods

## app methods

```python
app.wait_cpu_usage_lower(threshold=5) #等到cpu低于5%
app.wait_for_process_exit(timeout=None, retry_interval=None)
app.start()
app.connect()
wait(wait_for, timeout=None, retry_interval=None)
wait_not(wait(wait_for, timeout=None, retry_interval=None))
app.exists()

app.window()
app.windows()
```

## window/control common methods

```python
print_control_identifiers(depth=None, filename=None)
print_ctrl_ids(depth=None, filename=None)

capture_as_image()
click()
click_input()
close()
close_click()
debug_message()
double_click()
double_click_input()
drag_mouse()
draw_outline()
get_focus()
get_show_state()
maximize()
menu_select()
minimize()
move_mouse()
move_window()
notify_menu_select()
notify_parent()
press_mouse()
press_mouse_input()
release_mouse()
release_mouse_input()
restore()
right_click()
right_click_input()
send_message()
send_message_timeout()
set_focus()
set_window_text()
type_keys()
Children()
Class()
ClientRect()
ClientRects()
ContextHelpID()
ControlID()
ExStyle()
Font()
Fonts()
FriendlyClassName()
GetProperties()
HasExStyle()
HasStyle()
IsChild()
IsDialog()
IsEnabled()
IsUnicode()
IsVisible()
Menu()
MenuItem()
MenuItems()
Owner()
Parent()
PopupWindow()
ProcessID()
Rectangle()
Style()
Texts()
TopLevelParent()
UserData()
VerifyActionable()
VerifyEnabled()
VerifyVisible()
WindowText()
```

## window methods

```python
# app.window().
wait()
wait_not()

wait_until()
wait_until_passes()
#使用装饰器
from pywinauto.timings import always_wait_until，always_wait_until_passes

@always_wait_until_passes(4, 2)
def ensure_text_changed(ctrl):
    if previous_text == ctrl.window_text():
        raise ValueError('The ctrl text remains the same while change is expected')

#使用全局时间控制函数
from pywinauto.timings import Timings

Timings.defaults()
Timings.slow() # 慢一倍
Timings.fast() # 快一倍
```

## control methods

### Button, CheckBox, RadioButton, GroupBox

> * [ButtonWrapper.Check](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ButtonWrapper.Check)
> * [ButtonWrapper.GetCheckState](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ButtonWrapper.GetCheckState)
> * [ButtonWrapper.SetCheckIndeterminate](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ButtonWrapper.SetCheckIndeterminate)
> * [ButtonWrapper.UnCheck](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ButtonWrapper.UnCheck)

### ComboBox

> * [ComboBoxWrapper.DroppedRect](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ComboBoxWrapper.DroppedRect)
> * [ComboBoxWrapper.ItemCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ComboBoxWrapper.ItemCount)
> * [ComboBoxWrapper.ItemData](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ComboBoxWrapper.ItemData)
> * [ComboBoxWrapper.ItemTexts](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ComboBoxWrapper.ItemTexts)
> * [ComboBoxWrapper.Select](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ComboBoxWrapper.Select)
> * [ComboBoxWrapper.SelectedIndex](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ComboBoxWrapper.SelectedIndex)

### Dialog

> * [DialogWrapper.ClientAreaRect](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.DialogWrapper.ClientAreaRect)
> * [DialogWrapper.RunTests](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.DialogWrapper.RunTests)
> * [DialogWrapper.WriteToXML](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.DialogWrapper.WriteToXML)

### Edit

> * [EditWrapper.GetLine](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.EditWrapper.GetLine)
> * [EditWrapper.LineCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.EditWrapper.LineCount)
> * [EditWrapper.LineLength](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.EditWrapper.LineLength)
> * [EditWrapper.Select](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.EditWrapper.Select)
> * [EditWrapper.SelectionIndices](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.EditWrapper.SelectionIndices)
> * [EditWrapper.SetEditText](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.EditWrapper.SetEditText)
> * [EditWrapper.set_window_text](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.EditWrapper.set_window_text)
> * [EditWrapper.TextBlock](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.EditWrapper.TextBlock)

### Header

> * [HeaderWrapper.GetColumnRectangle](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.HeaderWrapper.GetColumnRectangle)
> * [HeaderWrapper.GetColumnText](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.HeaderWrapper.GetColumnText)
> * [HeaderWrapper.ItemCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.HeaderWrapper.ItemCount)

### ListBox

> * [ListBoxWrapper.GetItemFocus](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ListBoxWrapper.GetItemFocus)
> * [ListBoxWrapper.ItemCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ListBoxWrapper.ItemCount)
> * [ListBoxWrapper.ItemData](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ListBoxWrapper.ItemData)
> * [ListBoxWrapper.ItemTexts](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ListBoxWrapper.ItemTexts)
> * [ListBoxWrapper.Select](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ListBoxWrapper.Select)
> * [ListBoxWrapper.SelectedIndices](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ListBoxWrapper.SelectedIndices)
> * [ListBoxWrapper.SetItemFocus](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.win32_controls.html#pywinauto.controls.win32_controls.ListBoxWrapper.SetItemFocus)

### ListView

> * [ListViewWrapper.Check](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.Check)
> * [ListViewWrapper.ColumnCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.ColumnCount)
> * [ListViewWrapper.Columns](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.Columns)
> * [ListViewWrapper.ColumnWidths](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.ColumnWidths)
> * [ListViewWrapper.GetColumn](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.GetColumn)
> * [ListViewWrapper.GetHeaderControl](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.GetHeaderControl)
> * [ListViewWrapper.GetItem](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.GetItem)
> * [ListViewWrapper.GetSelectedCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.GetSelectedCount)
> * [ListViewWrapper.IsChecked](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.IsChecked)
> * [ListViewWrapper.IsFocused](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.IsFocused)
> * [ListViewWrapper.IsSelected](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.IsSelected)
> * [ListViewWrapper.ItemCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.ItemCount)
> * [ListViewWrapper.Items](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.Items)
> * [ListViewWrapper.Select](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.Select)
> * [ListViewWrapper.Deselect](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.Deselect)
> * [ListViewWrapper.UnCheck](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ListViewWrapper.UnCheck)

### PopupMenu

(no extra visible methods)

### ReBar

> * [ReBarWrapper.BandCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ReBarWrapper.BandCount)
> * [ReBarWrapper.GetBand](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ReBarWrapper.GetBand)
> * [ReBarWrapper.GetToolTipsControl](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ReBarWrapper.GetToolTipsControl)

### Static

(no extra visible methods)

### StatusBar

> * [StatusBarWrapper.BorderWidths](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.StatusBarWrapper.BorderWidths)
> * [StatusBarWrapper.GetPartRect](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.StatusBarWrapper.GetPartRect)
> * [StatusBarWrapper.GetPartText](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.StatusBarWrapper.GetPartText)
> * [StatusBarWrapper.PartCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.StatusBarWrapper.PartCount)
> * [StatusBarWrapper.PartRightEdges](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.StatusBarWrapper.PartRightEdges)

### TabControl

> * [TabControlWrapper.GetSelectedTab](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TabControlWrapper.GetSelectedTab)
> * [TabControlWrapper.GetTabRect](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TabControlWrapper.GetTabRect)
> * [TabControlWrapper.GetTabState](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TabControlWrapper.GetTabState)
> * [TabControlWrapper.GetTabText](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TabControlWrapper.GetTabText)
> * [TabControlWrapper.RowCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TabControlWrapper.RowCount)
> * [TabControlWrapper.Select](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TabControlWrapper.Select)
> * [TabControlWrapper.TabCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TabControlWrapper.TabCount)
> * [TabControlWrapper.TabStates](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TabControlWrapper.TabStates)

### Toolbar

> * [ToolbarWrapper.Button](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ToolbarWrapper.Button)
> * [ToolbarWrapper.ButtonCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ToolbarWrapper.ButtonCount)
> * [ToolbarWrapper.GetButton](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ToolbarWrapper.GetButton)
> * [ToolbarWrapper.GetButtonRect](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ToolbarWrapper.GetButtonRect)
> * [ToolbarWrapper.GetToolTipsControl](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ToolbarWrapper.GetToolTipsControl)
> * [ToolbarWrapper.PressButton](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ToolbarWrapper.PressButton)

> *ToolbarButton* (returned by `Button()`)
>
> > * [ToolbarButton.Rectangle](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._toolbar_button.Rectangle)
> > * [ToolbarButton.Style](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._toolbar_button.Style)
> > * [ToolbarButton.click_input](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._toolbar_button.click_input)
> > * [ToolbarButton.Click](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._toolbar_button.Click)
> > * [ToolbarButton.IsCheckable](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._toolbar_button.IsCheckable)
> > * [ToolbarButton.IsChecked](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._toolbar_button.IsChecked)
> > * [ToolbarButton.IsEnabled](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._toolbar_button.IsEnabled)
> > * [ToolbarButton.IsPressable](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._toolbar_button.IsPressable)
> > * [ToolbarButton.IsPressed](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._toolbar_button.IsPressed)
> > * [ToolbarButton.State](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._toolbar_button.State)

### ToolTips

> * [ToolTipsWrapper.GetTip](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ToolTipsWrapper.GetTip)
> * [ToolTipsWrapper.GetTipText](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ToolTipsWrapper.GetTipText)
> * [ToolTipsWrapper.ToolCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.ToolTipsWrapper.ToolCount)

### TreeView

> * [TreeViewWrapper.EnsureVisible](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TreeViewWrapper.EnsureVisible)
> * [TreeViewWrapper.GetItem](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TreeViewWrapper.GetItem)
> * [TreeViewWrapper.GetProperties](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TreeViewWrapper.GetProperties)
> * [TreeViewWrapper.IsSelected](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TreeViewWrapper.IsSelected)
> * [TreeViewWrapper.ItemCount](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TreeViewWrapper.ItemCount)
> * [TreeViewWrapper.Root](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TreeViewWrapper.Root)
> * [TreeViewWrapper.Select](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.TreeViewWrapper.Select)

> *TreeViewElement* (returned by `GetItem()` and `Root()`)
>
> > * [TreeViewElement.Children](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._treeview_element.Children)
> > * [TreeViewElement.Item](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._treeview_element.Item)
> > * [TreeViewElement.Next](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._treeview_element.Next)
> > * [TreeViewElement.Rectangle](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._treeview_element.Rectangle)
> > * [TreeViewElement.State](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._treeview_element.State)
> > * [TreeViewElement.SubElements](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._treeview_element.SubElements)
> > * [TreeViewElement.Text](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls._treeview_element.Text)

### UpDown

> * [UpDownWrapper.GetBase](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.UpDownWrapper.GetBase)
> * [UpDownWrapper.GetBuddyControl](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.UpDownWrapper.GetBuddyControl)
> * [UpDownWrapper.GetRange](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.UpDownWrapper.GetRange)
> * [UpDownWrapper.GetValue](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.UpDownWrapper.GetValue)
> * [UpDownWrapper.SetValue](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.UpDownWrapper.SetValue)
> * [UpDownWrapper.Increment](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.UpDownWrapper.Increment)
> * [UpDownWrapper.Decrement](https://www.kancloud.cn/gnefnuy/pywinauto_doc/code/pywinauto.controls.common_controls.html#pywinauto.controls.common_controls.UpDownWrapper.Decrement)

# pywinauto.mouse

跨平台模块模拟真实用户的鼠标事件

```python
pywinauto.mouse.click(button='left', coords=(0, 0)) #单击指定的坐标
pywinauto.mouse.double_click(button='left', coords=(0, 0)) #双击指定的坐标
pywinauto.mouse.move(coords=(0, 0)) #移动鼠标
pywinauto.mouse.press(button='left', coords=(0, 0)) #按下鼠标按钮
pywinauto.mouse.release(button='left', coords=(0, 0)) #释放鼠标按钮
pywinauto.mouse.right_click(coords=(0, 0)) #右键单击指定的坐标
pywinauto.mouse.scroll(coords=(0, 0), wheel_dist=1) #滚动鼠标滚轮
pywinauto.mouse.wheel_click(coords=(0, 0)) #鼠标中键单击指定的坐标
```

# pywinauto.keyboard

* `type_keys`

```python
app.window(handle=0x000D0648).type_keys('^p') # ctrl+p 搜索
```
* `send_keys`

```python
send_keys('^a^c') # 全选（Ctrl + A）并复制到剪贴板（Ctrl + C）
send_keys('+{INS}') # 从剪贴板插入（Shift + Ins）
send_keys('%{F4}') # 使用Alt + F4关闭活动窗口 
send_keys("{VK_SHIFT down}"
          "pywinauto"
          "{VK_SHIFT up}") # to type PYWINAUTO

send_keys("{h down}"
          "{e down}"
          "{h up}"
          "{e up}"
          "llo") # to type hello 
send_keys("{ENTER 2}")# to type enter twice

#使用花括号来转义修饰符
send_keys('{^}a{^}c{%}') # 键入字符串 "^a^c%" (不会按下Ctrl键)
send_keys('{{}ENTER{}}') # 键入字符串“{ENTER}”而不按Enter键 
```

**可用的按键代码:**

```python
{SCROLLLOCK}, {VK_SPACE}, {VK_LSHIFT}, {VK_PAUSE}, {VK_MODECHANGE},
{BACK}, {VK_HOME}, {F23}, {F22}, {F21}, {F20}, {VK_HANGEUL}, {VK_KANJI},
{VK_RIGHT}, {BS}, {HOME}, {VK_F4}, {VK_ACCEPT}, {VK_F18}, {VK_SNAPSHOT},
{VK_PA1}, {VK_NONAME}, {VK_LCONTROL}, {ZOOM}, {VK_ATTN}, {VK_F10}, {VK_F22},
{VK_F23}, {VK_F20}, {VK_F21}, {VK_SCROLL}, {TAB}, {VK_F11}, {VK_END},
{LEFT}, {VK_UP}, {NUMLOCK}, {VK_APPS}, {PGUP}, {VK_F8}, {VK_CONTROL},
{VK_LEFT}, {PRTSC}, {VK_NUMPAD4}, {CAPSLOCK}, {VK_CONVERT}, {VK_PROCESSKEY},
{ENTER}, {VK_SEPARATOR}, {VK_RWIN}, {VK_LMENU}, {VK_NEXT}, {F1}, {F2},
{F3}, {F4}, {F5}, {F6}, {F7}, {F8}, {F9}, {VK_ADD}, {VK_RCONTROL},
{VK_RETURN}, {BREAK}, {VK_NUMPAD9}, {VK_NUMPAD8}, {RWIN}, {VK_KANA},
{PGDN}, {VK_NUMPAD3}, {DEL}, {VK_NUMPAD1}, {VK_NUMPAD0}, {VK_NUMPAD7},
{VK_NUMPAD6}, {VK_NUMPAD5}, {DELETE}, {VK_PRIOR}, {VK_SUBTRACT}, {HELP},
{VK_PRINT}, {VK_BACK}, {CAP}, {VK_RBUTTON}, {VK_RSHIFT}, {VK_LWIN}, {DOWN},
{VK_HELP}, {VK_NONCONVERT}, {BACKSPACE}, {VK_SELECT}, {VK_TAB}, {VK_HANJA},
{VK_NUMPAD2}, {INSERT}, {VK_F9}, {VK_DECIMAL}, {VK_FINAL}, {VK_EXSEL},
{RMENU}, {VK_F3}, {VK_F2}, {VK_F1}, {VK_F7}, {VK_F6}, {VK_F5}, {VK_CRSEL},
{VK_SHIFT}, {VK_EREOF}, {VK_CANCEL}, {VK_DELETE}, {VK_HANGUL}, {VK_MBUTTON},
{VK_NUMLOCK}, {VK_CLEAR}, {END}, {VK_MENU}, {SPACE}, {BKSP}, {VK_INSERT},
{F18}, {F19}, {ESC}, {VK_MULTIPLY}, {F12}, {F13}, {F10}, {F11}, {F16},
{F17}, {F14}, {F15}, {F24}, {RIGHT}, {VK_F24}, {VK_CAPITAL}, {VK_LBUTTON},
{VK_OEM_CLEAR}, {VK_ESCAPE}, {UP}, {VK_DIVIDE}, {INS}, {VK_JUNJA},
{VK_F19}, {VK_EXECUTE}, {VK_PLAY}, {VK_RMENU}, {VK_F13}, {VK_F12}, {LWIN},
{VK_DOWN}, {VK_F17}, {VK_F16}, {VK_F15}, {VK_F14} 
```

**修饰符:**

* `'+': {VK_SHIFT}`
* `'^': {VK_CONTROL}`
* `'%': {VK_MENU}` a.k.a. Alt键

# pywinauto.findbestmatch

> ```python
> find_best_matches(search_text, clean=False, ignore_case=False)
> ```

返回项目中search_text的最佳匹配项

* **search_text** 要查找的文本
* **clean** 是否从字符串中清除非文本字符
* **ignore_case** 比较字符串不区分大小写

> ```python
> find_best_matches(search_text, clean=False, ignore_case=False)
> get_control_names(control, allcontrols, textcontrols)
> get_non_text_control_name(ctrl, controls, text_ctrls)
> ```