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

def products_real_url(htmls, maxnum):
	if len(htmls) == 1:
		return
	numbers1 = htmls[0][0:-5].split("-")
	numbers2 = htmls[1][0:-5].split("-")
	size = len(numbers1)
	diff_pos = -1
	base = ""
	hrefs = []
	for i in range(size):
		if numbers1[i] != numbers2[i]:
			diff_pos = i
			break
	
	for i in range(size):
		if i == diff_pos:
			for j in range(1, maxnum+1):
				tmp = base + str(j) + '-'
				hrefs.append(tmp)
		else:
			base += numbers1[i]
			base += '-'
	leave = ""
	for i in range(diff_pos+1, size):
		leave += numbers1[i]
		leave += '-'
	if leave and leave[-1] == '-':
		leave = leave[0:-1]
	leave += ".html"
	for j in range(maxnum):
		if leave == '.html':
			hrefs[j] += leave
		hrefs[j] += leave
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
	href = extract_href_from_htmlline('<span class="prev-disabled">上一页<b></b></span><a href="737-738-806-0-0-0-0-0-0-0-1-1-1.html" class="current">1</a><a href="737-738-806-0-0-0-0-0-0-0-1-1-2.html">2</a><a href="737-738-806-0-0-0-0-0-0-0-1-1-3.html">3</a><span class="text">…</span><a href="737-738-806-0-0-0-0-0-0-0-1-1-17.html">17</a><a href="737-738-806-0-0-0-0-0-0-0-1-1-2.html" class="next">下一页<b></b></a>')
	print href

