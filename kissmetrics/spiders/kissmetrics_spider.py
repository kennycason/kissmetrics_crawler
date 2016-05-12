import scrapy

class KissmetricsSpider(scrapy.Spider):
    name = "kissmetrics"
    allowed_domains = ["kissmetrics.com"]
    start_urls = [
        "https://blog.kissmetrics.com/page/1/"
    ]

    def parse(self, response):
        for post_link in response.css(".entry-title a::attr('href')"):
            print "post link: " + post_link.extract()
            yield scrapy.Request(post_link.extract(), self.parse_post)

        next_pages = response.css("a.next::attr('href')")
        next_page = next_pages[0].extract()
        print "next page: " + next_page
        if next_page:
            yield scrapy.Request(next_page, self.parse)

    def parse_post(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
