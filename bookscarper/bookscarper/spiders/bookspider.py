import scrapy
from bookscarper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(book_url, callback=self.parse_book_page, method='GET')

        next_page = response.css('li.next a ::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse, method='GET')

    def parse_book_page(self, response):
        tables_rows = response.css("table tr")
        book_item = BookItem()
        book_item['url'] = response.url
        book_item['title'] = response.css('.product_main h1::text').get()
        book_item['product_type'] = tables_rows[1].css('td ::text').get()
        book_item['price_excl_tax'] = tables_rows[2].css('td ::text').get()
        book_item['price_incl_tax'] = tables_rows[3].css('td ::text').get()
        book_item['tax'] = tables_rows[4].css('td ::text').get()
        book_item['availability'] = tables_rows[5].css('td ::text').get()
        book_item['num_reviews'] = tables_rows[6].css('td ::text').get()
        book_item['stars'] = response.css('p.star-rating').attrib['class']
        book_item['category'] = response.xpath(
            '//ul[@class="breadcrumb"]/li[@class="active"]/preceding-sibling::li[1]/a/text()').get()
        book_item['description'] = response.xpath(
            '//div[@id="product_description"]/following-sibling::p/text()').get()
        book_item['price'] = response.css('p.price_color ::text').get()

        yield book_item
