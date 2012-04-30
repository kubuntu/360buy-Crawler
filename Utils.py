#-*-coding=utf8-*-
import re

def extract_text_from_htmlline(htmlline):
	stack = []
	for i in unicode(htmlline, 'utf8'):
		if i != '>':
			stack.append(i)
		elif i == '>':
			while stack.pop() != '<':
				pass
	sstr = ''
	for i in stack:
		sstr += i
	return sstr

def extract_href_from_htmlline(htmlline):
	href = re.search('href="(.*)"', htmlline)	
	return href.group(1)

if __name__ == '__main__':
	sstr = extract_href_from_htmlline('<a href="http://www.163.com">djfjl</a>')
	print sstr
