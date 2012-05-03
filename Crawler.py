#-*-coding:utf-8-*-
from UrlFactory import *
from Utils import *
import os

def step1():
    url = "http://www.360buy.com/allSort.aspx"
    a, b = extract_htmlpage_products(url, 'gbk')
    if not a and not b:
        print "conntect error!"
        #fatal error is happend, program must shutdown
        exit()
    else:
        print "step1 is over!"
        return a, b

def step2(products_sub_catalog_href):
    assert products_sub_catalog_href
    #filter book link
    products_sub_catalog_href_filter = []
    filter_url = open("url_filter", "w")
    for product in products_sub_catalog_href:
        if product[1].find("mvd") != -1:
            continue
        ret = is_book_page(product[1], 'gbk')
        if ret == -1:
            continue
        if not ret:
            print product[1]
            products_sub_catalog_href_filter.append(product)
            print >> filter_url, product[0].encode("utf8"), " ", product[1]
    filter_url.close()
    assert len(products_sub_catalog_href_filter)
    print "step2 is over"
    return products_sub_catalog_href_filter

def step3():
    products_name = []
    products_href = []
    if os.path.isfile("./url_filter"):
        url_filter = open("./url_filter", "r")
        while 1:
            line = url_filter.readline()
            if not line:
                break
            tmp = Utils.split_by_space(line)
            products_name.append(tmp[0])
            products_href.append(tmp[1])
        url_filter.close()
    else:
        a, b = step1()
        products_href = step2(b)
    print "step3 is over!"
    return products_name, products_href

def step4(products_name, products_href):
    name_href_hash = {}
    for i in range(len(products_href)):
        maxnum, href_base = extract_products_pagenum(products_href[i], 'gbk')
        if maxnum == -1:
            continue
        hrefs = products_real_url(href_base, maxnum)
        name_href_hash[products_name[i]] = hrefs
    print "step4 is over!"
    return name_href_hash
        
def main():
    products_name, products_href = step3()
    hrefs = step4(products_name, products_href)
    for href in hrefs:
        print href

if __name__ == "__main__":
    main()
