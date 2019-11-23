#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-20 22:03:56
# @Author  : jge (173371929@qq.com)
# @Link    : ${link}
# @Version : $Id$

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.properties import StringProperty

class RootWidget(BoxLayout):
    def __init__(self,**kwargs):
        super(RootWidget,self).__init__(**kwargs)
        self.add_widget(Button(text='btn1'))
        cus_btn = CustomButton()
        cus_btn.bind(pressed=self.btn_pressed)
#         cus_btn.bind(btn_name) #错的,想加一个标签？
        self.add_widget(cus_btn)
        self.add_widget(Button(text='btn3'))
    def btn_pressed(self,instance,pos):
        print('pos:printed from root widget:{pos}'.format(pos=pos))
class CustomButton(Widget):
    pressed = ListProperty([0,0])
#     btn_name = StringProperty('btn2')
    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            return True
        return super(CustomButton,self).on_touch_down(touch)
    def on_pressed(self,instance,pos):
        print('pressed at {pos}'.format(pos=pos))
class TestApp(App):
    def build(self):
        return RootWidget()
if __name__ == '__main__':
    TestApp().run()
# TestApp().run()
