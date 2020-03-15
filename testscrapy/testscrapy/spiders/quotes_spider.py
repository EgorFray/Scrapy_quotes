import scrapy
from scrapy.http import FormRequest
from ..items import TestscrapyItem
from scrapy.utils.response import open_in_browser


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/login'
    ]

    def parse(self, response):
        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': 'fatamorganaa933@gmail.com',
            'password': '123'
        }, callback=self.start_scrapping)

    def start_scrapping(self, response):
        open_in_browser(response)
        items = TestscrapyItem()

        all_div_quote = response.css('div.quote')

        for quotes in all_div_quote:
            title = quotes.css('span.text::text').extract()
            author = quotes.css('.author::text').extract()
            tags = quotes.css('.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tags'] = tags

            yield items

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.start_scrapping(response))