#-*-coding:utf-8-*-
from UrlFactory import *
from Utils import *
import os
import threading
from threading import Thread, Lock
from Queue import Queue

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
    print "step4 is over!"
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
def step5_save():
    name_id_hash = {}
    file_ids = open("file_ids", "r")
    for line in file_ids:
        part = []
        split_by_multi_space(line.strip(), part)
        product_name = part[0]
        part = part[1:]
        name_id_hash[product_name] = part
    file_ids.close()
    print "step5 is over!"
    return name_id_hash

def step5(name_href_hash):
    if os.path.isfile("file_ids"):
        return step5_save()
    name_id_hash = {}
    file_ids = open("file_ids", "w")
    for item in name_href_hash.items():
        ids = []
        print >> file_ids, item[0]," ",
        for href in item[1]:
            try:
                products_id = products_id_maker(href, 'gbk')
                print products_id
                if products_id == -1:
                    continue
                for i in products_id:
                    print >> file_ids, i, " ",
            except UnicodeEncodeError:
                continue
            ids.append(products_id)
        print >> file_ids, "\n", 
        name_id_hash[item[0]] = ids
    file_ids.close()
    return name_id_hash
            
#生成评论页面链接和产品参数页面链接
def step6(name_id_hash):
    file_ids_filter = open("file_ids_filter", "w")
    name_reviews_contents_hash = {}
    for item in name_id_hash.items():
        products_url_reviews, products_url_contents = url_storage(item[1])
        print >> file_ids_filter, item[0], " ",
        for id in products_url_reviews:
            print >> file_ids_filter, id[0], ":", len(id[1]), " ", 
        print >> file_ids_filter, "\n"
        name_reviews_contents_hash[item[0]] = [products_url_reviews, products_url_contents]
        file_ids_filter.flush()
    file_ids_filter.close()
    return name_reviews_contents_hash

q = Queue()
file_mutex = Lock()
name_reviews_contents_hash = {}

def step6_mutil_thread():
    while True:
        item = q.get()
        print item[0]
        products_url_reviews, products_url_contents = url_storage(item[1])
        file_mutex.acquire()
        file_ids_filter = open("file_ids_filter", "a")
        print >> file_ids_filter, item[0], " ",
        for id in products_url_reviews:
            print >> file_ids_filter, id[0], ":", len(id[1]), " ",
        print >> file_ids_filter, "\n"
        name_reviews_contents_hash[item[0]] = [products_url_reviews, products_url_contents]
        file_ids_filter.flush()
        file_ids_filter.close()
        file_mutex.release()
        q.task_done()
        
def main():
    products_name, products_href = step3()
    name_href_hash = step4(products_name, products_href)
    name_id_hash = step5(name_href_hash)
    num_threads = 5 #线程数量
    for i in range(num_threads):
        t = Thread(target = step6_mutil_thread)
        t.daemon = True
        t.start()
        print "threading", i, "is start"
    for item in name_id_hash.items():
        q.put(item)
    q.join()
    #name_reviews_contents_hash = step6(name_id_hash)

if __name__ == "__main__":
    main()
