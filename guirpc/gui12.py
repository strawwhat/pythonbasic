#!/usr/bin/python
# *-*coding:utf-8 *-*

#python12章 GUI图形用户界面， wxpython
import wx

##每个wxpython程序都是wx.App的一个实例。False参数表示不要将stdout和stderr重定向到窗口
#创建应用程序对象，负责幕后的所有初始化,如果无法工作可能需要将它替换为wx.PysimpleApp
app = wx.App(False)
win = wx.Frame(None, title="Simple Editor", size=(410,335))#wx.Frame是一个顶层窗口
bkg = wx.Panel(win)#面板背景组件，一个面板是一个放置控件的窗口，通常放置在一个框架内

#wx.Button.__init__(parent, id=-1, label="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, validator=wx.DefaultValidator, name=wx.ButtonNameStr)
loadButton = wx.Button(bkg,label='open')#, pos=(315, 30), size=(50,25))#增加按钮使用win作为父参数实例化wx.Button即可
saveButton = wx.Button(bkg, label='save')#, pos=(200,30), size=(50, 25))#在创建部件的标签时使用构造函数label参数设定它们的标签

positionButton = wx.Button(bkg, label='position')#, pos=(200,5),size=(80,25))
establishButton = wx.Button(bkg, label='establish')#, pos=(315,5), size=(80,25))

#wxTextCtrl这个控件让用户输入文本。它产生两个主要事件。每当文本更改时调用EVT_TEXT。每按一次键即调用EVT_CHAR。
filename = wx.TextCtrl(bkg)#,pos=(2,2),size=(180,25))#默认文本控件
#创建文本区值使用style参数即可，style参数的值实际上是个整数，但不用直接指定可以使用按位或运算符
#OR(或者管道运算符 |)联合wx模块中具有特殊名字的风格来指定。联合了wx.TE_MULTILINE来获取多行文本区
#以及wx.HSCROLL来获取水平滚动条
contens = wx.TextCtrl(bkg,style=wx.TE_MULTILINE | wx.HSCROLL)# pos=(2,60), size=(390,260),style=wx.TE_MULTILINE | wx.HSCROLL)

hbox = wx.BoxSizer()
#使用尺寸器BoxSizer()有一个决定它是水平还是垂直的参数(wx.HORIZONTAL或者wx.VERTICAL)默认为水平
hbox.Add(filename, proportion=1,flag=wx.EXPAND)
hbox.Add(loadButton, proportion=0,flag=wx.LEFT,border=5)
hbox.Add(saveButton, proportion=0, flag=wx.LEFT,border=5)
hbox.Add(positionButton, proportion=0, flag=wx.LEFT, border=5)
hbox.Add(establishButton, proportion=0, flag=wx.RIGHT, border=5)
#Add方法有几个参数，第一个指定要在尺寸其中包含的控件，
#proportion参数根据在窗口改变大小时所分配的空间设置比例。可以设置为任何数
#flag参数类似于构造函数中的style参数，可以使用按位或运算符连接构造符号常量(symbolic constant)对其进行构造
#wx.LEFT, wx.RIGHT, wx.TOP, wx.BOTTOM, wx.ALL标记决定边框参数应用于哪个边
#border参数用于设置边缘宽度(间隔)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox, proportion=0, flag=wx.EXPAND |wx.ALL, border=5)
#vbox.Add(positionButton, proportion=0, flag=wx.RIGHT, border=5)
#vbox.Add(establishButton, proportion=0, flag=wx.LEFT, border=50)
vbox.Add(contens, proportion=1,
				flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
bkg.SetSizer(vbox)



win.Show()#通过Show()使框架可见，否则它会一直隐藏
app.MainLoop()#启动应用程序MainLoop，其作用是处理事件


---------------------------------------------------------------------------------

#!/usr/bin/python
# *-*coding:utf-8 *-*

#python 第12章GUI 打开读取写入文件

import wx

def load(event):
	file = open(filename.GetValue())
	contents.SetValue(file.read())
	file.close()

def save(event):
	file = open(filename.GetValue(), 'w')
	file.write((contents.GetValue()).encode('utf-8'))
	file.close()

app = wx.App()
win = wx.Frame(None, title="Simple Editor", size=(410, 335))

bkg = wx.Panel(win)

loadButton = wx.Button(bkg, label='Open')
loadButton.Bind(wx.EVT_BUTTON, load)

saveButton = wx.Button(bkg, label="Save")
saveButton.Bind(wx.EVT_BUTTON, save)

filename = wx.TextCtrl(bkg)
contents = wx.TextCtrl(bkg, style=wx.TE_MULTILINE | wx.HSCROLL)

hbox = wx.BoxSizer()
hbox.Add(filename, proportion=1,flag=wx.EXPAND)
hbox.Add(loadButton, proportion=0, flag=wx.LEFT, border=5)
hbox.Add(saveButton, proportion=0, flag=wx.LEFT, border=5)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(contents, proportion=1,
				flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

bkg.SetSizer(vbox)
win.Show()
app.MainLoop()

