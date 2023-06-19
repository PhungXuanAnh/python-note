import scrapy


class QuotesSpider(scrapy.Spider):
    name = "0.scrapy_at_a_glance"
    start_urls = [
        "https://quotes.toscrape.com/tag/humor/",
    ]
    
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'my_project.pipelines.QuotesMongoPipeline': 300,
    #     }
    # }

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "author": quote.xpath("span/small/text()").get(),
                "text": quote.css("span.text::text").get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            
            # yield response.follow(next_page, self.parse)