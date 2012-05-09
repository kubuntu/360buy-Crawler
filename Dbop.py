#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sqlite3
import os, sys, time

path = os.path.dirname(os.path.realpath(sys.argv[0]))
conn = sqlite3.connect(path + '/360buy.db')
conn.text_factory = str

def db_create(create_sentence):
    c = conn.cursor()
    c.execute(create_sentence)
    conn.commit()
    c.close()

def db_insert(insert_sentence):
    c = conn.cursor()
    tries = 0
    while tries < 5:
        try:
            c.execute(insert_sentence)
            break
        except:
            tries += 1
            time.sleep(5)
    conn.commit()
    c.close()

def db_update(update_sentence):
    tries = 0
    c = conn.cursor()
    while tries < 5:
        try:
            c.execute(update_sentence)
            break
        except:
            tries += 1
            time.sleep(5)
    conn.commit()
    c.close()

def db_list(list_sentence):
    c = conn.cursor()
    c.execute(list_sentence)
    for x in c:
        print x

if __name__ == "__main__":
#    db_create('create table v(product_id integer primary key,title text)')
    db_insert('insert into v(product_id, title) values(1, "ddd")')
    db_list('select * from v')
