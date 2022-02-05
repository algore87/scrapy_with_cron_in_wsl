#!/usr/bin/env python3

"""
Webscraper based on https://www.packtpub.com/mapt/book/big_data_and_business_intelligence/9781787285217/1/ch01lvl1sec14/scraping-python.org-with-scrapy
"""

import scrapy, time, webbrowser
from scrapy.crawler import CrawlerProcess

class PythonEventsSpider(scrapy.Spider):
    name = 'pythoneventsspider'

    start_urls = ['https://geizhals.de/sony-playstation-5-825gb-weiss-a2374643.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk']
    found_events = []

    def parse(self, response):
        for event in response.xpath('//*[@id="offer__price-0"]/span'): # xpath found with chrome STRG+SHIFT+I, select the element and right_click->Copy->Copy XPATH
            event_details = dict()
            event_details['price'] = int(event.xpath('//span[@class="gh_price"]/text()').extract_first()[2:5]) # cuts (example: '€ 719,00' -> '719') and casts to integer
            self.found_events.append(event_details)

def crawl():
    process = CrawlerProcess({ 'LOG_LEVEL': 'ERROR'})
    process.crawl(PythonEventsSpider)
    spider = next(iter(process.crawlers)).spider
    process.start()

    for event in spider.found_events:
        print('Verfügbarer Preis: {}'.format(event['price']))
        if event['price'] < 720: # only open browsertab if the price is below xxx euros
            webbrowser.open(spider.start_urls[0])   # export BROWSER=/mnt/c/Windows/explorer.exe to run main default browser in .bashrc
                                                    # set BROWSER in /etc/profile.d or /etc/environment to use it with cronjob
    



if __name__ == "__main__":
    crawl()
    
