# # #给布局添加背景
# # '''纯python语言'''
# # from kivy.app import App
# # from kivy.graphics import Color,Rectangle
# # from kivy.uix.floatlayout import FloatLayout
# # from kivy.uix.button import Button

# # class RootWidget(FloatLayout):
# # 	def __init__(self,**kwargs):
# # 		super(RootWidget,self).__init__(**kwargs)
# # 		self.add_widget(
# # 					Button(
# # 						text='Hello World',
# # 						size_hint=(.5,.5),
# # 						pos_hint={'center_x':.5,'center_y':.5}
# # 						))
# # #添加背景色						
# # class TestApp(App):
# # 	def build(self):
# # 		self.root = root = RootWidget()
# # 		root.bind(size=self._update_rect,pos=self._update_rect)

# # 		with root.canvas.before:
# # 			Color(0, 0.5, 0.5, 1.0)
# # 			self.rect = Rectangle(size=root.size, pos=root.pos)
# # 		return root

# # 	def _update_rect(self,instance,value):
# # 		self.rect.pos = instance.pos
# # 		self.rect.size = instance.size
# # if __name__ == '__main__':
# # 	TestApp().run()

# # '''使用KV语言'''
# # from kivy.app import App
# # from kivy.lang import Builder
# # root = Builder.load_string('''
# # FloatLayout:
# # 	canvas.before:
# # 		Color:
# # 			rgba:0,1,0,1
# # 		Rectangle:
# # 			pos:self.pos
# # 			size:self.size
# # 	Button:
# # 		text:'Hello World'
# # 		size_hint:0.5,0.5
# # 		pos_hint:{'center_x':0.5,'center_y':0.5}
# # ''')
# # class TestApp(App):
# # 	def build(self):
# # 		return root

# # if __name__=='__main__':
# # 	TestApp().run()

# # #自定义布局背景
# # '''纯python语言'''
# # from kivy.app import App
# # from kivy.graphics import Color, Rectangle
# # from kivy.uix.boxlayout import BoxLayout
# # from kivy.uix.floatlayout import FloatLayout
# # from kivy.uix.image import AsyncImage

# # class RootWidget(BoxLayout):
# # 	pass

# # class CustomLayout(FloatLayout):
# # 	def __init__(self,**kwargs):
# # 		super(CustomLayout,self).__init__(**kwargs)
# # 		with self.canvas.before:
# # 			Color(0.5, 0.5, 0.5, 1.0)
# # 			self.rect = Rectangle(size=self.size, pos=self.pos)
# # 		self.bind(size=self._update_rect,pos=self._update_rect)
# # 	def _update_rect(self,instance,value):
# # 		self.rect.size = instance.size
# # 		self.rect.pos = instance.pos

# # class TestApp(App):
# # 	def build(self):
# # 		root = RootWidget()
# # 		c = CustomLayout()
# # 		c.add_widget(
# # 			AsyncImage(
# # 				source='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1526849864452&di=cdfd4d8ab59ccd61dd833e267c8230ce&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimgad%2Fpic%2Fitem%2F9d82d158ccbf6c8154bdd5ccb63eb13533fa4008.jpg',
# # 				size_hint=(1,1),
# # 				pos_hint={'center_x':0.5,'center_y':0.5}))
# # 		root.add_widget(
# # 			AsyncImage(
# # 				source='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1526850135491&di=c4e0e99300a7ecdca1ed26c026f81afd&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimgad%2Fpic%2Fitem%2Fd439b6003af33a87d3332d30cd5c10385343b5b9.jpg',
# # 				size_hint=(1,1),
# # 				pos_hint={'center_x':0.5,'center_y':0.5}))
# # 		root.add_widget(c)
# # 		return root
# # if __name__=="__main__":
# # 	TestApp().run()

# # '''使用Kivy语言'''
# # from kivy.app import App
# # from kivy.uix.floatlayout import FloatLayout
# # from kivy.uix.boxlayout import BoxLayout
# # from kivy.lang import Builder

# # Builder.load_string('''
# # <CustomLayout>
# # 	canvas.before:
# # 		Color:
# # 			rgba:0,1,1,0
# # 		Rectangle:
# # 			pos:self.pos
# # 			size:self.size
# # <RootWidget>
# # 	CustomLayout:
# # 		AsyncImage:
# # 			source:'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1526849864452&di=cdfd4d8ab59ccd61dd833e267c8230ce&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimgad%2Fpic%2Fitem%2F9d82d158ccbf6c8154bdd5ccb63eb13533fa4008.jpg'
# # 			size_hint:1,0.5
# # 			pos_hint:{'center_x':0.5,'center_y':0.5}
# # 	AsyncImage:
# # 		source:'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1526850135491&di=c4e0e99300a7ecdca1ed26c026f81afd&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimgad%2Fpic%2Fitem%2Fd439b6003af33a87d3332d30cd5c10385343b5b9.jpg'
# # ''')

