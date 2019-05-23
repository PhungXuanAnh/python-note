import asyncio
import aiohttp
import aiofiles


async def get_sample():
    # params = {'key1': 'value1', 'key2': 'value2'}
    params = [('key', 'value1'), ('key', 'value2')]

    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get', params=params) as response:
            print(response.status)
            # print(await response.text())
            # print(await response.json())
            print(await response.content.read(10))


async def post_sample():
    payload = {'key1': 'value1', 'key2': 'value2'}
    url = 'http://httpbin.org/post'
    async with aiohttp.ClientSession() as session:
        # async with session.post(url, data=payload) as response:
        # async with session.post(url, data=b'\x00Binary-data\x00') as response:
        async with session.post(url, data='this is text') as response:
            print(await response.text())


async def post_multipart_encode_file():
    url = 'http://httpbin.org/post'
    files = {'file': open('report.md', 'rb')}

    data = aiohttp.FormData()
    data.add_field('file',
                   open('report.md', 'rb'),
                   filename='report.md',
                   content_type='application/md')

    async with aiohttp.ClientSession() as session:
        # async with session.post(url, data=files) as response:
        async with session.post(url, data=data) as response:
            print(await response.text())


async def file_sender(file_name=None):
    async with aiofiles.open(file_name, 'rb') as f:
        chunk = await f.read(64 * 1024)
        while chunk:
            yield chunk
            chunk = await f.read(64 * 1024)


async def post_stream_up():
    url = 'http://httpbin.org/post'

    # async with aiohttp.ClientSession() as session:
    #     with open('report', 'rb') as f:
    #         async with session.post(url, data=f) as response:
    #             print(await response.text())

    async with aiohttp.ClientSession() as session:
        # async with session.post(url, data=files) as response:
        async with session.post(url, data=file_sender('report.md')) as response:
            print(await response.text())


loop = asyncio.get_event_loop()
# loop.run_until_complete(get_sample())
# loop.run_until_complete(post_multipart_encode_file())
loop.run_until_complete(post_stream_up())
