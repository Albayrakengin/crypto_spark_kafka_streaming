from pathlib import Path
from typing import Any
from transformers import pipeline
import scrapy
from scrapy.http import Response
import os
from dotenv import load_dotenv

load_dotenv()

class QuotesSpider(scrapy.Spider):
    name = "newspider"
    start_urls = [
        os.getenv('NEWS_URL')
    ]
    load_dotenv()

    def parse(self, response: Response):
        i = 0
        for titles in response.css("div.card-title"):
            description = response.css("p::text")[i].get()
            i += 1 
            pipe = pipeline("sentiment-analysis")
            analaysis = pipe(description)
            yield {
                "title": titles.css("h4::text").get(),
                "description": description,
                "sentiment": analaysis[0]['label'],
                "score": analaysis[0]['score']
            }