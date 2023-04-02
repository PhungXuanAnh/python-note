#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import time
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

import requests


def get(url):
    return requests.get(url)


def async_get(*urls):

    number_thread = min(len(urls), cpu_count() * 2 - 1)

    pool = ThreadPool(number_thread)
    results = pool.map_async(get, urls)
    results.wait()  # blocking
    return results.get()


def sync_get(*urls):
    res = []
    for url in urls:
        res.append(get(url))
    return res


def main(argv):
    print("fetching {}hronously".format(argv))

    # urls to fetch
    urls = [
        "https://google.com",
        "https://bing.com",
        "https://duckduckgo.com",
        "https://yahoo.com",
    ] * 5  # 20 fetches

    # choose the getter func
    getter = (
        async_get if argv == "async" else sync_get
    )
    # get & time
    start = time.time()
    res = getter(*urls)
    end = time.time()
    # print the results
    for r in res:
        if r.ok:
            print(".", sep="", end="")
        else:
            print(",", sep="", end="")
    print(" took: {:.2f}s".format(end - start))
    # print("results: ", res)


if __name__ == "__main__":
    """
    usage:
        python threadpool.py [sync|async]
    """
    # from sys import argv
    # if len(argv[1:]):
    #     if argv[1] in ("async", "sync"):
    #         main(argv[1])
    #     else:
    #         main("sync")
    # else:
    #     main("sync")
        
    main("async")
    main("sync")
