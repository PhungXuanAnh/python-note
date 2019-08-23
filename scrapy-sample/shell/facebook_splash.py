# [s] Available Scrapy objects:
# [s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
# [s]   crawler    <scrapy.crawler.Crawler object at 0x7f13369c6908>
# [s]   item       {}
# [s]   settings   <scrapy.settings.Settings object at 0x7f1335313518>
# [s] Useful shortcuts:
# [s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
# [s]   fetch(req)                  Fetch a scrapy.Request and update local objects
# [s]   shelp()           Shell help (print this help)
# [s]   view(response)    View response in a browser


import scrapy
from scrapy_splash import SplashRequest

from scrapy.selector import Selector


# with open('/home/xuananh/Downloads/test.html', '+w') as f:
#     f.write(str(response.body))

def _read_lua(path):
    with open(path, 'r') as f:
        return f.read()


lua_shell = 'lua-scripts/facebook_shell.lua'

req = SplashRequest('https://m.facebook.com',
                    endpoint='execute',
                    args={'lua_source': _read_lua(lua_shell)})
fetch(req)

#------------------------------------------------------------------------

posts = Selector(response).xpath('//article/div')

for post in posts:
    print('==================================================')
    print('header', post.xpath('.//div[@class="_4g34"]/h3//text()').extract())
    print('--------------------------------------0')
    print('date: ', post.css('div[data-sigil="m-feed-voice-subtitle"] a abbr::text').extract())
    print('like', post.css('div[data-sigil="reactions-sentence-container"] div::text').extract())
    print('comment', post.css('div[data-sigil="reactions-bling-bar"] div span::text').extract())
    print('--------------------------------------1')
    print('date: ', post.xpath('.//div[@data-sigil="m-feed-voice-subtitle"]/a/abbr/text()').extract())
    print('like', post.xpath('.//div[@data-sigil="reactions-sentence-container"]/div/text()').extract())
    print('comment', post.xpath('.//div[@data-sigil="reactions-bling-bar"]/div/span/text()').extract())
    print('--------------------------------------2')
    