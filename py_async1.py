#/usr/bin/python
# *-*coding:utf-8 *-*


"""
#python 基础教程 24章 24-3具有一些清理功能的基本服务器

asyncore模块链接：https://docs.python.org/3/library/asyncore.html
asynchat模块链接 https://docs.python.org/3/library/asynchat.html
socket模块链接 https://docs.python.org/3/library/socket.html

asyncore模块中的dispatcher类基本上就是一个套接字对象
create_socket方法创建一个套接字，然后利用bind把服务器绑定到具体的地址上(主机名和端口)
主机名为空(空字符串，意味着本地主机，或者更专业一点来说是 '本机的所有接口')
listen方法监听进入的连接，参数为允许排队等待的连接数目
set_reuse_addr()调用可以在服务器没有正确关闭的情况下重用一个地址(具体来说是端口号)
handle_accept方法会调用允许客户端连接的self.accept函数
它返回一个连接(针对客户端的具体套接字)和一个地址(有关所连接计算机的信息)
loop方法 启动轮询循环监听 asyncore.loop([timeout[, use_poll[, map[, count]]]])
"""

from asyncore import dispatcher
import socket, asyncore

PORT = 5005

class ChatServer(dispatcher):
	
	def __init__(self, port):
		dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(('', port))
		self.listen(5)

	def handle_accept(self):
		conn, addr = self.accept()
		print("Connection attempt from", addr[0])
		

if __name__ == '__main__':

	s = ChatServer(PORT)
	try:
		asyncore.loop()
	except KeyboardInterrupt:pass
	

