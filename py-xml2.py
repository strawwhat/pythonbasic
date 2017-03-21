#/usr/bin/env python
# *-*coding:utf-8 *-*

#pyhton 基础教程22 简单的页面创建程序脚本
from xml.sax.handler import ContentHandler
from xml.sax  import parse


"""
xml.sax文档
#https://docs.python.org/3/library/xml.sax.html			
"""		
'''

startElement
标签等于page时 设置 passthrough为True 打开一个以标签名字命名的html文件然后写入html头部 标题 
如果标签名不等于page 但在page标签中 写入所有标签名和字符不做任何修改 
当在在page元素中但元素不是page， 使用self.passthrough来判断，
然后重建<尖括号 写入键值 然后闭合
没有标签键值的 写入标签然后 调用characters写入文本 然后调用endElement elif 写入闭合元素

endelement 当name等于page元素时 把passthrough设置为false 写入闭合标签 关闭打开文件
不等于page在page元素中 写入闭合标签
characters 在 passthrough为True时写入文本

'''

"""
xml.sax文档
#https://docs.python.org/3/library/xml.sax.html			
"""		

class PageMake(ContentHandler):
	
	passthrough = False
	
	def startElement(self, name, attrs):
		if name == 'page':
			self.passthrough = True
			self.out = open(attrs['name'] + '.html', 'w')
			self.out.write('<html><head>\n')
			self.out.write('<title>%s</title>\n' % attrs['title'])
			self.out.write('</head><body>\n')
		elif self.passthrough:
			self.out.write('<' + name)
			for key, val in attrs.items():
				self.out.write(' %s="%s"' %(key, val))
			self.out.write('>')
		
	def endElement(self, name):
		if name == 'page':
			self.passthrough = False
			self.out.write('\n</body></html>\n')
			self.out.close()
		elif self.passthrough:
			self.out.write('</%s>' % name)

	def characters(self, chars):
		if self.passthrough: 
			self.out.write(chars)
			
parse('~/py1/website.xml', PageMake())

