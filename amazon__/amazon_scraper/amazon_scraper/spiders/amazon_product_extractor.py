import scrapy


class AmazonProductExtractorPySpider(scrapy.Spider):
    name = "amazon_product_extractor.py"
    allowed_domains = ["amazon.com","amazon.eg"]
    start_urls = ["https://www.amazon.eg/-/en/Testa-Toro-TESTA-Comfortable-Everyday/dp/B0CTYN7GTT/"]

    def parse(self, response):
        reviews = response.xpath("//div[contains(@id, 'customer_review')]")
        extracted_product = {}
        extracted_product['productTitle']  = response.css("span#productTitle::text").get()
        extracted_product['rating'] = response.css("div#averageCustomerReviews span#acrPopover").xpath("text()").get()
        extracted_product['price'] = " ".join([tag.xpath("text()").get() for tag in  response.css("div#corePrice_desktop span.a-price *") if tag.xpath("text()").get() != None ])
        extracted_product['color'] = response.css("img.imgSwatch").xpath("@alt").getall()
        extracted_product['Product Details'] = response.css("div#productFactsDesktopExpander span.a-color-base::text").get()
        extracted_product['Product description'] = response.css("div#productDescription  span::text").get()
        extracted_product['product_details_general'] = response.css("div#detailBullets_feature_div span.a-list-item::text")
        
        for review in reviews:
            extracted_product[review.attrib["id"]] = {
                "review_person_name" : review.css("span.a-profile-name::text").get(),
                "review_title" : review.css("span.cr-original-review-content::text").get(),
                "review_rating" : review.css("i[data-hook='review-star-rating'] span.a-icon-alt::text").get(),
                "review_date" : review.css('span[data-hook="review-date"]::text').get(),
                "review_product_size_and_color" : review.css('span[data-hook="format-strip-linkless"]::text').get()
                ,
                "review_content" : review.css('span.cr-original-review-content::text').get(),
                "found_it_helpful" : review.css('span.cr-vote-text::text').get()
            } 
        yield extracted_product

