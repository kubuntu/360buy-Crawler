import urllib2
import re
from BeautifulSoup import BeautifulSoup
from RequestBase import RequestBase
import re
from utils import *

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

def extract_htmlpage_products(url, coding):
	request = urllib2.Request(url)
	try:
		response = urllib2.urlopen(request, timeout=15)
	except urllib2.URLError:
		html = "<a></a>"
		soup = BeautifulSoup(''.join(html), fromEncoding=coding)
		return soup
	html = response.read()
	response.close()
	block_soup = BeautifulSoup(''.join(html), fromEncoding=coding)
	block = block_soup.findAll(attrs={'id':re.compile("^tab-sort")})
	title_soup = BeautifulSoup(''.join(str(block)), fromEncoding=coding)
	title = title_soup.findAll("li")
	products_catalog = []
	for s in title:
		sstr = extract_text_from_htmlline(str(s))
		sstr = sstr.strip()
		products_catalog.append(sstr)
	return products_catalog

if __name__ == '__main__':
	url_arr=["http://www.360buy.com/allSort.aspx"]
	products_catalog = extract_htmlpage_products(url_arr[0], 'gbk')
	for p in products_catalog:
		print p

