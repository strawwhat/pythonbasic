#/usr/bin/python
# *-*coding:utf-8 *-*

#python NNTP
# group组返回响应信息

from nntplib import NNTP
with NNTP('news.gmane.org') as n:
	print(n.group('gmane.comp.python.committers'))


server = NNTP('web.aioe.org')

print(server.group('comp.lang.python.announce')[0])

#('211 4419 1 4419 gmane.comp.python.committers', 4419, 1, 4419, 'gmane.comp.python.committers')
#211 100 3923 4023 comp.lang.python.announce


'''
('211 4371 1 4371 gmane.comp.python.committers', 4371, 1, 4371, 'gmane.comp.python.committers')

411 开头意味着服务器没有这个组
nntplib.NNTPTemporaryError: 411 No such group comp.lang.python.announce

211开头 基本上意味着服务器拥有你所请求的组
('211 98 3911 4008 comp.lang.python.announce', 98, 3911, 4008, 'comp.lang.python.announce')

还有可能得到一个带有类似错误信息的的异常 如果引发了异常 可能是服务器的名字写错了
另外一种可能是在创建服务器对象和调用group方法之间 '超时了'， 服务器允许用户保持连接的时间很短(比如10秒)
如果输入速度不够快 把代码放到脚本里， 或着将服务器对象的创建和方法的调用放在同一行内 (以分号隔开)
'''

'''-----------------------------------------------------------------------------------------------------------'''

# 模块介绍 https://docs.python.org/3/library/nntplib.html
import nntplib

server = nntplib.NNTP('news.gmane.org')
resp, count, frist, last, name = server.group('gmane.comp.python.committers')
print('Group--', name, 'has--', count, 'articles, range--', frist, 'to--', last)
resp, overviews = server.over((last -9, last))
print(resp, '----', overviews)#返回消息头和概述信息

for id , over in overviews:
	print(id, nntplib.decode_header(over['subject']))
	print(server.body(id)[1])#所有文章信息
print('-----------------', resp)#响应信息
server.quit()


"""
当头decode_header()可以包含非ASCII字符时，建议使用该函数：
NNTP.over（message_spec，*，file = None ）
在旧服务器上发送OVER命令或XOVER命令。 message_spec可以是表示消息id的字符串，也可以是表示当前组中的文章范围的（第一，最后）元组元组，或者指示从第一个到最后一个文章开始的文章范围的（第一，无）元组 当前组中的文章，或“无”选择当前组中的当前文章。

返回一对（响应，概述）。 概述是（article_number，概述）元组的列表，一个用于每个由message_spec选择的文章。 每个概述都是一个具有相同数量项目的字典，但这个数字取决于服务器。

nntplib.decode_header（header_str )
解码标头值，解除转义的非ASCII字符。 header_str必须是一个str对象。返回未转义的值。建议使用此功能以人类可读的形式显示一些标题：
"""

'''
三个print输出
Group-- gmane.comp.python.committers has-- 4419 articles, range-- 1 to-- 4419

4410 Re: Proposal for procedures regarding CoC actions

ArticleInfo(number=4410, message_id='<CAP7h-xYfoPjqcCOH+401PNk629t2PiV+V-N9G3HB+h8LVT0Mzg@mail.gmail.com>', lines=[b'--===============8183602179802571856==', b'Content-Type: multipart/alternative; boundary=001a1148839ee2f6c3054c240484', b'', b'--001a1148839ee2f6c3054c240484', b'Content-Type: text/plain; charset=UTF-8', b'', b'On Sat, Apr 1, 2017 at 7:07 PM, Raymond Hettinger <', b'raymond.hettinger@gmail.com> wrote:', b'', b'> I propose that when someone thinks there is a problem serious enough to', b'> warrant a Code-of-Conduct action, that it get referred to a group of three', b'> people to make the decision.', b'', b'', b'This reminds me of <https://en.wikipedia.org/wiki/NKVD_troika>.', b'', ......

'''

'''-----------------------------------------------------------------------------------------------------------'''

# 原文连接 http://www.ynpxrz.com/n1039057c2023.aspx http://www.jb51.net/article/65708.htm

from nntplib import NNTP

server = NNTP('web.aioe.org')
#server = NNTP('news.gmane.org')

(resp, count, frist, last, name) = server.group('comp.lang.python')
#3211 3691 182837 186527 comp.lang.python -- 3691 --82837 --186527-- 3691

(resp,subs) = server.xhdr('subject', (str(frist) + '-' + str(last)))
#print(resp, '----', subs)
# NNTP.xhdr（hdr，str，*，file = None ）xhdr命令 hdr是标题关键字例如主题
# str是文章编号的的起始和终点位置编号 格式'first-last' 返回响应元组 Return a pair (response, list)
#其中list是对（id，text）的列表，其中id是文章编号，文本是该文章所请求的标题的文本
# 221 Header or metadata information for subject follows (from overview) 
#---- [('182841', 'Re: compile error when using override'), ....

##输出后十个文章ID和文章标题
for subject in subs[-10:]:
	print(subject)

number = input('Which article do you want to read?')

(reply, num, id, lists) = server.body(str(number))
#python3 会出现 错误#ValueError: not enough values to unpack (expected 4, got 2)

for line in lists:
	print(line)



'''


('186336', 'Re: ANN:  Wing Python IDE 6.0.3 released')
('186337', 'Re: Announcing SCM Workbench 0.8.5 GUI for Git, Mercurial (hg) and Subversion (svn)')
('186338', 'PyDev 5.6.0 Released')
('186339', 'Re: Recompilation of Python3.6.x')
('186340', 'Re: Recompilation of Python3.6.x')
('186341', 'Re: Recompilation of Python3.6.x')
('186342', 'Re: Manager for project templates, that allows "incremental" feature addition')
('186343', 'Re: Manager for project templates, that allows "incremental" feature addition')
('186344', 'Re: Manager for project templates, that allows "incremental" feature addition')
('186345', 'SNMP')
Which article do you want to read? 186495

'''

