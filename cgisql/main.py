#!/usr/bin/python
# *-*coding: utf-8 *-*

#main.cgi 电子公告板主页
print('Content-type:text/html\n')

import cgitb; cgitb.enable()

#import MySQLdb
#conn = MySQLdb.connect(user='', passwd='', db='', host='')
import psycopg2
conn = psycopg2.connect(user='', database='', password='', host='127.0.0.1')
curs = conn.cursor()


print("""
<html>
	<head>
		<title>Foobar Bulletin Board</title>
	</head>
	<body>
		<h1>The Foobar Bulletin Boaed Page</h1>
""")

#查找和获取所有数据
curs.execute('SELECT * FROM messages')
rows = curs.fetchall()
toplevel = []
children = {}

#reply_to为空加入到toplevel，否则把当前id和[row]加入到children中
for row in rows:
	parent_id = row[3]
	if parent_id is None:
		toplevel.append(row)
	else:
		children.setdefault(parent_id, []).append(row)

#输出每行的主题并链接到view,try children是否有当前行id的键，如果存在，else中对每个值调用format打印主题
def format(row):
	print('<p><a href="view.py?id=%i">%s</a></p>' % (row[0], row[1]))
	try: kids = children[row[0]]
	except KeyError: pass
	else:
		print("<blockquote>")
		for kid in kids:
			format(kid)
		print("</blockquote>")

print('<p>')
#对每个行调用format函数打印主题链接
for row in toplevel:
	format(row)

print("""
		</p>
		<hr />
		<p><a href='edit.py'>Post Messages</a></p>
	</body>
</html>
""")


