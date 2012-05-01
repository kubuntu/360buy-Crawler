#-*-coding:utf8-*-

import urllib2
import re
from BeautifulSoup import BeautifulSoup
from RequestBase import RequestBase
import re
from Utils import *

class UrlFactory(RequestBase):
    def __init__(self, url_arr, coding):
        self.url_array=[]
        self.url_reviews=[]
        for url in url_arr:
            RequestBase.__init__(self, url, coding)
            proIDs=self.soup.findAll('li', {'sku':True})
            for i in proIDs:
                self.url_array.append(str(i['sku']))
    def get_reviews_page_num(self, url, coding):
        pagination_soup = RequestBase.__init__(self, url, coding)
        pagination = pagination_soup.findAll('div', 'Pagination')
        soup2=BeautifulSoup(str(pagination))
        at = soup2.findAll('a')
        max_num=0
        for i in at:
            if re.match('[0-9]+', i.text):
                m = int(i.text)
                if m > max_num:
                    max_num = m
        print max_num
        return max_num
    def url_storage(self):
        for i in range(len(self.url_array)):
            url_for_reviews_num = 'http://club.360buy.com/review/'+self.url_array[i]+'-1-1-0.html'
            reviews_num=self.get_reviews_page_num(url_for_reviews_num, 'utf8')
            tmp=[]
            for index in range(reviews_num):
                sstr='http://club.360buy.com/review/'+self.url_array[i]+'-1'+'-'+str(index+1)+'-0'+'.html'
                tmp.append(sstr)
            self.url_reviews.append(tmp)
        for i in range(len(self.url_array)):
            sstr='http://www.360buy.com/product/'+self.url_array[i]+'.html'
            self.url_array[i]=sstr
        return self.url_array, self.url_reviews

def __htmlpage_soup(url, coding):
	request = urllib2.Request(url)
	try:
		response = urllib2.urlopen(request, timeout=15)
	except urllib2.URLError:
		html = "<a></a>"
		soup = BeautifulSoup(''.join(html), fromEncoding=coding)
		return soup
	html = response.read()
	response.close()
	htmlpage_soup = BeautifulSoup(''.join(html), fromEncoding=coding)	
	return htmlpage_soup

def extract_htmlpage_products(url, coding):
	base_url1 = "http://www.360buy.com/"
	base_url2 = "http://www.360buy.com"
	htmlpage_soup = __htmlpage_soup(url, coding)
	blocks = htmlpage_soup.findAll("div", attrs={"class":"mt"})
	blocks_sub = htmlpage_soup.findAll("em")
	products_top_catalog_href = [] #一级目录
	products_sub_catalog_href = [] #二级目录
	for block in blocks:
		catalog = extract_text_from_htmlline(str(block)).strip()
		href = extract_href_from_htmlline(str(block)).strip()
		products_top_catalog_href.append((catalog, href))
	for block_sub in blocks_sub:
		parts = split_htmlline2parts(str(block_sub).strip(), "</em>")
		for part in parts:
			catalog_sub = extract_text_from_htmlline(str(part)).strip()
			if len(catalog_sub) == 0:
				continue
			href_sub = extract_href_from_htmlline(str(part)).strip()
			if href_sub.find("http://") == -1:
				if href_sub[0] == '/':
					href_sub = base_url2 + href_sub
				else:
					href_sub = base_url1 + href_sub
			products_sub_catalog_href.append((catalog_sub, href_sub))
	return products_top_catalog_href, products_sub_catalog_href

def extract_products_pagenum(url, coding):
	htmlpage_soup = __htmlpage_soup(url, coding)
	block = htmlpage_soup.find("div", attrs={"class":"pagin fr"})
	num = extract_maxnum_from_htmlline(str(block))
	print num
	

if __name__ == '__main__':
	url_arr=["http://www.360buy.com/products/737-794-965.html"]
	num = extract_products_pagenum(url_arr[0], 'gbk')
