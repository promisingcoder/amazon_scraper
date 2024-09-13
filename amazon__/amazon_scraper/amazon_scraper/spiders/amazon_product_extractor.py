import scrapy
import re 
import string
def has_digits(a):
    for item in a:
        if item in string.digits:
            return True
def format(str1):
    new_string = ""
    for char in str1:
       
            
        if char.isalpha() or  char  in string.digits or char == ":" or char == " ":
            new_string += char
    
        
        
    modified =  new_string.split(" ")
    return(" ".join([a for a in modified if a.isalpha() or has_digits(a)]))
class AmazonProductExtractorPySpider(scrapy.Spider):
    name = "amazon_product_extractor.py"
    allowed_domains = ["amazon.com","amazon.eg"]
    def __init__(self, domain=None, *args, **kwargs):
        self.domain = domain

    def start_requests(self):
        urls = [self.domain]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        reviews = response.xpath("//div[contains(@id, 'customer_review')]")
        extracted_product = {}

        # Extract general product information using the provided selectors
        extracted_product['productTitle'] = response.css("span#productTitle::text").get().strip()
        extracted_product['rating'] = response.css("div#averageCustomerReviews span.a-color-base::text").get()
        extracted_product['price'] = response.css("span.a-price span.a-offscreen::text").get()
        extracted_product['product_color'] = response.css("div.a-row span.selection::text").getall()
        extracted_product['category_product_details'] = response.css("div.a-spacing-top-small tr::text").getall()
        extracted_product['category_product_details_value'] = response.css("span.a-size-base::text").getall()
        extracted_product['product_description'] = response.css("div#productDescription p span::text").get()

        # Loop through each review to extract details
        for review in reviews:
            extracted_product[review.attrib["id"]] = {
                "review_user_name": review.css("span.a-profile-name::text").get(),
                "review_title": review.css("a[data-hook='review-title'] span.cr-original-review-content::text").get(),
                "review_stars": review.css("span.a-icon-alt::text").get(),
                "review_product_size": review.css("span[data-hook='format-strip-linkless']::text").get(),
                "review_verified_purchase": review.css("span[data-hook='avp-badge-linkless']::text").get(),
                "review_date": review.css("span[data-hook='review-date']::text").get(),
                "review_details": review.css("div[data-hook='review-collapsed'] span.cr-original-review-content::text").get(),
                "found_it_helpful": review.css("span.cr-vote-text::text").get()
            }

            # Use response selectors directly for elements not within each review
            extracted_product['review_user_name'] = response.css("div[data-hook='genome-widget'] a.a-profile::text").get()
            extracted_product['review_title'] = response.css("a[data-hook='review-title'] span.cr-original-review-content::text").get()
            extracted_product['review_stars'] = response.css("span.a-icon-alt::text").get()
            extracted_product['review_product_size'] = response.css("span[data-hook='format-strip-linkless']::text").get()
            extracted_product['review_verified_purchase'] = response.css("span[data-hook='avp-badge-linkless']::text").get()
            extracted_product['review_date'] = response.css("span[data-hook='review-date']::text").get()
            extracted_product['review_details'] = response.css("div[data-hook='review-collapsed'] span.cr-original-review-content::text").get()

            
        yield extracted_product

