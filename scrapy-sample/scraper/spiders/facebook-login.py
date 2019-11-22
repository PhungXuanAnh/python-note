# -*- coding: utf-8 -*-
import scrapy

"""
dung selenium: https://stackoverflow.com/a/35323713
"""

class FacebookLogin(scrapy.Spider):
    name = 'test'
    start_urls = ['https://www.walmart.ca/en/clothing-shoes-accessories/men/mens-tops/N-11+2566']

    def parse(self, response):
        with open('/home/xuananh/data/Temp/temp.html', 'w+') as f:
            f.write(response.body_as_unicode())

# https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110
# https://www.facebook.com/login.php?login_attempt=1

sigmasolutions.test@gmail.com
Sigma2017

pstempien@coretechnology.pl
coreTech@2019