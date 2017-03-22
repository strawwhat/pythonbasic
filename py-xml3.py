#/usr/bin/env python
#*-*coding:utf-8 *-*

#python 基础教程 22 使用 xml
from xml.sax.handler import ContentHandler
from xml.sax import parse
import os

class Dispatcher():
	"""
	capitalize() 返回一个首字母大写的字符串
	getattr 返回给定对象中所指定的特性的值 如果不存在返回默认值
	callable 检查对象是否可调用
	如果方法可调用 将一个空元组赋值给args， 否则用getattr获取默认处理程序，将args赋值只包括标签名的元组
	如果正使用一个以start起始的程序 将attrs添加到参数元组中 ，最后如果程序可调用使用正确的参数调用
	"""
	def dispatch(self, prefix, name, attrs=None):
		mname = prefix + name.capitalize()
		dname = 'default' + prefix.capitalize()
		method = getattr(self, mname, None)
		if callable(method): args = ()
		else:
			method = getattr(self, dname, None)
			args = name, #使用逗号把str转换成元组
			
		if prefix == 'start': args += attrs,
		if callable(method): method(*args)


	def startElement(self, name, attrs):
		self.dispatch('start', name, attrs)
	
	def endElement(self, name):
		self.dispatch('end', name)


"""
混入(Mix-in)是一种python程序设计中的技术，作用是在运行期间动态改变类的基类或类的方法
从而使得类的表现可以发生变化。可以用在一个通用类接口中

网站的根目录作为参数提供给构造函数， 设置passthrough 变量
writeHeader writeFooter 用于编写首部和页脚
defaultStart defaultEnd 对XHTML进行处理
ensureDirectory检查目录是否存在，否则创建目录， 将目录列表提供给 os join时使用*进行参数分割
startDirectory endDirectory目录处理。 使用directory列表和ensureDirectory方法。
在进入目录时将它的名字追加到列表中 离开时使用pop删除
startPage 用os.path.join连接文件名 打开文件 调用writeHandler 写入头部信息 设置变量
endPage 设置passthrough变量值 调用 writeFooter写入尾部信息 关闭文件
writeHeader writeFooter 用于编写首部 title 和尾部信息
"""		
class WebsiteConstructor(Dispatcher, ContentHandler):
	
	passthrough = False

	def __init__(self, directory):
		self.directory = [directory]
		self.ensureDirectory()
	
	def ensureDirectory(self):
		path = os.path.join(*self.directory)
		if not os.path.isdir(path): os.makedirs(path)
		
	def characters(self, chars):
		if self.passthrough: self.out.write(chars)
		
	def defaultStart(self, name, attrs):
		if self.passthrough:
			self.out.write('<' + name)
			for key, val in attrs.items():
				self.out.write(' %s="%s"' %(key, val))
			self.out.write('>')
	
	def defaultEnd(self, name):
		if self.passthrough:
			self.out.write('</%s>' % name)
			
	def startDirectory(self, attrs):
		self.directory.append(attrs['name'])
		self.ensureDirectory()
	
	def endDirectory(self):
		self.directory.pop()
	
	def startPage(self, attrs):
		filename = os.path.join(*self.directory + [attrs['name']+'.html'])
		self.out = open(filename, 'w')
		self.writeHeader(attrs['title'])
		self.passthrough = True
		
	def endPage(self):
		self.passthrough = False
		self.writeFooter()
		self.out.close()

'''
#xml文件中有中文 在写入文件时添加 <meta charset=\"utf-8\">让浏览器知道以哪种编码打开文件
self.out.write('<html>\n <meta charset=\"utf-8\">\n <head>\n 	<title>')
'''		
	def writeHeader(self, title):
		self.out.write('<html>\n <head>\n	<title>')
		self.out.write(title)
		self.out.write('</title>\n </head>\n	<body>\n')
		
	def writeFooter(self):
		self.out.write('\n </body>\n</html>\n')

parse('~/py1/website.xml', WebsiteConstructor('public_html'))
"""
parse 函数负责读取文本并且生成事件， 由于它要生成事件 所以需要调用一些事件处理程序 
这些事件处理程序会作为内容处理器(content handler)的对象的方法来实现， 需要继承xml.sax. ContentHandler类, 因为它实现了所需要的事件处理程序 (只不过是没有任何效果的伪操作)
可以在需要的时候覆盖这些函数
"""

			