# # class RootWidget(BoxLayout):
# # 	pass
# # class CustomLayout(FloatLayout):
# # 	pass
# # class TestApp(App):
# # 	def build(self):
# # 		return RootWidget()
# # if __name__=='__main__':
# # 	TestApp().run()

# from kivy.app import App
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.gridlayout import GridLayout
# from kivy.lang import Builder

# Builder.load_string('''
# <GridLayout>
# 	canvas.before:
# 		BorderImage:
# 			border: 10, 10, 10, 10
# 			source: "F:/Anaconda3/share/kivy-examples/widgets/sequenced_images/data/images/button_white.png"
# 			pos: self.pos
# 			size: self.size
# <RootWidget>
# 	GridLayout:
# 		size_hint: .9, .9
# 		pos_hint: {'center_x': .5, 'center_y': .5}
# 		rows:1
# 		Label:
# 			text: "I don't suffer from insanity, I enjoy every minute of it"
# 			text_size: self.width-20, self.height-20
# 			valign: 'top'
# 		Label:
# 			text: "When I was born I was so surprised; I didn't speak for a year and a half."
# 			text_size: self.width-20, self.height-20
# 			valign: 'middle'
# 			halign: 'center'
# 		Label:
# 			text: "A consultant is someone who takes a subject you understand and makes it sound confusing"
# 			text_size: self.width-20, self.height-20
# 			valign: 'bottom'
# 			halign: 'justify'
# ''')
# class RootWidget(FloatLayout):
# 	pass
# class TestApp(App):
# 	def build(self):
# 		return RootWidget()
# if __name__ == '__main__':
# 	TestApp().run()

#添加动画背景
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_string('''
<CustomLayout>
	canvas.before:
		BorderImage:
			border: 10, 10, 10, 10
			texture: self.background_image.texture
			pos: self.pos
			size: self.size
<RootWidget>
	CustomLayout:
		size_hint: .9, .9
		pos_hint: {'center_x': .5, 'center_y': .5}
		rows:1
		Label:
			text: "I don't suffer from insanity, I enjoy every minute of it"
			text_size: self.width-20, self.height-20
			valign: 'top'
		Label:
			text: "When I was born I was so surprised; I didn't speak for a year and a half."
			text_size: self.width-20, self.height-20
			valign: 'middle'
			halign: 'center'
		Label:
			text: "A consultant is someone who takes a subject you understand and makes it sound confusing"
			text_size: self.width-20, self.height-20
			valign: 'bottom'
			halign: 'justify'
''')
class CustomLayout(GridLayout):
	background_image = ObjectProperty(
		Image(
			source="F:/Anaconda3/share/kivy-examples/widgets/sequenced_images/data/images/button_white_animated.zip",
			anim_delay=0.1))
class RootWidget(FloatLayout):
	pass
class TestApp(App):
	def build(self):
		return RootWidget()

if __name__ == '__main__':
	TestApp().run()

'''打包'''
######window打包######
#---First---
cd newfile
python -m PyInstaller --name touchtracer --icon "F:/Anaconda3/share/kivy-examples/demo/touchtracer/touchtracer.ico" "F:/Anaconda3/share/kivy-examples/demo/touchtracer/main.py" 

'''pyinstaller -w -F path.py 
-w表示不要控制台
-F表示只打包成一个exe文件(必须大写)。
-n name
-p path1;path2 增加pyinstaller搜索模块的路径,多个路径间加分号
-i path.ico
'''
#-----Second-----
#在打包的文件夹里配置spec文件,如
# from kivy.deps import sdl2,glew,gstreamer
'''
[若程序需要pygame]
def getResource(identifier, *args, **kwargs):
	if identifier == 'pygame_icon.tiff':
		raise IOError()
	return _original_getResource(identifier, *args, **kwargs)
import pygame.pkgdata
_original_getResource = pygame.pkgdata.getResource
pygame.pkgdata.getResource = getResource
'''
# coll = COLLECT(exe,Tree('F:/Anaconda3/share/kivy-examples/demo/touchtracer/'),
#                a.binaries,
#                a.zipfiles,
#                a.datas,
#                *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + gstreamer.dep_bins)],
#                strip=False,
#                upx=True,
#                name='touchtracer')