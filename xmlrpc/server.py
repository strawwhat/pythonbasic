#!/usr/bin/python
# *-*coding:utf-8 *-*

#pyhton3 新的Node实现(server.py)
from xmlrpc.client import ServerProxy, Fault, Binary
#from xmlrpclib import ServerProxy, Fault

from os.path import join, abspath, isfile
from xmlrpc.server import SimpleXMLRPCServer
#from SimpleXMLRPCServer import SimpleXMLRPCServer

from urllib.parse import urlparse
#from urlparse import urlparse
import sys

#SimpleXMLRPCServer.allow_reuse_address = 1 #源文件已经是True
MAX_HISTORY_LENGTH = 6
UNHANDLED = 100
ACCESS_DENIED = 200

class UnhandledQuery(Fault):
	"""
	表示无法处理的查询异常
	"""
	def __init__(self, message="Couldn't handle the query"):
		Fault.__init__(self, UNHANDLED, message)

class AccessDenied(Fault):
	"""
	在用户试图访问未被授权的访问的资源时引发的异常
	"""
	def __init__(self, message='Access denied'):
		Fault.__init__(self, ACCESS_DENIED, message)

def inside(dir, name):
	"""
	检查给定的目录中是否有给定的文件名
	"""
	dir = abspath(dir)
	name = abspath(name)
	return name.startswith(join(dir, ''))

def getPort(url):
	"""
	从url中提取端口
	"""
	name = urlparse(url)[1]
	parts = name.split(':')
	return int(parts[-1])
	
class Node:
	"""
	p2p网络中的节点
	"""
	def __init__(self, url, dirname, secret):
		self.url = url
		self.dirname = dirname
		self.secret = secret
		self.known = set()

	def query(self, query, history=[]):
		"""
		查询文件，可能会向其他已知节点请求帮助，将件作为字符串返回
		"""
		try:
			return self._handle(query)
		
		except UnhandledQuery: 
			history = history + [self.url]
			if len(history) >= MAX_HISTORY_LENGTH: raise
			return self._broadcast(query, history)
	
	def hello(self, other):
		"""
		用于将节点介绍给其他节点
		当前节点使用hello将其他节点添加到self.known集合中，调用query-broadcast
		使用其他节点打开下载文件
		"""
		self.known.add(other)
		return 0
	
	def fetch(self, query, secret):
		"""
		节点找到文件并且下载
		open打开文件写入数据
		"""
		if secret != self.secret: raise AccessDenied
		result = self.query(query)
		#f = open(join(self.dirname, query), 'w')
		#f.write(result)
		#传输大的文件图片视频
		f = open(join(self.dirname, query), 'wb')
		f.write(result.data)
		f.close()
		return 0
	
	def _start(self):
		"""用于启动XML_RPC服务器， 将实例注册"""
		s = SimpleXMLRPCServer(("", getPort(self.url)), logRequests=False)
		s.register_instance(self)
		s.serve_forever()
	
	def _handle(self, query):
		"""处理查询请求。 将找到的文件返回"""
		dir = self.dirname
		name = join(dir, query)
		if not isfile(name): raise UnhandledQuery
		if not inside(dir, name): raise AccessDenied
		#使用Binary函数传输图片视频
		return Binary(open(name, 'rb').read())
		#return open(name).read()
	
	def _broadcast(self, query, history):
		"""
		用于将查询广播到所有的已知节点.
		也就是当前节点用helle方法将其他节点添加到self.known中
		用其他节点创建client，然后返回查询值
		"""
		for other in self.known.copy():
			if other in history: continue
			try:
				s = ServerProxy(other)
				return s.query(query, history)

			except Fault as f:
				if f.faultCode == UNHANDLED: pass
				else: self.known.remove(other)

			#except Exception as e:
			except:
				self.known.remove(other)
		raise UnhandledQuery
	
def main():
	url, dirname, secret = sys.argv[1:]
	n = Node(url, dirname, secret)
	n._start()

if __name__ == '__main__':
	main()



