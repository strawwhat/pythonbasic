#/usr/bin/python
# *-*coding:utf-8 *-*


"""
#python 基础教程24章 24-4 带有ChatSession类的服务器程序

在python2中运行，python3需要用 encode('utf-8')转码
set.terminator(term)设置要在信道上识别的终止对象
collect_incoming_data(data)在每次从套接字中读取一些数据时被自动调用
found_terminator()当输入的数据流与set_terminator()设置的终止条件匹配时调用

"""

from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore

PORT = 5005


class ChatSession(async_chat):
	
	def __init__(self, sock):
		async_chat.__init__(self, sock)
		self.set_terminator("\r\n")
		self.data = []
	
	def collect_incoming_data(self, data):
		self.data.append(data)
	
	def found_terminator(self):
		line = ''.join(self.data)
		self.data = []
		#处理这行数据.在服务器端打印出来
		print(line)


class ChatServer(dispatcher):
	
	def __init__(self, port):
		dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(('', port))
		self.listen(5)
		self.sessions = []
		
	def handle_accept(self):
		conn, addr = self.accept()
		self.sessions.append(ChatSession(conn))


if __name__ == '__main__':
	s = ChatServer(PORT)
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		print(' End run')



