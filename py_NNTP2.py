#/usr/bin/env python
#*-*coding:utf-8 *-*

#python 基础 23章NNTP 23-1 简单的新闻收集道理程序
#python2.7 运行

from nntplib import NNTP
from time import strftime, time, localtime

day = 24 * 60 * 60 # 一天的秒数
yesterday = localtime(time() - day)
date = strftime('%y%m%d', yesterday)
hour = strftime('%H%M%S', yesterday)

servername = 'web.aioe.org'
group = 'comp.lang.python'#.announce'
server = NNTP(servername)

ids = server.newnews(group, date, hour)[1]

for id in ids:
	head = server.head(id)[3]
	for line in head:
		if line.lower().startswith('subject'):
			subject = line[9::]
			break

	body = server.body(id)[3]

	print(subject)
	print('-'*len(subject))
	print('\n'.join(body))


server.quit()

"""
480管理员禁用NEWNEWS命令 使用另一种方法

from nntplib import NNTP

servername = 'web.aioe.org'
group = 'comp.lang.python'

server = NNTP(servername)


(resp, count, first, last, name) = server.group(group)
#print((resp,'---', count, '---', first, '----',last,'----', name))
#返回响应 ，文章计数， 第一个和最后一个文章编号， 组名
#('211 3681 182872 186552 comp.lang.python',-, 3681, -, 182872, -, 186552, -, 'comp.lang.python')

for i in range(last-10,last):
	article = server.body(i)[1]
	#print(server.head(i))# 头信息
	print(article.number)#文章编号

	for s in article.lines:
		print(str(s).strip(' b > >> = '))#文章信息

	#print(len(server.body(i)[1])) 3
	#print(server.head(i), '\n')
	


'''
body--- ('222 186542 <mailman.111.1490722977.2634.python-list@python.org> body', ArticleInfo(number=186542, message_id='<mailman.111.1490722977.2634.python-list@python.org>', lines=[b'I am wanting to run a CherryPy app as a daemon on CentOS 6 using an =', b'init.d script. By subscribing to the "Daemonizer" and PIDFile cherrypy =', b'plugins, I have been able to write an init.d script that starts and =', b"stops my CherryPy application. There's only one problem: it would appear =", b'that the program daemonizes, thus allowing the init.d script to return a =', b'good start, as soon as I call cherrypy.engine.start(), but *before* the =', b'cherrypy app has actually started. Particularly, this occurs before =', b'cherrypy has bound to the desired port. The end result is that running =', b'"service <myapp> start" returns OK, indicating that the app is now =', b'running, even when it cannot bind to the port, thus preventing it from =', b'actually starting. This is turn causes issues with my clustering =', b'software which thinks it started just fine, when in fact it never =', b'*really* started.', b'', b'As such, is there a way to delay the demonization until I call =', b'cherrypy.engine.block()? Or some other way to prevent the init.d script =', b'from indicating a successful start until the process has actually bound =', b'to the needed port and fully started? What is the proper way of doing =', b'this?=20', b'', b'Thanks!=20', b'-----------------------------------------------', b'Israel Brewster', b'Systems Analyst II', b'Ravn Alaska', b'5245 Airport Industrial Rd', b'Fairbanks, AK 99709', b'(907) 450-7293', b'-----------------------------------------------', b'', b'', b'', b'']))

head--- ('221 186542 <mailman.111.1490722977.2634.python-list@python.org> head',
 ArticleInfo(number=186542, message_id='<mailman.111.1490722977.2634.python-list@python.org>', lines=[b'Path: aioe.org!news.stack.nl!newsfeed.xs3.de!io.xs3.de!nntp-feed.chiark.greenend.org.uk!ewrotcd!fu-berlin.de!uni-berlin.de!not-for-mail', b'From: Israel Brewster <israel@ravnalaska.net>', b'Newsgroups: comp.lang.python', b'Subject: Proper way to run CherryPy app as a daemon?', b'Date: Tue, 28 Mar 2017 09:25:33 -0800', b'Lines: 33', b'Message-ID: <mailman.111.1490722977.2634.python-list@python.org>', b'References: <D551A466-E69E-4416-B326-6DE10E237F5D@ravnalaska.net>', b'Mime-Version: 1.0 (Mac OS X Mail 10.2 \\(3259\\))', b'Content-Type: text/plain;', b'\tcharset=us-ascii', b'Content-Transfer-Encoding: quoted-printable', b'X-Trace: news.uni-berlin.de /4YHk7uoEEnabMHJBirLmADg1pN/Rp9NUVppW5jkToTg==', b'Return-Path: <israel@ravnalaska.net>', b'X-Original-To: python-list@python.org', b'Delivered-To: python-list@mail.python.org', b'X-Spam-Status: OK 0.023', b"X-Spam-Evidence: '*H*': 0.95; '*S*': 0.00; 'indicating': 0.05;", b" 'space;': 0.07; 'stops': 0.07; 'word-wrap:': 0.07; 'cherrypy':", b" 0.09; 'port,': 0.09; 'started?': 0.09; 'helvetica;': 0.13;", b" '*before*': 0.16; 'bind': 0.16; 'clustering': 0.16; 'subject:run':", b" 0.16; 'subscribing': 0.16; 'such,': 0.16; 'x-mailer:apple mail", b" (2.3259)': 0.16; 'script.': 0.18; 'app': 0.18; 'break-word;':", b" 0.22; 'delay': 0.22; 'fine,': 0.22; 'flying': 0.22; 'occurs':", b" 0.22; 'problem:': 0.22; 'tech': 0.23; 'appear': 0.26; 'script':", b" 0.26; 'prevent': 0.27; 'start,': 0.27; 'airport': 0.29; 'port.':", b" 0.29; 'skip:c 60': 0.29; 'skip:e 60': 0.29; 'thinks': 0.29;", b" 'thus': 0.29; 'skip:- 40': 0.30; 'starts': 0.31; 'thanks!': 0.31;", b" 'running': 0.32; 'this?': 0.32; 'desired': 0.34; 'but': 0.34;", b' \'run\': 0.35; \'end\': 0.35; \'12px;\': 0.35; "there\'s": 0.36;', b" 'subject:?': 0.36; 'there': 0.36; 'skip:& 10': 0.36; 'to:addr", b" :python-list': 0.36; '0);': 0.38; 'skip:- 10': 0.38; 'charset:us-", b" ascii': 0.38; 'needed': 0.38; 'received:10': 0.38; 'some': 0.38;", b" 'turn': 0.39; 'to:addr:python.org': 0.39; 'received:io': 0.39;", b" 'received:psf.io': 0.39; 'actually': 0.40; 'received:ams1.psf.io':", b" 0.40; 'received:mail1.ams1.psf.io': 0.40; 'received:net': 0.60;", b" 'skip:n 20': 0.60; 'application.': 0.61; 'skip:t 30': 0.61;", b" 'call': 0.61; 'line-height:': 0.61; 'header:Message-Id:1': 0.61;", b" 'soon': 0.63; 'received:10.9': 0.66; 'started.': 0.66;", b" 'subject:way': 0.72; '*really*': 0.84; 'skip:4 60': 0.84;", b' \'to:name:python\': 0.84; \'0px;">\': 0.91; \'alaska\': 0.91;', b" 'preventing': 0.91", b'X-ASG-Debug-ID: 1490721934-0a64a2118f2f67f0001-tYLEC7', b'X-Barracuda-Envelope-From: israel@ravnalaska.net', b'X-Barracuda-Apparent-Source-IP: 52.124.20.45', b'X-ASG-Orig-Subj: Proper way to run CherryPy app as a daemon?', b'X-Mailer: Apple Mail (2.3259)', b'X-Barracuda-Connect: mailserver-a.ravnalaska.net[52.124.20.45]', b'X-Barracuda-Start-Time: 1490721934', b'X-Barracuda-URL: http://filter-fai1.ravnalaska.net:8000/cgi-mod/mark.cgi', b'X-Virus-Scanned: by bsmtpd at ravnalaska.net', b'X-Barracuda-BRTS-Status: 1', b'X-Barracuda-Spam-Score: 0.00', b'X-Barracuda-Spam-Status: No, SCORE=0.00 using global scores of TAG_LEVEL=1000.0', b' QUARANTINE_LEVEL=1000.0 KILL_LEVEL=5.0 tests=HTML_MESSAGE', b'X-Barracuda-Spam-Report: Code version 3.2, rules version 3.2.3.37596', b' Rule breakdown below', b' pts rule name              description', b' ---- ---------------------- --------------------------------------------------', b' 0.00 HTML_MESSAGE           BODY: HTML included in message', b'X-Content-Filtered-By: Mailman/MimeDel 2.1.23', b'X-BeenThere: python-list@python.org', b'X-Mailman-Version: 2.1.23', b'Precedence: list', b'List-Id: General discussion list for the Python programming language', b' <python-list.python.org>', b'List-Unsubscribe: <https://mail.python.org/mailman/options/python-list>,', b' <mailto:python-list-request@python.org?subject=unsubscribe>', b'List-Archive: <http://mail.python.org/pipermail/python-list/>', b'List-Post: <mailto:python-list@python.org>', b'List-Help: <mailto:python-list-request@python.org?subject=help>', b'List-Subscribe: <https://mail.python.org/mailman/listinfo/python-list>,', b' <mailto:python-list-request@python.org?subject=subscribe>', b'X-Mailman-Original-Message-ID: <D551A466-E69E-4416-B326-6DE10E237F5D@ravnalaska.net>', b'Xref: aioe.org comp.lang.python:186542']))
('221 186543

186542
'I am wanting to run a CherryPy app as a daemon on CentOS 6 using an ='
'init.d script. By subscribing to the "Daemonizer" and PIDFile cherrypy ='
'plugins, I have been able to write an init.d script that starts and ='
"stops my CherryPy application. There's only one problem: it would appear ="
'that the program daemonizes, thus allowing the init.d script to return a ='
'good start, as soon as I call cherrypy.engine.start(), but *before* the ='
'cherrypy app has actually started. Particularly, this occurs before ='
'''
"""


