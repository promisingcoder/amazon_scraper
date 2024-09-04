import scrapy


class AmazonProductExtractorPySpider(scrapy.Spider):
    name = "amazon_product_extractor.py"
    allowed_domains = ["amazon.com","amazon.eg"]
    start_urls = ["https://amazon.com"]

    def parse(self, response):
        pass
