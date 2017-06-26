#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
29-4 主Game模块(Squish.py)
这个模块包括Squish游戏的主要游戏逻辑
"""

import os, sys, pygame
from pygame.locals import *
import objects, config

class State:
	"""泛型游戏的超类，可以处理事件并且在给定的表面上显示自身"""

	def handle(self, event):
		"""只处理退出事件的默认事件处理"""
		if event.type == QUIT:
			sys.exit()
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			sys.exit()

	def firstDisplay(self, screen):
		"""用于第一次显示状态，使用背景颜色填充边界"""
		screen.fill(config.Background_color)
		#调用flip，让更改可见
		pygame.display.flip()

	def display(self, screen):
		"""
		用于在已经显示过一次状态后再次显示。默认的行为是什么都不做
		"""
		pass

class Level(State):
	"""
	游戏等级。用于计算已经落下了多少秤砣，移动子图形以及其他和游戏逻辑相关的任务
	"""
	def __init__(self, number=1):
		self.number = number
		#本关还要落下多少秤砣？
		self.remaining = config.Weights_per_level
		
		speed = config.Drop_speed
		#为每个大于1的等级都增加一个speed_increase
		speed += (self.number-1) * config.Speed_increase
		#创建秤砣和香蕉
		self.weight = objects.Weight(speed)
		self.banana = objects.Banana()
		both = self.weight, self.banana #This could contain more sprites...
		self.sprites = pygame.sprite.RenderUpdates(both)
	
	def update(self, game):
		"从前一帧更新游戏状态"
		#更新所有子图形
		self.sprites.update()
		#如果香蕉碰到了秤砣，那么告诉游戏切换到GameOver状态
		if self.banana.touches(self.weight):
			game.nextState = GameOver()
		#否则在秤砣落地使将其复位。如果本关内的所有秤砣都落下了，则让游戏切换到LevelCleared状态
		elif self.weight.landed:
			self.weight.reset()
			self.remaining -= 1
			if self.remaining == 0:
				game.nextState = LevelCleared(self.number)
	
	def display(self, screen):
		"""
		在第一次显示（只清空屏幕）后显示状态。与firshDisplay不同，这个方法使用
		pygame.display.update对self.sprites.draw提供的、需要更新的矩形列表进行更新
		"""
		screen.fill(config.Background_color)
		updates = self.sprites.draw(screen)
		pygame.display.update(updates)


class Paused(State):
	"""简单的暂停游戏状态。按下键盘上的任意键或点击鼠标都会结束这个状态"""
	finished = 0 #用户结束暂停了吗
	image = None #如果需要图片的话，将这个变量设定为文件名
	text = ''	#将它设定为一些提示性文本

	def handle(self, event):
		"""
		用State的handle的方法处理一般退出事件，以及对按键和鼠标点击作出反映来处理事件
		如果键被按下或者鼠标被点击，将self.finished设定为真
		"""

		State.handle(self, event)
		if event.type in [MOUSEBUTTONDOWN, KEYDOWN]:
			self.finished = 1
	
	def update(self, game):
		"""
		更新等级。如果按键被按下或者鼠标被点击（比如self.finished为真），那么告诉
		游戏切换到下一个由self.nextState()表示的状态（应该由子类实现）
		"""
		if self.finished:
			game.nextState = self.nextState()
	
	def firstDisplay(self, screen):
		"""暂停状态的第一次出现，绘制图像（如果有的话）并且生成文本 """
		#首先，使用填充背景色的方式清空屏幕
		screen.fill(config.Background_color)
		
		#使用默认的外观和指定的大小创建Font对象
		font = pygame.font.Font(None, config.font_size)
		
		#获取self.text中的文本行，忽略开头和结尾的空行
		lines = self.text.strip().splitlines()
		
		#计算文本的高度(使用font.get_linesize())以获取每行文本的像素高度
		height = len(lines) * font.get_linesize()
		#计算文本的放置位置（屏幕中心).屏幕高度的一半减去文本高度的一半
		center, top = screen.get_rect().center
		top -= height // 2 #264
		#如果有图片要显示
		if self.image:
			#载入图片
			image = pygame.image.load(self.image).convert()
			#获取它的rect
			r = image.get_rect()
			#将图片向下移动到其高度的一半距离. 
			top += r.height // 2 
			#将图片放置在文本上方20像素处.
			r.midbottom = center, top-20
			#将图片移动到屏幕上
			screen.blit(image, r)
		
		antialias = 1 #Smooth the text
		black = 0,0,0 #Render it as balck
		
		#生成所有行，从计算过的top开始，并且对于每一行向下移动font.get_linesize()像素
		for line in lines:
			text = font.render(line.strip(), antialias, black)
			r = text.get_rect()
			r.midtop = center, top
			screen.blit(text, r)
			top += font.get_linesize()
		
		#显示所有更改
		pygame.display.flip()

class Info(Paused):
	"""简单的暂停状态，显示有关游戏的信息，在StartUp后显示"""
	nextState = Level
	text = '''
	In this game you are a banana,
	trying to survive a course in
	self-defense against fruit. where the
	particpents will "defend" whemselves
	against you with a 16 ton weight
	'''

class StartUp(Paused):
	"""显示图片和欢迎信息的暂停状态，在Info状态前显示"""
	nextState = Info
	image = config.Splash_image
	text = '''
	Welcome to Squish,
	the game of Fruit Self-Defense
	'''

class LevelCleared(Paused):
	"""提示用户过关的暂停状态。在next Level后显示"""
	def __init__(self, number):
		self.number = number
		self.text = '''Level %i cleared
		Click to start next level ''' % self.number
	
	def nextState(self):
		return Level(self.number+1)

class GameOver(Paused):
	"""提示用户输掉游戏的状态"""
	nextState = Level
	text = '''
	Game Over
	Click to Restart, Esc to Quit'''

class Game:
	"""负责主事件循环的游戏对象，任务包括在不同状态间切换"""
	def __init__(self, *args):
		#获取游戏和图像放置的目录
		path = os.path.abspath(args[0])
		dir = os.path.split(path)[0]
		#移动哪个目录（这样图片文件可以在随后打开）
		os.chdir(dir)
		#无状态方式启动
		self.state = None
		#在第一个事件循环迭代中移动到StateUp
		self.nextState = StartUp()

	def run(self):
		"""
		这个方法动态设定变量，进行一些重要的初始化工作，并且进入主事件循环
		"""
		pygame.init()#初始化所有pygame模块
		#决定以窗口模式还是全屏模式显示游戏
		flag = 0
		if config.full_screen:
			#flag = FULLSCREEN
			flag = RESIZABLE
		
		screen_size = config.Screen_size
		screen = pygame.display.set_mode(screen_size, flag)
		
		pygame.display.set_caption('Fruit Self Defense')
		pygame.mouse.set_visible(False)
		
		#主循环
		while True:
			#1 如果nextState被修改了，那么移动到新状态，并且显示它（第一次）
			if self.state != self.nextState:
				self.state = self.nextState
				self.state.firstDisplay(screen)
			#2代理当前状态的事件处理
			for event in pygame.event.get():
				self.state.handle(event)
			#3 更新当前状态
			self.state.update(self)
			#4显示当前状态
			self.state.display(screen)

if __name__ == '__main__':
	game = Game(*sys.argv)
	game.run()


