=====kivy属性=====
	直接在class中，而不是在class的任何方法中创建kivy属性。属性是会自动创建实例属性的类属性。
默认情况下，每个属性都会提供一个on_<propertyname>事件，该属性的状态/值发生更改时会被调用。
--Kivy提供以下属性：
	NumericProperty，StringProperty， ListProperty，ObjectProperty，
	BooleanProperty，BoundedNumericProperty， OptionProperty，
	ReferenceListProperty， AliasProperty， DictProperty。

====kivy设计语言===
#：kivy 1.10.0
<LoginScreen>:
	GridLayout:
		rows:2
		cols:2
		Label:
			text:'username'
		Label:
			text:'password'
=====事件====
---时钟事件
	schedule_once()#允许函数调用一个一次性事件
	schedule_interval()#允许函数调用重复的事件。
	create_trigger() #创建触发事件 。触发器的优点是每帧只能调用一次，即使同一回调安排了多个触发器。
---输入事件
	所有鼠标点击，触摸和滚轮事件都是MotionEvent的事后处理的扩展部分，并通过类中的事件进行分派 。
	on_motion()/on_touch_down()/on_touch_move()/on_touch_up()

---class活动
	基类EventDispatcher使用 Widget的属性来调度变更。当一个小部件改变其位置或大小时，相应的事件会自动被触发。
	另外，可以使用 register_event_type()的 on_press和on_release事件来创建自己的Button事件 。
====非控件对象====
---Animation
	用于在目标时间内将小部件的属性（大小/位置/中心等）更改为目标值。
---transition
	提供了各种功能。您可以使用它们来制作小部件动画并构建非常流畅的用户界面行为。
---Atlas
	是一个用于管理纹理贴图的类，即将多个纹理打包成一个图像。
	这样可以减少加载的图像数量，从而加快应用程序的启动速度。
---Clock
	为您提供了一个方便的方式来按设定的时间间隔安排作业，并优先于 sleep()，这会阻止kivy事件循环。
	这些间隔可以在之前或之后相对于OpenGL绘图指令进行设置 。时钟还为您提供了创建触发事件的方法，
	这些触发事件组合在一起，并在下一帧之前只调用一次。	
	schedule_once()
	schedule_interval()
	unschedule()
	create_trigger()
---UrlRequest
	对于不阻塞事件循环的异步请求非常有用。您可以使用它来通过回调来管理URL请求的进度。
=======布局======
---AnchorLayout：
	小部件可以固定在'顶部'，'底部'，'左'，'右'或'中心'。
---BoxLayout：
	小部件按照“垂直”或“水平”方向依次排列。
---FloatLayout：
	小工具基本上不受限制。
---RelativeLayout：
	子窗口小部件相对于布局定位。
---GridLayout：
	小部件被布置在由定义的一个网格的行和 COLS性质。
---PageLayout：
	用于创建简单的多页面布局，以便使用边框轻松地从一个页面翻页到另一个页面。
---ScatterLayout：
	小部件的定位与RelativeLayout类似，但可以进行翻译，旋转和缩放。
---StackLayout：
	小部件以lr-tb（从左到右，然后从上到下）或tb-lr顺序堆叠。
	将小部件添加到布局时，根据布局的类型，使用以下属性来确定小部件的大小和位置：

	---size_hint：将小部件的大小定义为布局的百分比大小。数值被限制在0.0-1.0的范围内。
	---pos_hint：用于将小部件相对于父项放置。
	//如果将这些值设置为None，则可以直接在屏幕坐标中指定值（x，y，宽度，高度）。

===绘图/画布====
	可以将两种类型的指令添加到画布：上下文指令和顶点指令。
	可以从Python代码或从kv文件中添加说明（首选方法）。
	从kv中添加说明的优点是更改任何属性时控件会自动更新。在Python中，需要自己做这件事。
	可以使用 canvas.before或 canvas.after根据希望执行的时间来添加绘图指令。
