import scrapy
import os

class KissmetricsSpider(scrapy.Spider):
    name = "kissmetrics"
    allowed_domains = ["kissmetrics.com"]
    start_urls = [
        "https://blog.kissmetrics.com/page/1/"
    ]
    pages_crawled = 0
    max_pages = 3

    def parse(self, response):
        if self.pages_crawled > self.max_pages:
            print "finished reading " + str(self.pages_crawled - 1) + " pages, finished paging."
            return

        for post_link in response.css(".entry-title a::attr('href')"):
            print "post link: " + post_link.extract()
            yield scrapy.Request(post_link.extract(), self.parse_post)

        next_pages = response.css("a.next::attr('href')")
        next_page = next_pages[0].extract()
        print "next page: " + next_page
        if next_page:
            self.pages_crawled += 1
            yield scrapy.Request(next_page, self.parse)

    def parse_post(self, response):
        html_dir = os.path.dirname(os.path.realpath(__file__)) + '/../../html/'
        filename = html_dir + response.url.split("/")[-2] + '.html'
        print "writing raw html to file -> " + filename
        with open(filename, 'wb') as f:
            f.write(response.body)
