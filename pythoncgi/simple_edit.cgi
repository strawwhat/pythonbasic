#!/usr/bin/python
#-*-coding:UTF-8-*-

#python25 使用cgi进行远程编辑 25-1 简单的网页编辑器


import cgi

form = cgi.FieldStorage()

text = form.getvalue('sometext', open('simple_edit.dat').read())
#当通过Web服务器访问页面时，CGI脚本会检查名为text的输入值，
#如果这个值被提交了，那么文本会被写道simple_edit.dat文件中，这三行也可以放在最后
f = open(filepath, 'w')
f.write(text)
f.close()


#第一行是必需的。告诉浏览器显示的内容类型为text/html，然后输出空行告诉服务器结束头部信息
print("""Content-type: text/html

<html>
	<head>
		<meta charset='utf-8'>
		<title>A Simple Editor</title>
	</head>
	<body>
		<form action='cgi253.cgi' method='POST'>
		<textarea rows='30' cols='60' name='sometext'>%s</textarea><br />
		<input type='submit' />
		</form>
	</body>
</html>
""" % text)



"""
-------------------------------------------------------------------
<meta charset='utf-8'> 输入汉字不乱码
把需要读取和写入的文件权限改为 777全局可操作， 755会报错

输入是通过HTML表单提供给CGI脚本的键值对或称字段。
可以使用cgi模块的FieldStorage类从cgi脚本中获取这些字段
当创建FieldStorage实例时(应该只创建一个)，它会从请求中获取变量(或字段)
然后通过类字典接口将他们提供给程序。
somename = form.getvalue('name', 'unknown')
如果不提供默认值 'unknown'的话，就会将None作为默认值使用

---------------------------------------------------------------
使用cgi的post方法代替get方法(提交大量数据时使用post方法)
使用数据文件作为text的默认值， 将文本保存到数据文件中，打印表单，将文本显示在文本域中textarea 


当通过web服务器访问页面时，cgi脚本会检查名为text的输入值，
默认值是文本当前内容， 在文本域textarea中显示
如果这个值被提交了，那么文本会被写到simple_edit.dat文件中，
最终修改和提交的后的文本也会显示在网页中


"""



