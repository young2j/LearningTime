from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.lang import Builder
from random import randint

Builder.load_string('''
#:kivy 1.0.9 
<PongBall>:
	size:50,50
	canvas:
		Ellipse:
			pos:self.pos
			size:self.size
<PongPaddle>:
	size:25,200
	canvas:
		Rectangle:
			pos:self.pos
			size:self.size
<PongGame>:
	ball:pong_ball  
	player1:player_left
	player2:player_right

    canvas:
        Rectangle:
            pos: self.center_x - 5, 0
            size: 10, self.height
            
    Label:
        font_size: 70  
        center_x: root.width / 4
        top: root.top - 50
        text: str(root.player1.score)
        
    Label:
        font_size: 70  
        center_x: root.width * 3 / 4
        top: root.top - 50
        text: str(root.player2.score)
    PongBall:
    	id:pong_ball
    	center:self.parent.center
    PongPaddle:
    	id:player_left
    	x:root.x
    	center_y:root.center_y
    PongPaddle:
    	id:player_right
    	x:root.width-self.width
    	center_y:root.center_y
	''')
#：kv文件的名称必须与应用程序的名称匹配,例如PongApp（pong.kv）
#Rectangle的pos以及Label的top和center_x是在PongGame类的上下文中定义的，
	#这些属性将在相应的小部件属性更改时自动更新。Kv语言提供自动属性绑定。:)
#ball:pong_ball /id:pong_ball 将球对象挂载进KV文件中,类似于Python类实例化？
class PongPaddle(Widget):
	score = NumericProperty(0)
	def bounce_ball(self,ball):
		if self.collide_widget(ball):
			vx,vy=ball.velocity
			bounced = Vector(-1*vx,vy) #击球反向弹跳
			speed = 1.1
			vel = bounced*speed #获得新的速度
			offset = (ball.center_y-self.center_y)/(self.height/2) #y轴产生偏移
			ball.velocity = vel.x,vel.y+offset

class PongBall(Widget):
	vel_x = NumericProperty(0) 
	vel_y = NumericProperty(0)
	#ReferenceListProperty相当于引用多个属性,如self.velocity表示self.vel_x和self.vel_y
	velocity = ReferenceListProperty(vel_x,vel_y) 
	def move(self):
		self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
	ball = ObjectProperty(None)
	player1 = ObjectProperty(None)
	player2 = ObjectProperty(None)

	def serve_ball(self,vel=(4,0)):
		self.ball.center = self.center
		self.ball.velocity = vel

	def update(self,dt):
		self.ball.move()

		self.player1.bounce_ball(self.ball)
		self.player2.bounce_ball(self.ball)

		if (self.ball.y<self.y) or (self.ball.top>self.top):
			self.ball.vel_y *= -1 
		if self.ball.x<self.x:
			self.player2.score += 1
			self.serve_ball(vel=(4,0))
		if self.ball.x>self.width:
			self.player1.score += 1
			self.serve_ball(vel=(-4,0))
	
	def on_touch_down(self,touch):
		if touch.x < self.width/2:
			self.player1.center_y = touch.y
		if touch.x >self.width/2:
			self.player2.center_y = touch.y

class PongApp(App):
	def build(self):
		game = PongGame()
		game.serve_ball()
		Clock.schedule_interval(game.update,1.0/60.0)
		return PongGame()

if __name__ == '__main__':
    PongApp().run()