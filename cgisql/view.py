#!/usr/bin/python
# *-*coding: utf-8 *-*

#view.cgi 信息浏览
print('Content-type:text/html\n')
 
import cgitb;cgitb.enable()
 
#import MySQLdb
#conn = MySQLdb.connect(user='', passwd='', db='', host='')
import psycopg2
conn = psycopg2.connect(user='', database='', password='', host='127.0.0.1')
curs = conn.cursor()
 
import cgi, sys
form = cgi.FieldStorage()
id = form.getvalue('id')
 
print("""
<html>
	<head>
		<title>View Message</title>
	</head>
	<body>
		<h1>The View Message Page</h1>
""")


try: id = int(id)
except:
	print("Invalid messages ID")
	sys.exit()

#将所有结果的行作为序列的序列获取，如果没有rows退出
curs.execute("SELECT * FROM messages WHERE id='%i'" % id)
rows = curs.fetchall()

if not rows:
	print("Unknown messages ID")
	sys.exit()

row = rows[0]

print("""
		<p><b>Subject: </b>%s<br />
		<b>Sender: </b>%s<br />
		<pre>%s</pre>
		</p>
		<hr />
		<a href="main.py">Back to the main page</a>
		| <a href="edit.py?reply_to=%s">Reply</a>
	</body>
</html>
""" % (row[1], row[2], row[4], row[0]))


