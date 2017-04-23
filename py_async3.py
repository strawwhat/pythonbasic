#/usr/bin/python
# *-*coding:utf-8 *-*


"""
#python 基础教程 24章 24-5 简单的聊天的服务器

#telnet 127.0.0.1 5005连接， 设置退出符号 telnet -e '=' 输入quit退出 
#python3连接后报错 error: uncaptured python exception, closing channel
#(<class 'TypeError'>:('data argument must be byte-ish (%r)'
#使用 encode('utf-8')转码

问题的解答链接
https://segmentfault.com/q/1010000000616608
http://stackoverflow.com/questions/24928908/python3-type-str-doesnt-support-the-buffer-api
"""


from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore

PORT = 5005

NAME = 'TestChat'

class ChatSession(async_chat):
	"""
	处理服务器和一个用户之间连接的类
	"""
	
	def __init__(self, server, sock):
		#标准设置任务
		async_chat.__init__(self, sock)
		self.server = server
		self.set_terminator(b'\r\n')
		self.data = []
		
		self.push('Welcome to %s \r\n' % self.server.name)
		#python3中用encode('utf-8')转码
		#self.push("Welcome to %s \r\n".encode('utf-8')  % self.server.name.encode('utf-8'))
	
	def collect_incoming_data(self, data):
		self.data.append(data)
		#self.data.append(data.decode('utf-8'))
	
	def found_terminator(self):
		"""
		如果发现了一个终止对象， 也就意味着读入了一个完整的行， 将其广播给每个人
		"""
		line = ''.join(self.data)
		self.data = []
		self.server.broadcast(line)
		#self.server.broadcast(line.encode('utf-8'))
		
	def handle_close(self):
		async_chat.handle_close(self)
		self.server.disconnect(self)

class ChatServer(dispatcher):
	"""
	接受连接并且产生单个会话的类， 它还是会处理到其他会话的广播
	"""
	def __init__(self, port, name):
		#Standard setup, tasks
		dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(('', port))
		self.listen(5)
		self.name = name
		self.sessions = []
		
	def disconnect(self, session):
		self.sessions.remove(session)

	def broadcast(self, line):
		for session in self.sessions:
			session.push(line + b'\r\n')
	
	def handle_accept(self):
		conn, addr = self.accept()
		self.sessions.append(ChatSession(self, conn))

if __name__ == '__main__':
	s = ChatServer(PORT, NAME)
	try: asyncore.loop()
	except KeyboardInterrupt: print('  End run')



"""
创建ChatServer实例对象s， ChatServer对象继承asyncore模块dispatcher类
try 启动asyncore.loop()轮询循环
ChatServer handle_accept()处理连接，创建新的ChatServer对象并且将其追加到self.sessions列表中

ChatSession类继承async_chat类

collect_incoming_data方法 在读取数据时被调用，将数据加入到self.data中
found_terminator方法 发现一个终止符时被调用，将当前数据连接成字符串line，并将self.data重置为空，
然后用chatserver类的broadcast方法将line发送到每一个客户端session
handle_close方法 async_chat.handle_close(self)关闭客户端连接时被自动调用，从sessions会话列表中删除当前客户端会话

"""

	
