import scrapy


class LozaSpider(scrapy.Spider):
    name = 'loza'

    start_urls = [
        "https://loza.vn/ao-so-mi-nu",
        # "https://loza.vn/quan-cong-so-nu",
        # "https://loza.vn/vay-dam",
        # "https://loza.vn/chan-vay",
        # "https://loza.vn/vest-nu",
        # "https://loza.vn/ao-khoac-nu",
        # "https://loza.vn/set-do",
        # "https://loza.vn/thoi-trang-dao-pho"
    ]

    def parse(self, response):
        for item_link in response.xpath('*//div[@class="category-products"]/ul/li[@class="item last"]/a/@href').extract():
        # for item_link in response.css('div.category-products li.item a.product-image::attr(href)').extract():
            # print(item_link)
            yield scrapy.Request(item_link, callback=self.parse_single_item)

    def parse_single_item(self, response):
        # for link in response.css('div.more-views ul li a img').xpath('@src').extract():
        for link in response.xpath('//div[@class="slick-slide slick-cloned"]/a/img/@src').extract():
            img_link = link.replace("thumbnail/200x280", "image/1000x")
            print(img_link)
            print('======================')
            # yield scrapy.Request(img_link, callback=self.parse_img)

    def parse_img(self, response):
        with open("images/%s" % response.url.split('/')[-1], 'wb') as f:
            f.write(response.body)
