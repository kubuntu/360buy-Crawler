#-*-coding=utf8-*-
import urllib2
from BeautifulSoup import BeautifulSoup

#将页面转换为BeautifulSoup的形式
def __htmlpage_soup(url, coding):
	request = urllib2.Request(url)
	try:
		response = urllib2.urlopen(request, timeout=15)
	except urllib2.URLError:
		return
	html = response.read()
	response.close()
	htmlpage_soup = BeautifulSoup(''.join(html), fromEncoding=coding)
	return htmlpage_soup

def is_book_page(url, coding):
	soup = __htmlpage_soup(url, coding)
	if not soup:
		return
	title = soup.find("title").text
	if title.encode("utf8").find("京东图书") != -1:
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
	return max(num_list)


def split_htmlline2parts(htmlline, split_symbol):
	parts = htmlline.split(split_symbol) 	
	return parts

if __name__ == '__main__':
	ret = is_book_page("http://www.360buy.com/products/1713-3293-000.html", "gbk")
	print ret
