from core.linkedin import LinkedIn
from core.chatgpt import ChatGpt
from core.scraper import Scraper
import requests
from core.news import News

import random
from re import sub

from utils import get_file_data, custom_print


class ContentManager:
    @staticmethod
    def load_config(fpath):
        return get_file_data(fpath)

    def __init__(self, config_path):

        self.config = self.load_config(config_path)

        # Initialize all config options as instance variables
        self.cookies            = self.config.get("cookies")
        self.chatgpt            = ChatGpt( self.config.get("open_ai_api_key") )
        topic = input('\nInput a topic: ')
        res = News.getUrls(topic)
        self.images = [x['image'] for x in res]
        self.urls               = res
        self.preamble           = self.config.get("gpt_preamble")
        self.bio                = self.config.get("bio")
        self.gpt_token_limit    = self.config.get("gpt_token_limit")
        self.scrape_char_limit  = self.config.get("scrape_char_limit")

    def fetch_website_content(self):
        # TODO: look into using chatgpt to format scraped data.
        content = []
        urls = [x['url'] for x in self.urls]
        for url in urls:
            data = Scraper(url, self.scrape_char_limit).fetch_content()
            if data:
                content.append('url: '+url+'data: '+data)
        random.shuffle(content)

        return content
    
    def fetch_website_content2(self):
        # TODO: look into using chatgpt to format scraped data.
        content = []
        for url in self.urls:
            content.append('url: '+url['url']+'data: '+url['text'])
        random.shuffle(content)

        return content

    def process_gpt_response(self, content):
        # Combine preamble, bio, and website content into the correctly formatted messages
        gpt_messages = [
            {"role": "system", "content": self.preamble},
            {"role": "system", "content": self.bio},
        ] + [
            {"role": "user", "content": item} for item in content
        ]
        gpt_res = self.chatgpt.ask(gpt_messages, self.gpt_token_limit)

        if not gpt_res:
            return None

        return gpt_res

    def post_content(self):
        
        if self.config.get('scraper'):
            content         = self.fetch_website_content()
        else:
            content         = self.fetch_website_content2()
        gpt_response    = self.process_gpt_response(content)
        if not gpt_response:
            custom_print("Error: gpt response empty")
            return

        linkedin        = LinkedIn(self.cookies)
        print(gpt_response)
        proceed = input('\nProceed? (y/n): ')
        if proceed=='y':
            linkedin.post_file(gpt_response,  self.images)
        print('Posted')
