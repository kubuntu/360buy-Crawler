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

def step4_save():
    file_real_url = open("url_real", "r")
    name_href_hash = {}
    for line in file_real_url:
        part = []
        split_by_multi_space(line, part)
        hrefs = products_real_url([part[3], part[2]], int(part[1]))
        name_href_hash[part[0]] = hrefs
    file_real_url.close()
    return name_href_hash

def step4(products_name, products_href):
    if os.path.isfile("./url_real"):
        return step4_save()
    name_href_hash = {}
    file_real_url = open("url_real", "w")
    for i in range(len(products_href)):
        try:
            maxnum, href_base = extract_products_pagenum(products_href[i], 'gbk')
        except UnicodeEncodeError:
            continue
        if maxnum == -1:
            continue
        print >> file_real_url, products_name[i], " ", maxnum, " ", href_base[0], " ", href_base[1]
        hrefs = products_real_url(href_base, maxnum)
        name_href_hash[products_name[i]] = hrefs
        #test
        for j in hrefs:
            print j
    print "step4 is over!"
    return name_href_hash

#获取商品的id号
def step5(name_href_hash):
    name_id_hash = {}
    for item in name_href_hash.items():
        ids = []
        for href in item[1]:
            try:
                products_id = products_id_maker(href, 'gbk')
                print products_id
                if products_id == -1:
                    continue
            except UnicodeEncodeError:
                continue
            ids.append(products_id)
        name_id_hash[item[0]] = ids
    return name_id_hash
            
#生成评论页面链接和产品参数页面链接
def step6(name_id_hash):
    name_reviews_contents_hash = {}
    for item in name_id_hash.items():
        products_url_reviews, products_url_contents = url_storage(item[1])
        name_reviews_contents_hash[item[0]] = [products_url_reviews, products_url_contents]
    return name_reviews_contents_hash
        
def main():
    products_name, products_href = step3()
    name_href_hash = step4(products_name, products_href)
    name_id_hash = step5(name_href_hash)

if __name__ == "__main__":
    main()
