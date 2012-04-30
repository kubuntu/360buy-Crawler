import urllib2
import re
from BeautifulSoup import BeautifulSoup
from RequestBase import RequestBase
import re

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

def htmlpage_has_products(url, coding):
	request = urllib2.Request(url)
	try:
		response = urllib2.urlopen(req, timeout=15)
	except urllib2.URLError:
		html = "<a></a>"
		soup = BeautifulSoup(''.join(html), fromEncoding=coding)
		return soup
	html = response.read()
	response.close()
	soup = BeautifulSoup(''.join(html), fromEncoding=coding)
	

def main():
	base_url = "http://www.360buy.com/products/"

if __name__ == '__main__':
    url_arr=['http://www.360buy.com/products/670-677-678-0-0-0-0-0-0-0-1-1-1.html',
             'http://www.360buy.com/products/670-677-678-0-0-0-0-0-0-0-1-1-2.html']
    ul=UrlFactory(url_arr, 'utf8')
    url_array, url_reviews=ul.url_storage()
