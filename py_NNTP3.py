#/usr/bin/env python
#*-*coding:utf-8 *-*

# python 基础教程23章NNTP 23-2 更灵活的新闻收集代理程序
#python2.7 运行

from nntplib import NNTP
from time import strftime, time, localtime
from email import message_from_string
from urllib import urlopen
import  textwrap
import re

day = 24 * 60 * 60

def wrap(string, max=70):
	"""
	将字符串调整为最大行宽
	"""
	return '\n'.join(textwrap.wrap(string)) + '\n'

class NewsAgent():
	"""
	可以从新闻来源获取新闻项目并且发布到新闻目标的对象
	"""
	def __init__(self):
		self.sources = []
		self.destinations = []
	
	def addSource(self, source):
		self.sources.append(source)
	def addDestination(self, dest):
		self.destinations.append(dest)
	
	def distribute(self):
		"""
		从所有来源获取新闻项目并且发布到所有目标
		"""
		items =[]
		for source in self.sources:
			items.extend(source.getItems())
		for dest in self.destinations:
			dest.receiveItems(items)

class NewsItem():
	"""
	包括主题和主体文本的简单新闻项目
	"""
	def __init__(self, title, body):
		self.title = title
		self.body = body

class NNTPSource():
	"""
	从NNTP组中获取新闻项目的新闻来源
	"""
	def __init__(self, servername, group, window):
		self.servername = servername
		self.group = group
		self.window = window
	
	
	def getItems(self):

		server = NNTP(self.servername)
		(resp, count, frist, last, name) = server.group(self.group)
		(resp, subs) = server.xhdr('subject', (str(frist) + '-' +(last)))
	
		for subject in subs[-10:]:
			title = subject[1]
			(reply, num, id, list) = server.body(subject[0])
			body = ''.join(list)

			#print(num) #186919
			#print(title) #Re: Find out which module a class came from
			#print(''.join(list))#prano wrote:> But for merely ordinary obfuscation caused by poor...
		
			yield NewsItem(title, body)
		server.quit()

"""
书中原例getItems()方法
返回 nntplib.NNTPTemporaryError: 480 NEWNEWS command disabled by administrator
#480管理员禁用NEWNEWS命令

def getItems(self):
	start = localtime(time() - self.window*day)
	date = strftime('%y%m%d', start)
	hour = strftime('%H%M%S', start)
	
	server = NNTP(self.servername)
	ids = server.newnews(self.group, date, hour)[1]
	
	for id in ids:
		lines = serverarticle(id)[3]
		message = message_from_string('\n'.join(lines))
		
		title = message['subject']
		body = message.get_payload()
		if message.is_multipat():
			body = body[0]
		
		yield NewsItem(title, body)
	server.quit()
"""
	


class SimpleWebSource():
	"""
	使用正则表达式从网页中提取新闻项目的新闻来源
	"""
	def __init__(self, url, titlePattern, bodyPattern):
		self.url = url 
		self.titlePattern = re.compile(titlePattern)
		self.bodyPattern = re.compile(bodyPattern)

	def getItems(self):
		text = urlopen(self.url).read()
		titles = self.titlePattern.findall(text)
		bodies = self.bodyPattern.findall(text)
		for title, body in zip(titles, bodies):
			yield NewsItem(title[1], wrap(body[1]))
"""
书中原例 getItems()方法
def getItems(self):
		text = urlopen(self.url).read()
		titles = self.titlePattern.findall(text)
		bodies = self.bodyPattern.findall(text)
		for title, body in zip(titles, bodies):
			yield NewsItem(title, wrap(body))
"""

class PlainDestination():
	"""
	将所有新闻项目格式化为纯文本的新闻目标类
	"""
	def receiveItems(self, items):
		for item in items:
			print item.title
			print '-'*len(item.title)
			print item.body

class HTMLDestination():
	"""
	将所有新闻项目格式化为HTML的目标类
	"""
	def __init__(self, filename):
		self.filename = filename
	
	def receiveItems(self, items):
		
		out = open(self.filename, 'w')
		
		print >> out, """
			<html>
				<head>
					<title>Today's News</title>
				</head>
				<body>
				<h1>Today's News</h1>
		"""
		
		print >> out, '<ul>'
		id = 0
		for item in items:
			id += 1
			print >> out, '<li><a href="#%i">%s</a></li>' % (id, item.title)
		print >> out, '</ul>'
		
		id =0 
		for item in items:
			id += 1
			print >> out, '<h2><a name="%i">%s</a></h2>' % (id, item.title)
			print >> out, '<pre>%s</pre>' %item.body
		
		print >> out, """
			</body>
		</html>
		"""

def runDefaultSetup():
	"""
	来源和目标的默认设置， 可以自己修改
	"""
	agent = NewsAgent()
	
	#从BBS新闻站获取新闻的SimpleWebSource
	bbc_url = 'http://www.bbc.com/news'
	bbc_title = r'<h3 class="(.+?)">(.+?)</h3>'
	bbc_body = r'<p class="(.+?)">(.+?)</p>'
	bbc = SimpleWebSource(bbc_url, bbc_title, bbc_body)
	
	agent.addSource(bbc)
	
	#从 comp.lang.python获取新闻的NNTPSource
	"""
	NNTP服务器 新闻组
	'web.aioe.org', 'comp.lang.python'
	'news.gmane.org',  'gmane.comp.python.committers'
	"""

	clpa_server = 'web.aioe.org' 
	clpa_group = 'comp.lang.python'
	clpa_window = 1
	clpa = NNTPSource(clpa_server, clpa_group, clpa_window)
	
	agent.addSource(clpa)
	
	#增加纯文本目标和HTML目标
	agent.addDestination(PlainDestination())
	agent.addDestination(HTMLDestination('news.html'))
	
	#发布新闻项目
	agent.distribute()

if __name__ == '__main__':
	runDefaultSetup()



