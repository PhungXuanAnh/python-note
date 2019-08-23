import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

is_banned = ''


def crawler_facebook():
    process = CrawlerProcess(get_project_settings())
    process.crawl('face3')
    process.start()  # the script will block here until the crawling is finished

with open('/home/xuananh/Downloads/is_banned.txt', 'w+') as f:
        pass
        
while not is_banned:
    worker = multiprocessing.Process(target=crawler_facebook)
    worker.start()
    worker.join()
    with open('/home/xuananh/Downloads/is_banned.txt', 'r') as f:
        is_banned = f.read()
