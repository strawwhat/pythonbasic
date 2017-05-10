#!/usr/bin/env python
# *-*coding:utf-8 *-*


#实现保存功能的脚本


print('Content-type: text/html\n')

from os.path import join, abspath
import cgi, sha, sys


BASE_DIR = abspath('data')
form = cgi.FieldStorage()

text = form.getvalue('text')
filename = form.getvalue('filename')
password = form.getvalue('password')


if not (file and text and password):
	print('Invaild password')
	sys.exit()

#sha.sha('cgi').hexdigest() >>> '27b4d0f8ee1e61a07904f1afd558aa878973f2d1'
if sha.sha(password).hexdigest() != '27b4d0f8ee1e61a07904f1afd558aa878973f2d1':
	print('Invalid password')
	sys.exit()

f= open(join(BASE_DIR, filename), 'w')
f.write(text)
f.close()

print('The file has been saved')


