#-*-coding:utf8-*-

import urllib2
import re
from BeautifulSoup import BeautifulSoup
from Utils import *

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

def products_id_maker(url_arr, coding):
	products_id = []
	for url in url_arr:
		soup = __htmlpage_soup(url, coding)
        ids = soup.findAll('li', {'sku':True})
        for i in ids:
        	products_id.append(str(i['sku']))
	return products_id

def get_reviews_page_num(url, coding):
	pagination_soup = __htmlpage_soup(url, coding)
	pagination = pagination_soup.findAll("div", attrs={"class":"Pagination"})
	soup2=BeautifulSoup(str(pagination))
	at = soup2.findAll('a')
	max_num = 0
	for i in at:
		if re.match('[0-9]+', i.text):
			m = int(i.text)
			if m > max_num:
				max_num = m
	return max_num

def url_storage(products_id):
	products_url_reviews = []
	products_url_contents = []
	for i in range(len(products_id)):
		url_for_reviews_num = 'http://club.360buy.com/review/' + products_id[i] + '-1-1-0.html'
		reviews_page_totalnum = get_reviews_page_num(url_for_reviews_num, 'gbk')
		print reviews_page_totalnum
        	temp=[]
        	for index in range(reviews_page_totalnum):
            		sstr='http://club.360buy.com/review/'+products_id[i]+'-1-'+str(index+1)+'-0'+'.html'
            		temp.append(sstr)
        	products_url_reviews.append((products_id[i], temp))
	for i in range(len(products_id)):
		sstr='http://www.360buy.com/product/'+products_id[i]+'.html'
        products_url_contents.append(sstr)
	return products_url_reviews, products_url_contents


#http://www.360buy.com/allSort.aspx
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
	maxnum = extract_maxnum_from_htmlline(str(block))
	return maxnum

if __name__ == '__main__':
	url_arr=["http://www.360buy.com/products/737-738-1052.html"]
	products_id = products_id_maker(url_arr, 'gbk')
	products_url_reviews, products_url_contents = url_storage(products_id)
	for i in products_url_reviews:
		print i


