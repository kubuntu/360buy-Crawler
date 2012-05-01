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
	if not href:
		return ""
	return href.group(1)

def extract_maxnum_from_htmlline(htmlline):
	buf = ''
	num_list = []
	flag = False
	for i in unicode(htmlline, 'utf8'):
		if i == '>':
			flag = True
		if i == '<':
			flag = False
		if i.isdigit() and flag:
			buf += i
			continue
		if buf != '' and flag:
		 	num_list.append(int(buf))
		 	buf = ''
	return max(num_list)

def split_htmlline2parts(htmlline, split_symbol):
	parts = htmlline.split(split_symbol) 	
	return parts

if __name__ == '__main__':
	num = extract_maxnum_from_htmlline('<span class="prev-disabled">上一页<b></b></span><a href="737-738-806-0-0-0-0-0-0-0-1-1-1.html" class="current">1</a><a href="737-738-806-0-0-0-0-0-0-0-1-1-2.html">2</a><a href="737-738-806-0-0-0-0-0-0-0-1-1-3.html">3</a><span class="text">…</span><a href="737-738-806-0-0-0-0-0-0-0-1-1-17.html">17</a><a href="737-738-806-0-0-0-0-0-0-0-1-1-2.html" class="next">下一页<b></b></a>')
	print num

