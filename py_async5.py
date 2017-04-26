#/usr/bin/python
# *-* coding:utf-8 *-*

"""
多个聊天室的版本
转载自 https://bblove.me/2015/03/26/python-im/
"""

from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore

PORT = 5005
NAME = 'TestChat'

class EndSession(Exception): pass

class CommandHandler():
	"""
	类似于标准库中cmd.Cmd的简单命令处理程序
	"""
	
	#响应未知的命令
	def unknown(self, session, cmd):
		session.push('Unknown command: %s \r\n' % cmd)
	
	def handle(self, session, line):
		if not line.strip():
			return
		parts = line.split(' ', 1)
		cmd = parts[0]
		try:
			line = parts[1].strip()
		except IndexError: line = ''
		meth = getattr(self, 'do_'+ cmd, None)
		try:
			meth(session, line)
		except TypeError:
			self.unknown(session, cmd)

#聊天室的主类，继承上面的类是为例继承命令的功能
class ChatRoom(CommandHandler):
	def __init__(self, name, server):
		self.server = server
		self.name = name
		self.sessions = []
	
	def add(self, session):
		self.broadcast(session.name + ' has entered the room %s\r\n' %self.name)
		session.push('You can type "h" for help\r\n')
		#因为后面要将用户挪动房间，所以必须保存每个用户的session，这样才能挪动和删除
		self.server.users[session.name] = session
		self.sessions.append(session)
	
	def remove(self, session):
		try:
			self.sessions.remove(session)
		except: pass #如果此处的session为空或者已经不存在，会出错，此处不上报
	
	def broadcast(self, line):
		#广播，只广播到当前房间
		for session in self.sessions:
			session.push(line)
	
	def do_say(self, session, line):
		#发言
		self.broadcast(session.name + ':' + line + '\r\n')
	
	def do_login(self, session, line):
		#实现改名字的功能，登录房间
		name = line.strip()
		if not name:
			session.push('Please enter a name\r\n')
		elif name in self.server.users.keys():
			session.push('The name %s taken\r\n' % name)
			session.push('Please try again\r\n')
		else:
			session.server.users[name] = session.server.users.pop(session.name)
			session.name = name
			session.enter(self)
			self.do_list(session, '')
			session.push('type "select name" to choose one room\r\n')
	
	def do_logout(self, session, line):
		'退出'
		raise EndSession

	def do_look(self, session, line):
		session.push('The following are in this room: \r\n')
		for other in self.sessions:
			session.push(other.name + "\r\n")
	
	#查看当前在线的用户，所有房间的用户
	def do_who(self, session, line):
		session.push('The following are logged in: \r\n')
		for name in self.server.users:
			session.push(name + '\r\n')
	
	#查看当前所有的房间
	def do_list(self, session, line):
		session.push('The room list is below\r\n')
		session.push('  '.join(self.server.rooms) + '\r\n')
	
	#选择房间
	def do_select(self, session, line):
		name = line.strip()
		if not name:
			session.push('Please enter a name\r\n')
		elif name in self.server.rooms.keys():
			session.enter(self.server.rooms[name])
			self.broadcast(' %s, Welcome to join %s\r\n' %(session.name, name))
	
	#输出帮助
	def do_h(self, session, line):
		session.push('you can use this command: \r\n1, who to see who is on this server(online and offline)\r\n2,'
		'list to see how many room are avaliable\r\n3, look to see who are in this room\r\n4,login to login online and'
		'change a name\r\n5, create to create a new room\r\n')
		
	#创建新房间
	def do_create(self, session, line):
		name = line.strip()
		if not name:
			session.push('Please enter a name\r\n')
		elif name in self.server.rooms.keys():
			session.push('The room name %s is taken\r\n' % name)
			session.push('Please try again\r\n')
		else:
			ChatRoom(name, self.server)
			session.server.rooms[name] = ChatRoom(name, self.server)
			session.push('The room %s create successful\r\n' % name)
			session.enter(session.server.rooms[name])

#每个用户会话类， 这是个重点类
class ChatSession(async_chat):

	def __init__(self, server, sock):
		async_chat.__init__(self, sock)
		self.server = server
		self.set_terminator('\r\n')
		self.data = []
		self.name = 'vistor' + str(len(server.users)) #初始化用户名，用vistor1之类表示
		self.room = self.server.main_room
		self.enter(self.server.main_room)
	
	def enter(self, room):
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
		try:
			self.room.handle(self, line)
		except EndSession:
			self.handle_close()
	
	def handle_close(self):
		async_chat.handle_close(self)


class ChatServer(dispatcher):

	def __init__(self, port, name):
		dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(('', port))
		self.listen(5)
		self.sesions = {}
		self.name = name
		self.users = {}
		self.rooms = {}
		#新建一个房间hall，因为每个初始登录的用户都没有房间，但是操作是依赖于ChatRoom类的，所以设置一个默认初始房间
		self.main_room = ChatRoom('hall', self)
		self.rooms[self.main_room.name] = self.main_room
	
	def handle_accept(self):
		conn, addr = self.accept()
		ChatSession(self, conn)
		print('Connection attempt from', addr[0])

if __name__ == '__main__':
	print('Server Start')
	s = ChatServer(PORT, NAME)
	try:
		asyncore.loop()
	except KeyboardInterrupt: print('End Run')


