# *-*coding:utf-8 *-*

#python 3简单的Node实现 (simple_node.py)
from xmlrpc.client import ServerProxy
from os.path import join, isfile
from xmlrpc.server import SimpleXMLRPCServer
from urllib.parse import urlparse
import sys

def getPort(url):
	'从url中获取节点'
	name = urlparse(url)[1]
	parts = name.split(':')
	return int(parts[-1])

MAX_HISTORY_LENGTH = 6
OK = 1
FAIL = 2
EMPTY = ''

class Node:
	"""
	p2p中的网络节点
	"""
	def __init__(self, url, dirname, secret):
		self.url = url
		self.dirname = dirname
		self.secret = secret
		self.known = set()
	
	def query(self, query, history=[]):
		"""
		查询文件可能向其他已知节点求助， 将文件作为字符串返回
		"""
		code, data = self._handle(query)
		if code == OK:
			return code, data
		else:
			history = history + [self.url]
			if len(history) >= MAX_HISTORY_LENGTH:
				return FAIL, EMPTY
			return self._broadcast(query, history)
	
	def hello(self, other):
		"""
		将节点添加到self.known中
		"""
		self.known.add(other)
		return OK
	
	def fetch(self, query, secret):
		"""
		寻找文件并且下载当前节点目录
		"""
		if secret != self.secret: return FAIL
		code, data = self.query(query)
		if code == OK:
			f = open(join(self.dirname, query), 'w')
			f.write(data)
			f.close()
			return OK
		else:
			return FAIL
	
	def _start(self):
		"""用于启动XML_PRC服务器"""
		s = SimpleXMLRPCServer(("", getPort(self.url)), logRequests=True)
		s.register_instance(self)
		s.serve_forever()
	
	def _handle(self, query):
		"""isfile判断路径是否存在，如果存在返回OK和读取内容"""
		dir = self.dirname
		name = join(dir, query)
		if not isfile(name): return FAIL, EMPTY
		return OK, open(name).read()
	
	def _broadcast(self, query, history):
		"""
		用hello方法加入的self.known中url查询文件
		"""
		for other in self.known.copy():
			if other in history: return FAIL, EMPTY
			try:
				s = ServerProxy(other)
				code, data = s.query(query)
				if code == OK:
					return  code, data
			except:
				self.known.remove(other)
		return FAIL, EMPTY

def main():
	url, dirname, secret = sys.argv[1:]
	n = Node(url, dirname, secret)
	n._start()

if __name__ == '__main__':
	main()

"""
xmlrpc.server, xmlrpc.client, urllib.parse，cmd文档
https://docs.python.org/3/library/xmlrpc.server.html
https://docs.python.org/3/library/xmlrpc.client.html
https://docs.python.org/3/library/urllib.parse.html
https://docs.python.org/3/library/cmd.html

运行节点
$: python simple_node.py http://localhost:4242

连接
>>> from xmlrpc.client import *
>>> one = ServerProxy('http:localhost:4242')
>>> one.query('test.txt') 调用服务器的query方法
"""


