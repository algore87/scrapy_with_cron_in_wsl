#!/usr/bin/env python3
import scrapy, time, webbrowser
from scrapy.crawler import CrawlerProcess

found = False # if found, stop crawling

class PythonEventsSpider(scrapy.Spider):
    name = 'pythoneventsspider'

    start_urls = ['https://www.telekom.de/unterwegs/samsung/samsung-galaxy-s7/schwarz-32gb-ohne-vertrag',
                  'https://www.telekom.de/unterwegs/samsung/samsung-galaxy-s7/silber-32gb-ohne-vertrag',
                  'https://www.telekom.de/unterwegs/samsung/samsung-galaxy-s7/weiss-32gb-ohne-vertrag',
                  'https://www.telekom.de/unterwegs/samsung/samsung-galaxy-s7/gold-32gb-ohne-vertrag']
    found_events = []

    def parse(self, response):
        for event in response.xpath('//div[@class="col-l-7 col-s-12"]'):
            event_details = dict()
            event_details['color'] = event.xpath('//span[@class="t9 color-configuration__color-name--value"]/text()').extract_first()
            event_details['price'] = event.xpath('//span[@class="p1 price__total-price price__total-price--big"]/text()').extract_first()
            event_details['available'] = event.xpath('//div[@class="t8 intro-configuration__details-info-delivery-information"]/text()').extract_first()[9:]
            self.found_events.append(event_details)

def crawl():
    process = CrawlerProcess({ 'LOG_LEVEL': 'ERROR'})
    process.crawl(PythonEventsSpider)
    spider = next(iter(process.crawlers)).spider
    process.start()

    which_available = []
    for event in spider.found_events: 
        print(event)
        if event['available'] != 'Aktuell nicht lieferbar':
            which_available.append(event)
    

    print('Verfügbar: {}'.format(which_available))
    for available in which_available: # open new tab with available handy to buy
        for url in spider.start_urls:
            if available.get('color').lower() in url:
                webbrowser.open(url)    # export BROWSER=/mnt/c/Windows/explorer.exe to run main default browser in .bashrc
                                        # set BROWSER in /etc/profile.d or /etc/environment to use it with cronjob
                found = True
    return found


if __name__ == "__main__":
    found = crawl()
    print(found)
    
