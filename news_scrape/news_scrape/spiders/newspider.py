from pathlib import Path
from typing import Any
import scrapy
from scrapy.http import Response
import os
from dotenv import load_dotenv
from kafka import KafkaProducer
import json

load_dotenv()

class NewSpider(scrapy.Spider):
    name = "newspider"
    page_counter = 0

    def __init__(self, *args, **kwargs):
        super(NewSpider, self).__init__(*args, **kwargs)
        self.producer = KafkaProducer(   
        bootstrap_servers=['broker:29092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def start_requests(self):
        url = os.getenv('NEWS_URL')
        tag = getattr(self, "tag", None)
        if tag is not None:
            url = url + "tag/" + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        self.page_counter += 1
        i = 0
        descArray = response.xpath("//span[@class='content-text']/text()").getall()

        for titles in response.xpath("//a[@class='card-title']/text()").getall():
            description = descArray[i]
            i += 1 
            
            data = {
                "title": titles,
                "description": description
            }
            self.producer.send('ratatoy', value=data)
            yield data

        next_page = response.xpath("//meta[@property='og:url']/@content").get()
        next_page = f"{next_page}{self.page_counter}"
        
        if (next_page is not None) and (self.page_counter <= 10):
            yield response.follow(next_page, self.parse)