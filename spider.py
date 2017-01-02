#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-1-1 下午5:46
# @Author  : rhys
# @File    : spider.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing.dummy import Pool as ThreadPool

import multiprocessing
from time import time
import os
import json

url = "http://acm.hdu.edu.cn/userstatus.php"
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36'
headers = {'User-Agent': user_agent}

member_file = "members.csv"


def complete_info(user_id):
    print 'started...'
    d = {"user": user_id[1]}

    r = requests.get(url, params=d, headers=headers)
    content = r.content

    bs = BeautifulSoup(content, 'html.parser')

    t = bs.find('td', text='Rank')
    if t is None:
        print r.url, r.status_code
        return {"error": "No such user"}

    rank = t.find_next_sibling().text
    problems_submitted = bs.find(
        'td', text='Problems Submitted').find_next_sibling().text
    problems_solved = bs.find(
        'td', text='Problems Solved').find_next_sibling().text
    submissions = bs.find('td', text='Submissions').find_next_sibling().text
    accepted = bs.find('td', text='Accepted').find_next_sibling().text

    print 'end...'
    d = {
        "user_name": user_id[0],
        "user_id": user_id[1],
        "rank": rank,
        "problems_submitted": problems_submitted,
        "problems_solved": problems_solved,
        "submissions": submissions,
        "accepted": accepted
    }
    return d


def load_members_list():
    print os.path.abspath('.')
    ret = {}
    with open("members.csv", "rb") as f:
        members = csv.reader(f)
        for member in members:
            ret[member[0].strip()] = member[1].strip()
            # print member[0].strip(), member[1].strip()
    return ret


def thread_pool_run():
    t_start = time()
    pool = ThreadPool(4)
    results = pool.map(complete_info, m)
    t_end = time()
    print 'elapsed %s' % (t_end - t_start)
    return results


def processing_pool_run():
    t_start = time()
    pool = multiprocessing.Pool(processes=4)
    for i in m:
        res.append(pool.apply_async(complete_info, (i,)))
    pool.close()
    pool.join()

    t_end = time()
    print 'elapsed %s' % (t_end - t_start)


m = []
for k, v in load_members_list().items():
    m.append((k, v))

if __name__ == '__main__':

    res = thread_pool_run()
    res = sorted(res, key=lambda e: int(e['problems_solved']))
    print res

    with open("data.json", "w") as f:
        json.dump(res, f)
