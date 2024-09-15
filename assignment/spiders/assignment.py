import scrapy
import json


class NewsSpider(scrapy.Spider):
    name = 'assignment'

    # List of start URLs (the homepages)
    start_urls = [
        'https://www.livemint.com',
        'https://economictimes.indiatimes.com',
        'https://www.telegraf.rs',
        'https://inc42.com',
        'https://www.digitalterminal.in'
    ]

    def parse(self, response):
        # Select article links from the homepage using basic selectors
        article_links = response.css('a::attr(href)').getall()

        # Loop through article links and send them to parse_article method
        for link in article_links:
            if link.startswith('/'):  # Convert relative links to absolute
                link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article)

    def parse_article(self, response):
        # Extract necessary data using CSS selectors
        article_data = {
            'Article URL': response.url,
            'Title': response.css('title::text').get(),  # Simplified title extraction
            'Author Name': response.css('.author-name::text').get(),  # Adjust according to site's structure
            'Author URL': response.css('.author-name a::attr(href)').get(),  # Optional
            'Article Content': ' '.join(response.css('p::text').getall()),  # Grab all paragraphs
            'Published Date': response.css('.publish-date::text').get()  # Simplified date extraction
        }

        # Yield the article data as JSON
        yield article_data
