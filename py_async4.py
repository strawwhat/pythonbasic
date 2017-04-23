#/usr/bin/python
# *-*coding:utf-8 *-*

"""
python 基础教程24章 24-6 稍复杂些的聊天服务器
"""

from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore

PORT = 5005
NAME = 'TestChat'

#Exception所有异常的基类
class EndSession(Exception): pass

class CommandHandler():
	"""
	类似于标准库中的cmd.Cmd简单命令处理程序
	"""
	
	def unknown(self, session, cmd):
		'响应未知命令'
		session.push('Unknown command: %s\r\n' %cmd)
	
	def handle(self, session, line):
		'处理从给定的会话中接收到的行'
		if not line.strip(): return
		#分离命令 用空格分割字符串，只分割一次
		parts = line.split(' ', 1)
		cmd = parts[0]
		try: line = parts[1].strip()
		except IndexError: line = ''
		#试着查找处理程序
		meth = getattr(self, 'do_'+cmd, None)
		try:
			#假定它是可调用的
			meth(session, line)
		except TypeError:
			#如果不可以被调用， 此段代码响应未知的命令
			self.unknown(session, cmd)

class Room(CommandHandler):
	"""
	包括一个或多个用户(会话)的泛型环境。它负责基本的命令处理和广播。
	"""
	
	def __init__(self, server):
		self.server = server
		self.sessions = []
	
	def add(self, session):
		'一个会话(用户)已经进入房间'
		self.sessions.append(session)
	
	def remove(self, session):
		'一个会话(用户)已离开房间'
		self.sessions.remove(session)
	
	def broadcast(self, line):
		'向房间中的所有会话发送一行'
		for session in self.sessions:
			session.push(line)
	
	def do_logout(self, session, line):
		'响应logout命令'
		raise EndSession

class LoginRoom(Room):
	"""
	为刚刚连接上的用户准备的房间
	"""
	
	def add(self, session):
		Room.add(self, session)
		#当用户进入时， 问候他或她
		self.broadcast('Welcome to %s\r\n'  % self.server.name)
	
	def unknown(self, session, cmd):
		#所有未知命令(除了login或者logout外的一切)会导致一个警告
		session.push('Please log in \n Use "login <nick>"\r\n')
	
	def do_login(self, session, line):
		name = line.strip()
		#确保用户输入了名字
		if not name:
			session.push('Please enter a name\r\n')
		#确保用户名没有被使用
		elif name in self.server.users:
			session.push('The name "%s" is taken.\r\n' %name)
			session.push('Please try again.\r\n')
		else:
			#名字没问题，所以储存在会话中，并且将用户移动到主聊天室
			session.name = name
			session.enter(self.server.main_room)

class ChatRoom(Room):
	"""
	为多用户相互聊天准备的房间。
	"""
	
	def add(self, session):
		#告诉所有人有新用户进入
		self.broadcast(session.name + ' has entered the room.\r\n')
		self.server.users[session.name] = session
		Room.add(self, session)
	
	def remove(self, session):
		Room.remove(self, session)
		#告诉所有人有用户离开
		self.broadcast(session.name + ' has left the room.\r\n')
		
	def do_say(self, session, line):
		'处理say命令，向每个会话发送发言人名称和发言内容'
		self.broadcast(session.name+ ':' + line + '\r\n')
	
	def do_look(self, session, line):
		'处理look命令，该命令用于查看谁在房间内'
		session.push('The follwing are in this room: \r\n')
		for other in self.sessions:
			session.push(other.name + '\r\n')
	
	def do_who(self, session, line):
		'处理who命令， 该命令用于查看谁登录了'
		session.push('The following are logged in : \r\n')
		for name in self.server.users:
			session.push(name + '\r\n')

class LogoutRoom(Room):
	"""
	为单用户准备的房间，只用于将用户名从服务器移除.
	"""
	
	def add(self, session):
		#当前会话(用户)进入要删除的LogoutRoom时
		try:
			del self.server.users[session.name]
		except KeyError:
			pass
	
class ChatSession(async_chat):
	"""
	单会话， 负责和单用户通信
	"""
	def __init__(self, server, sock):
		async_chat.__init__(self, sock)
		self.server = server
		self.set_terminator("\r\n")
		self.data = []
		self.name = None
		#所有的会话都开始于单独的LoginRoom
		self.enter(LoginRoom(server))

	def enter(self, room):
		#从当前房间移除自身(self), 并且将自身添加到下一个房间
		try:
			cur = self.room
		except AttributeError:
			pass
		else:
			cur.remove(self)
		self.room = room
		room.add(self)
	
	def collect_incoming_data(self, data):
		self.data.append(data)
	
	def found_terminator(self):
		line = ''.join(self.data)
		self.data = []
		try: self.room.handle(self, line)
		except EndSession:
			self.handle_close()
	
	def handle_close(self):
		async_chat.handle_close(self)
		self.enter(LogoutRoom(self.server))


"""
collect_incoming_data() 方法在发现数据时被自动调用
found_terminator()方法在发现终止符\r\n被调用，调用handle处理line中包括的命令
将self.data中的数据连接成字符串line， self.data设置为空，
在try语句中 line作为参数给ChatRoom类的handle方法，
handle方法处理从给定的会话中接收到的行。
except EndSession捕捉所有的错误，async_chat.handle_close()关闭套接字,
将LogoutRoom(self.server)传递到self.enter中， 
把一个self(一个从客户端连接的ChatSession对象)从ChatRoom中删除，加入到LogoutRoom中

"""

class ChatServer(dispatcher):
	"""
	只有一个房间的聊天服务器
	"""
	
	def __init__(self, port, name):
		dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(('', port))
		self.listen(5)
		self.name = name
		self.users = {}
		self.main_room = ChatRoom(self)
	
	def handle_accept(self):	
		conn, addr = self.accept()
		ChatSession(self, conn)

if __name__ == '__main__':
	s = ChatServer(PORT, NAME)
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		print(' End run')

"""

初始化ChatServer(), asyncore.loop()轮寻循环

ChatSession() 接收ChatServer()和 handle_accept()连接的客户端套接字 作为参数
Chatsession()继承async_chat, 构造函数调用enter(LoginRoom)进入LoginRoom类。
do_login方法  用login输入名字进入并且确保用户名没有被使用，
然后用session.enter(self.server.main_room)进入ChatRoom()类

"""

