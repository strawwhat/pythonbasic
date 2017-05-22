#!/usr/bin/python
# *-*coding: utf-8 *-*

#26-7 edit 消息编辑
print('Content-type:text/html\n')
 
import cgitb;cgitb.enable()
 
#import MySQLdb
#conn = MySQLdb.connect(user='', passwd='', db='', host='')
import psycopg2
conn = psycopg2.connect(user='', database='', password='', host='127.0.0.1')
curs = conn.cursor()
 
import cgi,sys
form = cgi.FieldStorage()
reply_to = form.getvalue('reply_to')
 
print("""
<html>
	<head>
		<title>Compose Messages</title>
	</head>
	<body>
		<h1>The Compose Messges Page</h1>
	
		<form action='save.py' method='POST'>
""")

#如果reply_to不是None，把它保存在表单的一个隐藏输入中 type='hidden'
#subject = curs.fetchone()[0] 将一个结果作为元组获取
subject = ''
if reply_to is not None:
	print('<input type="hidden" name="reply_to" value="%s">' % reply_to)
	curs.execute("SELECT subject FROM messages WHERE id=%s" % reply_to)
	subject = curs.fetchone()[0]
	if not subject.startswith('Re: '):
		subject = 'Re: ' + subject
		
print("""
		<b>Subject:</b><br />
		<input type='text' size='40' name='subject' value='%s'><br />
		<b>Sender:</b><br />
		<input type='text' size='40' name='sender' /><br />
		<b>Messages:</b><br />
		<textarea name='text' cols='40' rows='20'></textarea><br />
		<input type='submit' name='Save' />
		</form>
		<hr />
		<a href='main.py'>Back to the main page</a>
	</body>
</html>
""" % subject)

