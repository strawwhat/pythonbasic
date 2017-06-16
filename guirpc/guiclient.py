#!/usr/bin/python
# *-*coding:utf-8 *-*

"""28章项目9
python2 完成后的GUI客户端(guiclient.py)
"""

from xmlrpclib import ServerProxy, Fault
from test8 import Node, UNHANDLED
from test9 import randomString
from threading import Thread
from time import sleep
from os import listdir
import sys
import wx

HEAD_START=0.1
SECRET_LENGTH = 100

class ListableNode(Node):
	"""
    Node的扩展版本，可以列出文件目录中的文件
	os.listdir()方法用于返回指定文件夹包含的文件或文件夹的列表，以字母排序
	"""
	def list(self):
		return listdir(self.dirname)

class Client(wx.App):
	"""
	主客户端类，用于设定GUI，启动为文件服务的Node
	"""
	def __init__(self, url, dirname, urlfile):
		"""
		创建一个随机密码来实例化Node，利用Node的_start方法(确保Thread是个无交互的后台程序，这样它会随着程序
		的退出而退出)启动一个Thread，读取URL文件中的所有URL，并且将Node介绍给这些URL，最后设置GUI
		"""
		self.secret = randomString(SECRET_LENGTH)
		n = ListableNode(url, dirname, self.secret)
		t = Thread(target=n._start)
		t.setDaemon(1)
		t.start()

		sleep(HEAD_START)
		self.server = ServerProxy(url)
		for line in open(urlfile):
			line = line.strip()
			self.server.hello(line)
		#运行GUI
		super(Client, self).__init__()


	def updateList(self):
		"""
		使用从服务器Node中获得的文件名更新列表框
		wx.ListBox的Set()方法 清空列表框并向其中添加给定字符串，参数为字符串列表
		"""
		self.files.Set(self.server.list())
		
	def OnInit(self):
		"""
		设置GUI。创建窗体、文本框和按钮，并且进行布局。将提交按钮绑定到self.fetchHandler上
		wx.Frame()框架是一个窗口，其大小和位置可以(通常)由用户改变
		wx.Panel()背景组件是一个放置控件的窗口，它通常放在一个框架内。它的主要目的是在外观和功能上与对话框相似，
		但具有将任何窗口作为父级窗口的灵活性
		wx.TextCtrl()文本控件允许显示和编辑文本。它可以是单行或多行
		wx.Button()按钮是包含文本字符串的控件，它是GUI最常见的元素之一，它可以放在对话框或面板上或者任何其他窗口
		wx.BoxSizer()尺寸器背后的基本理念是，窗口通常被布置在相当简单的基本几何布局，
		通常在一行或一列或几个层次结构中
		SetSizer(sizer, deleteOld=True)将窗口设置为具有给定布局大小，然后窗口拥有该对象
		"""
		win = wx.Frame(None, title="File Sharing Client", size=(500,300))
		bkg = wx.Panel(win)
		self.input = input = wx.TextCtrl(bkg)
		
		submit = wx.Button(bkg, label="Fetch", size=(80,25))
		submit.Bind(wx.EVT_BUTTON, self.fetchHandler)
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(input, proportion=1, flag= wx.ALL | wx.EXPAND, border=10)
		hbox.Add(submit, flag=wx.TOP | wx.BOTTOM | wx.RIGHT, border=10)
		
		self.files = files = wx.ListBox(bkg)
		self.updateList()
		
		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(hbox, proportion=0, flag=wx.EXPAND)
		vbox.Add(files, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
		
		bkg.SetSizer(vbox)
		win.Show()
		return True

	def fetchHandler(self, event):
		"""
		在用户点击"Fetch"按钮时调用，读取文本框中的查询，调用服务器Node的fetch方法。
		处理查询之后，调用updatelist更新文本框列表。如果请求没有被处理则打印错误信息
		"""
		query = self.input.GetValue()
		try:
			self.server.fetch(query, self.secret)
			self.updateList()
		except Fault, f:
			if f.faultCode != UNHANDLED: raise
			#print("Couldn't find the file", query)
			self.files.Set(["Couldn't find the file: {0}".format(query)])

def main():
	urlfile, directory, url = sys.argv[1:]
	client = Client(url, directory, urlfile)
	client.MainLoop()
	
if __name__ == '__main__':
	main()

	
