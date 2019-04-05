import requests
import datetime

import asyncio
from aiohttp import ClientSession
from multiprocessing.pool import ThreadPool


def get_sync(urls):
    start = datetime.datetime.now()

    for url in urls:
        response = requests.get(url)
        print(response.text.encode('utf-8'))

    done = datetime.datetime.now()
    print('ssssssssssssssssssssssssssssssssssssss', done - start)


async def fetch(url, session):
    async with session.get(url) as response:
        # delay = response.headers.get('DELAY')
        # date = response.headers.get('DATE')
        # print("{}:{} with delay {}".format(date, response.url, delay))
        return await response.read()


async def run(urls):
    tasks = []

    # fetch all response within one client session
    # keep connection alive for all request
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        print(responses)


async def bound_fetch(url, sem, session):
    async with sem:
        return await fetch(url, session)


async def run_semaphore(urls):
    tasks = []

    sem = asyncio.Semaphore(1000)

    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(bound_fetch(url, sem, session))
            tasks.append(task)

        response = asyncio.gather(*tasks)
        await response
        print(response)


def get_async(urls, func):
    start = datetime.datetime.now()

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(func(urls))
    loop.run_until_complete(future)

    done = datetime.datetime.now()
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaa', done - start)


urls = [
    # "https://bing.com",
    # "https://duckduckgo.com",
    # "https://yahoo.com",
    "http://httpbin.org/get"
] * 10000  # 20 fetches


# get_sync(urls)
# get_async(urls, run)
get_async(urls, run_semaphore)
