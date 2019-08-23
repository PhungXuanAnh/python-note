import json
import scrapy
from scrapy.selector import Selector


# url = "https://www.facebook.com/K14vn"
url = "https://www.facebook.com/mytam.info"
headers = {
    "accept-language": "vi,en;q=0.9,es;q=0.8,pl;q=0.7",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
    "accept": "*/*",
    "authority": "www.facebook.com"
}
response = scrapy.Request(url=url,
                          headers=headers,
                          dont_filter=True)
fetch(response)

# -------------------------------------------------- get page_id

# get first page_id

page_id_url = Selector(text=response.body).xpath('//div[@id="www_pages_reaction_see_more_unitwww_pages_home"]/div/a/@ajaxify').extract_first()
page_id_url = response.urljoin(page_id_url) + "&__a=1&__user=0"

for i in range(0, 5):
    headers["referer"] = url
    response = scrapy.Request(url=page_id_url, headers=headers,dont_filter=True)
    fetch(response)
    domops = json.loads(response.body_as_unicode()[9:])["domops"][0]
    html = None
    for value in domops:
        if isinstance(value, dict):
            html = value.get("__html")
            break
    with open('/home/xuananh/Downloads/page{}.html'.format(i), 'w+') as f:
        f.write(html)
    page_id_url = Selector(text=html).xpath('//div[@id="www_pages_reaction_see_more_unitwww_pages_home"]/div/a/@ajaxify').extract_first()
    page_id_url = response.urljoin(page_id_url) + "&__a=1&__user=0"


viewcount = Selector(text=html).xpath('//div[contains(@class, "uiContextualLayerParent")]/div/span')

# ----------------
posts = Selector(text=html).xpath('//div[contains(@class, "userContentWrapper")]')

print('================================')
print(len(posts))

# --------------------------------------------------------------------------- get post
post_url = posts[0].xpath('.//span/span/a/abbr/./../@href').extract_first()
post_url = response.urljoin(post_url)

headers = {
    "accept-language": "vi,en;q=0.9,es;q=0.8,pl;q=0.7",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
    "accept": "*/*",
    "authority": "www.facebook.com",
    "referer": "https://www.facebook.com/mytam.info"
}
post_url = "https://www.facebook.com/mytam.info/videos/974961919357021/?__xts__[0]=68.ARCM82J3z847MHoJK4GvgWMdwFOBfyFWRxCe33XxbK4_X9SlGA8Fm18nE2FJhzGMVaVEjPJWTf--2VVa-EVs57v6x8hnX336TeqZHkqTMNHe4WrOVJYXWV9ZJACtjPIIJ6-qfvfd5viTn5-hZFL2va6h9I3F-tjYVOugDx53ghe6mriKpDo-&__tn__=-R"
response = scrapy.Request(url=post_url,
                          headers=headers,
                          dont_filter=True)
fetch(response)

Selector(text=response.body).xpath('.//code')

Selector(response).re(r'likecount:([.0-9]+)')
Selector(response).re(r'commentcount:([.0-9]+)')
Selector(response).re(r'sharecount:([.0-9]+)')
Selector(response).re(r'viewcount:([.0-9]+)')


post.xpath('.//code').extract()


print('header:', remove_tags(post.xpath('.//span[@class="fwn fcg"]').extract()[0], which_ones=('span', 'a', )))
print('Date: ', post.xpath('.//span/span/a/abbr/span/text()').extract())
print('timestamp: ', post.xpath('.//span/span/a/abbr/@data-utime').extract()[0])
print('Text len: ', len(post.xpath('.//p/text()').extract()))
if post.xpath('.//p').extract():
    print('Text: ', remove_tags(post.xpath('.//p').extract()[0], which_ones=('p', 'span', 'a', 'img',)))
hashtags_node = post.xpath('.//span[@aria-label="hashtag"]').xpath('..')
print('Hashtash link: ', post.xpath(".//a[contains(@href,'hashtag')]/@href").extract())
print('Hashtash name: ', post.xpath(".//a[contains(@href,'hashtag')]/span//text()").extract())
# print('link_of_content: ', post.xpath('.//div[@class="mtm"]/div/a//@href').extract())
print('link_of_content: ', post.xpath(".//a[contains(@rel,'theater')]/@href").extract())
# print('link_shared: ', post.xpath('.//div[@class="mtm"]/div/div/div/span/div/a/@href').extract())
print('link_shared: ', post.xpath('.//a[@rel="nofollow" and contains(@href, "l.facebook")]/@href').extract())
# print('N.like: ', post.xpath(".//a[contains(@href,'reaction')]/span/span/text()").extract())
like = post.xpath(".//div[contains(@class,'UFILikeSentenceText')]/span/text()").extract_first()
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
share = post.xpath(".//a[contains(@href,'shares')]/text()").extract()
if share:
    share = share[0][:-13]
print('N.share: ', share)
# print('N.view: ', post.xpath(".//a[contains(@href,'shares')]").xpath('../../div[3]/span/text()').extract())
view = post.xpath(".//form[contains(@class,'commentable_item')]/div/div/span/text()").extract()
if view:
    view = view[0][:-9]
print('N.view: ', view)



# ---------------------------- test fucntion parse next page

headers = {
    "accept-language": "vi,en;q=0.9,es;q=0.8,pl;q=0.7",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
    "accept": "*/*",
    "authority": "www.facebook.com"
}
scrapy shell 'https://www.facebook.com/pages_reaction_units/more/?page_id=153133638065261&cursor=%7B%22card_id%22%3A%22page_posts_card%22%2C%22has_next_page%22%3Atrue%7D&surface=www_pages_home&unit_count=8&referrer&__a=1&__user=0'
fetch('https://www.facebook.com/pages_reaction_units/more/?page_id=153133638065261&cursor=%7B%22card_id%22%3A%22page_posts_card%22%2C%22has_next_page%22%3Atrue%7D&surface=www_pages_home&unit_count=16&referrer&__a=1&__user=0')

import json
from scrapy.selector import Selector
response_json = json.loads(response.body_as_unicode()[9:])
domops = response_json["domops"][0]
html = None
for value in domops:
    if isinstance(value, dict):
        html = value.get("__html")
        break
html = Selector(text=html)
posts = html.xpath('//div[contains(@class, "userContentWrapper")]')
len(posts)
page_id_url = html.xpath('//div[@id="www_pages_reaction_see_more_unitwww_pages_home"]/div/a/@ajaxify').extract_first()
page_id_url = response.urljoin(page_id_url) + "&__a=1&__user=0"
page_id_url

for post in posts:
