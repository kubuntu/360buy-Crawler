#-*-coding=utf8-*-
def extract_text_from_htmlline(htmlline):
	stack = []
	for i in unicode(htmlline, 'utf8'):
		if i != '>':
			stack.append(i)
		elif i == '>':
			while stack.pop() != '<':
				pass
			if len(stack) != 0:
				stack.append("|")
	sstr = ''
	stack.pop()
	stack.pop()
	for i in stack:
		sstr += i
	return sstr

if __name__ == '__main__':
	sstr = extract_text_from_htmlline("<h>图书，</h><p>音像</p>")
	print sstr
