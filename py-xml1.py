#/usr/bin/env python
# *-*coding:utf-8 *-*

'''
python 教程 22获取标签中的文本

startElement 在标签为h1是设置变量 in_headline 为True 
characters 当in headline为True 也就是在 h1 标签中时 把文本加入到 data中
endElement 在标签为h1时 使用join连接data中的数据， 赋值给text， 并且把data设置为空列表
把连接后的h1标签中的文本加入到 headlines中， 把in_headlines设为False等待下一个h1标签
调用parse读取文本 生成事件

#super函数返回了一个super对象，这个对象负责进行方法解析，当对其特性进行访问同时 它会查找所有的超类(以及超类的超类)，直到找到所需的特性为止(或者引发一个AttributeError)
#super函数不带任何参数进行调用 功能依然具有魔力
'''


from xml.sax.handler import ContentHandler
from xml.sax import parse

class HeadlineHandler(ContentHandler):
	
	in_headline = False
	
	def __init__(self, hdli):
		ContentHandler.__init__(self)
		#super(ContentHandler).__init__() #super().__init__()
		self.headlines = hdli
		self.data = []
	
	def startElement(self, name, attrs):
		if name == 'h1':
			self.in_headline = True
	
	def characters(self, string):
		if self.in_headline:
			self.data.append(string)
		
	def endElement(self, name):
		if name == 'h1':
			text =''.join(self.data)
			self.data = []
			self.headlines.append(text)
			self.in_headline = False


headlines = []
parse('~/py1/website.xml', HeadlineHandler(headlines))

for i in headlines:
	print(i)
