import time
from typing import List
import logging
import requests
import json
import logging
# from scrapy import Selector
import scrapy



def get_itunes_api_result(url: str) -> List[dict]:
    try:
        for _ in range(0, 2):
            response = requests.get(url)
            if response:
                response_map = response.json()
                results = response_map.get("results")
                time.sleep(2)
                print(results)
                return results
            time.sleep(2)
    except Exception:
        logging.debug(f"Got error when calling url [{url}]")
    return []


class PostsSpider(scrapy.Spider):
    name = "posts"

    start_urls = [
        'https://blog.scrapinghub.com/'
    ]

    def parse(self, response):
        for post in response.css('div.post-item'):
            yield {
                'title': post.css('.post-header h2 a::text')[0].get(),
                'date': post.css('.post-header a::text')[1].get(),
                'author': post.css('.post-header a::text')[2].get()
            }
        next_page = response.css('a.next-posts-link::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



if __name__ == "__main__":
    url = "http://itunes.apple.com/lookup?id=792893703&entity=song&country=us&limit=1000"
    data = get_itunes_api_result(url)



    # print(k[1].get(k, default = None))

    # url = "https://music.apple.com/us/album/clube-da-esquina-2/1361080094?uo=4"

    # get_itunes_api_result()


