#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#编辑器脚本

print('Content-type: text/html\n')

from os.path import join, abspath
import cgi, sys

BASE_DIR = abspath('data')#返回绝对路径



form = cgi.FieldStorage()
#把index.html放在apache2/htdocs文件夹中，index.html中文本框被命名为filename，
#这样就保证它的内容会被当作CGI的filename参数提供给edit.cgi脚本，也就是form标签的action特性
filename = form.getvalue('filename')
if not filename:
	print('Please enter a file name')
	sys.exit()

text = open(join(BASE_DIR, filename)).read()

print("""
<html>
	<head>
		<meta charset='utf-8'>
		<title>Editing....</title>
	</head>
	<body>
		<form action='save.cgi' method='POST'>
		<b>File:</b> %s<br />
		<input type='hidden' value='%s' name='filename' />
		<b>Password:</b><br />
		<input name='password' type='password' /><br />
		<b>Text: </b><br />
		<textarea name='text' cols='60' rows='30'>%s</textarea><br />
		<input type='submit' value='Save' />
		</form>
	</body>
</html>
""" % (filename, filename, text))



