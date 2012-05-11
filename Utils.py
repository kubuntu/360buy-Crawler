#-*- coding:utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup
import socket
from threading import Timer

#将页面转换为BeautifulSoup的形式
class TimerOut:
	pass

def str2int(sstr):
	j = 0
	for i in sstr:
		if i.isdigit():
			break
		j += 1
	if j == len(sstr):
		return 0
	return int(sstr[j:])

def __throw_timeout_error():
	print "Timeout!"
	raise TimeOut()

def __htmlpage_soup(url, coding):
	request = urllib2.Request(url)
	try:
		t = Timer(30.0, __throw_timeout_error)
		response = urllib2.urlopen(request)
		html = response.read()
		t.cancel()
	except:
		print "connect error!"
		t.cancel()
		return -1
	response.close()
	htmlpage_soup = BeautifulSoup(''.join(html), fromEncoding=coding)
	return htmlpage_soup

def split_by_space(sstr):
	two_part = []
	j = 0
	for i in sstr:
		if i == " ":
			two_part.append(sstr[0:j].strip())
			two_part.append(sstr[j+1:].strip())
		j += 1
	return two_part

def split_by_multi_space(sstr, part):
	j = 0
	i = 0
	while i < len(sstr):
		if sstr[i] == ' ':
			part.append(sstr[j:i])
			j = i
			while j < len(sstr) and sstr[j] == ' ':
				j += 1
			i = j
		i += 1
	part.append(sstr[j:i])

def is_book_page(url, coding):
	try:
		soup = __htmlpage_soup(url, coding)
	except UnicodeEncodeError:
		print "UnicodeEncodeError!"
		return -1
	if soup == -1:
		return -1
	find_result = soup.find("title")
	if not find_result:
		return -1
	else:
		find_result = find_result.text
	if find_result.encode("utf8").find("京东图书") != -1:
		return True
	else:
		return False

#从htmlline中提取文字
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

#从htmlline中提取第一个链接
def extract_href_from_htmlline(htmlline):
	return extract_mutil_href_from_htmlline(htmlline)[0]

#从htmlline中提取多个链接
def extract_mutil_href_from_htmlline(htmlline):
	hrefs = []
	length = len(htmlline)
	for i in range(length - 5):
		if htmlline[i:i+6] == 'href="':
			for j in range(i+6, length-5):
				if htmlline[j] == '"':
					hrefs.append(htmlline[i+6:j])
					i = j - 1
					break
	return hrefs

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
	if len(num_list) == 0:
		return -1
	return max(num_list)


def split_htmlline2parts(htmlline, split_symbol):
	parts = htmlline.split(split_symbol) 	
	return parts

if __name__ == '__main__':
	ret = is_book_page("http://www.360buy.com/products/1713-3293-000.html", "gbk")
	print ret
