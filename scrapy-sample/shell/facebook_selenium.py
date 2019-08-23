
import scrapy

from scrapy.selector import Selector
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from w3lib.html import remove_tags

import json
import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def get_clear_browsing_button(driver):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


def clear_cache(driver, timeout=60):
    """Clear the cookies and cache for the ChromeDriver instance."""
    # navigate to the settings page
    driver.get('chrome://settings/clearBrowserData')

    # wait for the button to appear
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)

    # click the button to clear the cache
    get_clear_browsing_button(driver).click()

    # wait for the button to be gone before returning
    wait.until_not(get_clear_browsing_button)


# with open('/home/xuananh/Dropbox/Work/Other/facebook-account.json', "r") as in_file:
#     accounts = json.load(in_file)
#     email = accounts[0]["email"]
#     password = accounts[0]["password"]


def wait_for_element_display(driver, by, by_value, wait_in_second):
    for _ in range(0, wait_in_second - 1):
        try:
            if driver.find_element(by, by_value):
                return True
        except NoSuchElementException:
            print('waiting element for display...')
        time.sleep(1)
    return False


chrome_option = ChromeOptions()
chrome_option.add_argument("--disable-notifications")
chrome_option.add_argument('--disable-application-cache')
driver = Chrome(executable_path='/home/xuananh/Downloads/chromedriver_linux64/chromedriver',
                chrome_options=chrome_option)

# driver.get("https://facebook.com")

driver.maximize_window()
# driver.set_network_conditions(
#     offline=False,
#     latency=5,
#     download_throughput=100 * 1024,
#     upload_throughput=100 * 1024)

# driver.find_element_by_id('email').send_keys(email)
# driver.find_element_by_id('pass').send_keys(password)
# driver.find_element_by_id('loginbutton').click()

# if not wait_for_element_display(driver, By.ID, "userNavigationLabel", 10):
#     raise('Cannot load page')

# url = "https://www.facebook.com/mytam.info"
url = "https://www.facebook.com/videogiaitri"
url = "https://facebook.com/officialdoda/"
driver.get(url)

for _ in range(0, 10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

response = Selector(text=driver.page_source.encode('utf-8'))
response.xpath('//div[contains(@class, "userContentWrapper")]/.//span/span/a/abbr/@data-utime').extract()

posts = response.xpath('//div[contains(@class, "userContentWrapper")]')
print('================================')
print(len(posts))

for post in posts:
    print('-----------------------------------------')
    post.xpath(".//div[contains(@class,'UFILastCommentComponent')]/div/div/a/text()").extract()
    post.xpath(".//div[contains(@class,'UFILastCommentComponent')]/div/div/a/text()").re_first(r'[Xem thêm|Xem tất cả|View|View all] ([.0-9]+) [bình luận khác|bình luận|more comments|comments]')
    
    print('post_id: ', post.xpath('.//span/span/a/abbr/./../@href').re_first(r'/(\d+)[/?]'))
    print('header: ', remove_tags(post.xpath('.//span[@class="fwn fcg"]/span').extract()[0], which_ones=('span', 'a', )))
    print('header: ', ''.join(post.xpath('.//span[@class="fwn fcg"]/span//text()').extract()))
    print('Date: ', post.xpath('.//span/span/a/abbr/span/text()').extract())
    print('timestamp: ', post.xpath('.//span/span/a/abbr/@data-utime').extract()[0])
    print('Text len: ', len(post.xpath('.//p/text()').extract()))
    if post.xpath('.//p').extract():
        print('Text: ', remove_tags(post.xpath('.//p').extract()[0], which_ones=('p', 'span', 'a', 'img',)))
    print('Hashtash link: ', post.xpath(".//a[contains(@href,'hashtag')]/@href").extract())
    print('Hashtash name: ', post.xpath(".//a[contains(@href,'hashtag')]/span//text()").extract())
    hashtags = {}
    hashtags_t = post.xpath(".//a[contains(@href,'hashtag')]")
    for hashtag in hashtags_t:
        hashtag_name = ''.join(hashtag.xpath("./span//text()").extract())
        hashtag_link = hashtag.xpath("./@href").extract_first()
        hashtags[hashtag_name] = hashtag_link
    print('hashtags: ', hashtags)
    # print('link_of_content: ', post.xpath('.//div[@class="mtm"]/div/a//@href').extract())
    print('link_of_content: ', post.xpath(".//a[contains(@rel,'theater')]/@href").extract())
    # print('link_shared: ', post.xpath('.//div[@class="mtm"]/div/div/div/span/div/a/@href').extract())
    print('link_shared: ', post.xpath('.//a[@rel="nofollow" and contains(@href, "l.facebook")]/@href').extract())
    # print('N.like: ', post.xpath(".//a[contains(@href,'reaction')]/span/span/text()").extract())
    like = post.xpath(".//div[contains(@class,'UFILikeSentenceText')]/span/text()").extract()[0]
    like = ''.join(list(filter(str.isdigit, like)))
    if like:
        like = int(like) + 3
    else:
        like = 3
    print('N.like: ', like)
    # print('N.comment: ', post.xpath(".//a[contains(@href,'comment_tracking')]/text()").extract())
    comment = post.xpath(".//div[contains(@class,'UFILastCommentComponent')]/div/div/a/text()").extract()
    if comment:
        comment = comment[0]
        if any(char.isdigit() for char in comment):
            comment = int(''.join(list(filter(str.isdigit, comment)))) + 2
        else:
            comment = 2
    
    print('N.comment: ', comment)
    print('N.share: ', post.xpath(".//a[contains(@href,'shares')]/text()").re_first(r'([.0-9]+) [lượt chia sẻ|shares]'))
    print('N.view: ', post.xpath(".//form[contains(@class,'commentable_item')]/div/div/span/text()").re_first(r'([0-9]+?K) [lượt xem|Views]'))

