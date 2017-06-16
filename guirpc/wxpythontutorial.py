#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
wxPython tutorial
http://zetcode.com/wxpython/
"""

#从技术上讲，wx是一个命名空间。基本模块的所有功能和对象都以wx开头
import wx

#创建一个应用程序对象每个wxPython程序必须有一个应用程序对象。它负责幕后所有的初始化
app = wx.App()
#创建一个wx.Frame对象，它是一个重要的容器构件，也是其他部件的父部件
frame = wx.Frame(None, id=-1, title='simple.py', style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

#show方法显示窗口，mainloop主循环它捕获和调度在应用程序的所有事件
frame.Show()
app.MainLoop()


----------------------------------------------------------

import wx

APP_EXIT=1

class Example(wx.Frame):
	
	def __init__(self, *args, **kwargs):
		super(Example, self).__init__(*args, **kwargs)
		
		#self.Move((0,0))#移动到给定位置
		self.InitUI()
	
	def InitUI(self):

		menubar = wx.MenuBar()#创建一个菜单栏对象
		fileMenu = wx.Menu()#创建一个菜单对象
		##将菜单项添加到菜单对象中，三个参数包括菜单项的ID,名称，简短帮助字符串
		#fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
		#没有明确地创建一个wx.Menuitem,它是由幕后的Append()方法创建的，该方法返回创建的菜单项
		#&字符指定一个快捷键
		#menubar.Append(fileMenu, '&File')
		
		#符号后面的字符加下划线。实际的快捷方式由字符组合定义。我们已经指定了Ctrl+Q字符
		#在＆字符和快捷方式之间放置一个制表符,这样设法在它们之间设置一些空间
		qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
		qmi.SetBitmap(wx.Bitmap('picture.png'))
		fileMenu.AppendItem(qmi)
		
		self.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)
		menubar.Append(fileMenu, '&File')
		#设置菜单
		self.SetMenuBar(menubar)
		#将菜单项的事件wx.EVT_MENU()，绑定到方法上
		#self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
		
		self.SetSize((500,200))
		self.SetTitle('Simple menu')
		#self.Centre()#窗口居中
		self.Show(True)
	
	def OnQuit(self, e):
		self.Close()

def main():
	ex = wx.App()
	Example(None)
	ex.MainLoop()

if __name__ == '__main__':
	main()


----------------------------------------------------------------------------------------
#!/usr/bin/python
# *-*coding:utf-8 *-*

import wx


class Example(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) 
            
        self.InitUI()
        
    def InitUI(self):

        menubar = wx.MenuBar()
		
		#创建新建，打开和保存标准菜单项
        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_NEW, '&New')
        fileMenu.Append(wx.ID_OPEN, '&Open')
        fileMenu.Append(wx.ID_SAVE, '&Save')
        
        #附加了一个菜单分隔符的AppendSeparator()方法
        fileMenu.AppendSeparator()
		
		#一个子菜单也是一个wx.Menu菜单中附加三个菜单项。使用AppenMenu()方法将子菜单附加到文件菜单
        imp = wx.Menu()
        imp.Append(wx.ID_ANY, 'Import newsfeed list...')
        imp.Append(wx.ID_ANY, 'Import bookmarks...')
        imp.Append(wx.ID_ANY, 'Import mail...')

        fileMenu.AppendMenu(wx.ID_ANY, 'I&mport', imp)

        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        fileMenu.AppendItem(qmi)

        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.SetSize((350, 250))
        self.SetTitle('Submenu')
        self.Centre()
        self.Show(True)
        
    def OnQuit(self, e):
        self.Close()

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()


