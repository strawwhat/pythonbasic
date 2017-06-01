#!/usr/bin/python
# *-*coding:utf-8 *-*

#python3 新的Node控制器界面(client.py)

#from xmlrpclib import ServerProxy, Fault
from xmlrpc.client import ServerProxy, Fault

from cmd import Cmd
from random import choice

#from string import lowercase
from string import ascii_lowercase

from server import Node, UNHANDLED
from threading import Thread
from time import sleep
import sys

HEAD_START = 0.1#Seconds
SECRET_LENGTH = 100

def randomString(length):
	"""
	返回给定长度的由字母组成的随机字符串
	"""
	chars = []
	#letters = lowercase[:26]
	letters = ascii_lowercase[:26]
	while length > 0:
		length -= 1
		chars.append(choice(letters))
	return ''.join(chars)

class Client(Cmd):
	"""
	Node类的简单的基于文本的界面
	"""
	promt = '>'
	
	def __init__(self, url, dirname, urlfile):
		"""
		设定url， dirname和urlfile，并且在单独的线程中启动Node服务器
		"""
		Cmd.__init__(self)
		self.secret = randomString(SECRET_LENGTH)
		n = Node(url, dirname, self.secret)
		t = Thread(target=n._start)
		t.setDaemon(1)
		t.start()
		#停0.1秒让服务器先启动
		sleep(HEAD_START)
		self.server = ServerProxy(url)
		for line in open(urlfile, 'r'):
			line = line.strip()
			self.server.hello(line)

	
	def do_fetch(self, arg):
		"""调用服务器的fetch方法"""
		try:
			self.server.fetch(arg, self.secret)
		except Fault as f:
			if f.faultCode != UNHANDLED: raise
			print("Couldn't find the file", arg, f.faultCode, UNHANDLED, f)
	
	def do_exit(self, arg):
		"""退出程序 打印空行处于美观考虑..."""
		print()
		sys.exit()
	
	do_EOF = do_exit #EoF与'exit'同义

#获取命令输入，添加到client中
def main():
	urlfile, directory, url = sys.argv[1:]
	client = Client(url, directory, urlfile)
	client.cmdloop()

if __name__ == '__main__':
	main()

"""
命令行 $ python client.py ~/urls.txt ~/directory/  http://localhost:4242
		$ python client.py ~/urls.txt ~/directory/  http://localhost:4243
	
urls.txt中每一行都包括程序所知道的其他节点的url地址
初始时4242端口的directory中没有要查询的文件。如果只运行4242命令行调用do_fetch，_broadcast的第二个except捕捉Connection refused错误。do_fetch返回Couldn'file，原因是4243的节点服务器还没有启动。
只运行4242不运行4243就会返回返回错误


"""
