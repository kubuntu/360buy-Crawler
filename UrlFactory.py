#-*-coding:utf-8-*-

from BeautifulSoup import BeautifulSoup
import Utils

#从页面中获取商品的id号
def products_id_maker(url, coding): 
	if not url:
		return -1
	products_id = []
	soup = Utils.__htmlpage_soup(url, coding)
	if soup == -1:
		return -1
	ids = soup.findAll('li', {'sku':True})
	for i in ids:
		products_id.append(str(i['sku']))
	return products_id

#获取评论页面数
def get_reviews_page_num(url, coding):
	pagination_soup = Utils.__htmlpage_soup(url, coding)
	if not pagination_soup:
		return
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

#生成评论页面链接，和产品参数页面链接
def url_storage(products_id):
	products_url_reviews = []
	products_url_contents = []
	for i in range(len(products_id)):
		url_for_reviews_num = 'http://club.360buy.com/review/' + products_id[i] + '-1-1-0.html'
		reviews_page_totalnum = get_reviews_page_num(url_for_reviews_num, 'gbk')
		if not reviews_page_totalnum:
			continue
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
#生成所有商品的一级目录链接和二级目录链接, 并导入文本文件
def extract_htmlpage_products(url, coding):
	url_file = open("url", "w")
	base_url1 = "http://www.360buy.com/"
	base_url2 = "http://www.360buy.com"
	htmlpage_soup = Utils.__htmlpage_soup(url, coding)
	blocks = htmlpage_soup.findAll("div", attrs={"class":"mt"})
	if not blocks:
		return (None, None)
	blocks_sub = htmlpage_soup.findAll("em")
	products_top_catalog_href = [] #一级目录
	products_sub_catalog_href = [] #二级目录
	for block in blocks:
		catalog = Utils.extract_text_from_htmlline(str(block)).strip()
		href = Utils.extract_href_from_htmlline(str(block)).strip()
		products_top_catalog_href.append((catalog, href))
	for block_sub in blocks_sub:
		parts = Utils.split_htmlline2parts(str(block_sub).strip(), "</em>")
		for part in parts:
			catalog_sub = Utils.extract_text_from_htmlline(str(part)).strip()
			if len(catalog_sub) == 0:
				continue
			href_sub = Utils.extract_href_from_htmlline(str(part)).strip()
			if href_sub.find("http://") == -1:
				if href_sub[0] == '/':
					href_sub = base_url2 + href_sub
				else:
					href_sub = base_url1 + href_sub
			products_sub_catalog_href.append((catalog_sub, href_sub))
	for item in products_sub_catalog_href:
		print >> url_file, item[0].encode("utf8"), " ", item[1].encode("utf8")
	url_file.close()
	return products_top_catalog_href, products_sub_catalog_href

#生成产品的最大页面数
def extract_products_pagenum(url, coding):
	htmlpage_soup = Utils.__htmlpage_soup(url, coding)
	if htmlpage_soup == -1:
		return -1, -1
	block = htmlpage_soup.find("div", attrs={"class":"pagin fr"})
	if not block:
		return -1, -1
	maxnum = Utils.extract_maxnum_from_htmlline(str(block))
	href_base = Utils.extract_mutil_href_from_htmlline(str(block))
	return maxnum, href_base

#生成产品的真实链接
def products_real_url(htmls, maxnum):
	base_url = "http://www.360buy.com/products/"
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
			hrefs[j] = hrefs[j][0:-1]
		hrefs[j] += leave
		hrefs[j] = base_url + hrefs[j]
	return hrefs

if __name__ == '__main__':
	url = "http://www.360buy.com/allSort.aspx"
	products_top_catalog_href, products_sub_catalog_href = extract_htmlpage_products(url, 'gbk')
	if not products_top_catalog_href and not products_sub_catalog_href:
		print "链接错误..."
	else:
		for i in products_sub_catalog_href:
			print i
