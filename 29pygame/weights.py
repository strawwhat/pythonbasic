#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
ubuntu 16.10 python3
sudo pip install pygame
安装 pygame-1.9.3

文档
http://www.pygame.org/docs/

方法索引
pygame v1.9.2 documentation 
https://www.pygame.org/docs/genindex.html#G

---------------------------------------------------

简单的“天上掉秤砣”动画(weights.py)

"""

import sys, pygame
from pygame import *
from random import randrange

class Weight(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = Weight_image
		#get_rect()返回一个Rect实例，包括渲染文本的大小和偏移量
		self.rect = self.image.get_rect()
		self.reset()

	def reset(self):
		"""
		将秤砣移动到屏幕顶端的随机位置. http://www.pygame.org/docs/ref/rect.html
		Pygame使用Rect对象来存储和操作矩形区域。
		Rect对象具有几个虚拟属性，可用于移动和对齐Rect：top laft centerx...
		"""
		self.rect.top = -self.rect.height
		self.rect.centerx = randrange(screen_size[0])

	def update(self):
		"""
		更新秤砣，显示下一帧
		self.rect.top增加到大于600时更新图像，
		设置的显示尺寸高为600,也就是秤砣下降到显示屏幕底部更新
		"""
		self.rect.top += 1
		if self.rect.top > screen_size[1]:
			self.reset()

#初始化
#pygame.init()初始化所有导入的pygame模块,display.set_mode()初始化用于显示的窗口或屏幕
#set_mode(resolution=(0,0), flags=0, depth=0)初始化用于显示的窗口或屏幕
#resolution参数是表示宽度和高度的一对数字。flags 参数是附加选项的集合。深度参数表示用于颜色的位数。
#pygame.mouse.set_visible()隐藏或显示鼠标光标
pygame.init()
screen_size = 800,600
pygame.display.set_mode(screen_size, RESIZABLE)#FULLSCREEN
pygame.mouse.set_visible(0)

#载入秤砣的图像pygame.image.load()从文件源加载图像
#convert()创建更改像素格式的Surface的新副本
#没有参数调用convert()新的surface将具有与display surface相同的像素格式，并以尽可能快的速度显示新surface
Weight_image = pygame.image.load('/home/asu/Download/pic.jpg')
Weight_image = Weight_image.convert() #...to match the display 匹配显示

#创建一个子图形组(sprite group)，增加Weight
#pygame.sprite.RenderUpdates()此类派生自 pygame.sprite.Group().它具有一个扩展的draw()方法来跟踪屏幕的变化区域。
#RenderUpdates按照添加顺序绘制Sprites的子类。add()将sprites对象添加到此组
sprites = pygame.sprite.RenderUpdates()
sprites.add(Weight())

#读取屏幕表面 #pygame.display.get_surface()返回一个可用于画图的surface对象
#色彩通过RGB三原色表示，(红绿蓝，每个值的范围为0-255)
#pygame.Surface.fill()用纯色填充表面如果没有rect参数,整个Surface将被填充.rect参数将限制填充到特定区域 #pygame.display.flip()将全部显示更新到屏幕
screen = pygame.display.get_surface()
bg = (255,255,255)#white
screen.fill(bg)
pygame.display.flip()

#用于清除子图形
def clear_callback(surf, rect):
	surf.fill(bg, rect)

#
while True:
	#检查退出事件
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit()
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			sys.exit()
	#清除前面的位置
	#擦除最后一个Group.draw()调用中使用的Sprite。
	#但是, 它也可以是采用两个参数的回调函数;目标曲面和要清除的区域。后台回调函数会被多次调用。
	sprites.clear(screen, clear_callback)
	#更新所有子图形。当调用Group对象的update方法时，它就会自动调用所有Srite对象的update方法
	sprites.update()
	
	#绘制所有子图形 draw刷新Sprite图像并跟踪更改的区域
	#将所有Sprite绘制到表面,与Group.draw()相同。此方法还返回屏幕上已更改的矩形区域列表。
	#返回的Rect列表应该传递给pygame.display.update().这将有助于在软件驱动的显示模式下的性能.
	#这种类型的更新通常仅对具有非动画背景的目的地有帮助。
	updates = sprites.draw(screen)
	#print(updates)[<rect(320, 598, 176, 2)>] #[<rect(320, 600, 0, 0)>, <rect(320, 599, 176, 1)>]

	#更新所需的显示部分. 更新给定参数矩形列表部分
	#它只允许更新屏幕的一部分,而不是整个区域.如果没有参数传递,则会更新整个Surface区域,如pygame.display.flip
	pygame.display.update(updates)
	#pygame.display.flip()不在乎性能使用filp()更新整个显示区域



