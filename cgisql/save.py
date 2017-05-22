#!/usr/bin/python
# *-*coding: utf-8 *-*
 
#save.cgi 保存消息
print("Content-type: text/html\n")n'
 
import cgitb;cgitb.enable()
 
def quote(string):
        if string:
                return string.replace("'","\\'")
        else:
                return string
 
#import MySQLdb
#conn = MySQLdb.connect(user='', passwd='', db='', host='')
import psycopg2
conn = psycopg2.connect(user='', database='', password='', host='127.0.0.1')
curs = conn.cursor()
 
import cgi, sys
form = cgi.FieldStorage()
 
sender = quote(form.getvalue('sender'))
subject = quote(form.getvalue('subject'))
text = quote(form.getvalue('text'))
reply_to = form.getvalue('reply_to')
 
if not (sender and subject and text):
        print 'Please supply sender,subject,text'
        sys.exit()
 
if reply_to is not None:
        query = """
        INSERT INTO messages(reply_to,sender,subject,text)
        VALUES(%d,'%s','%s','%s')""" % (int(reply_to),sender,subject,text)
else:
        query = """
        INSERT INTO messages(sender,subject,text)
        VALUES('%s','%s','%s')""" % (sender,subject,text)
 
curs.execute(query)
conn.commit()
 
print("""
<html>
	<head>
		<title>Messages Saved</title>
	</head>
	<body>
		<h1>The Messages Saved Page</h1>
		<hr />
		<a href='main.py'>Back to the main page</a>
	</body>
</html>
""")


