import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor

import requests
import logging
import os
import re
import json
import random
import datetime
import hashlib

# import sys
# sys.path.append("../")
# from param_injection import ParamInjectors
# from parsing_html_table_standalone import 

class SeleniumSpider(scrapy.Spider):
    name = 'static_page'    

    def __init__(self, crawler_id, *a, **kw):
        self.crawler_id = crawler_id
        with open(f"config/{crawler_id}_config.json", "r") as f:
            self.config = json.loads(f.read())

        folders = [
            f"data/{crawler_id}",
            f"data/{crawler_id}/raw_pages",
            f"data/{crawler_id}/csv",
            f"data/{crawler_id}/files",
        ]
        for f in folders:
            try:
                os.mkdir(f)
            except FileExistsError:
                pass
        
        with open(f"data/{crawler_id}/files/file_description.txt", "a+") as f:
            pass

    def start_requests(self):
        if self.config["url"]["type"] == "simple":
            urls = [self.config["url"]["url"]]
        elif self.config["url"]["type"] == "template":
            # urls = ParamInjector.generate_format(
            #     self.config["url"]["tamplate_params"]["code_format"],
            #     self.config["url"]["tamplate_params"]["param_limits"],
            #     self.config["url"]["tamplate_params"]["verif"],
            #     self.config["url"]["tamplate_params"]["verif_index"],
            # )
            pass
        else:
            raise ValueError
        
        if self.config["crawler_type"] == "single_file":
            raise ValueError
        elif self.config["crawler_type"] == "file_bundle":
            raise ValueError
        elif self.config["crawler_type"] == "deep_crawler":
            raise ValueError
        elif self.config["crawler_type"] == "static_page":
            # DO STUFF
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse) 
        else:
            raise ValueError

    def hash(self, string):
        return hashlib.md5(string.encode()).hexdigest()

    def store_raw(self, response):
        """Store file, TODO convert to csv?"""
        assert response.headers['Content-type'] != b'text/html'

        file_format = str(response.headers['Content-type']).split("/")[1][:-1]
        hsh = self.hash(response.url)
        content = {
            "hash": hsh,
            "url": response.url,
            "crawler_id": self.crawler_id,
            "type": str(response.headers['Content-type']),
            "crawled_at_date": str(datetime.datetime.today()),
        }

        with open(f"data/{self.crawler_id}/files/{hsh}.{file_format}", "wb") as f:
            f.write(response.body)

        with open(f"data/{self.crawler_id}/files/file_description.txt", "a+") as f:
            f.write(json.dumps(content) + '\n')

    def extract_and_store_csv(self, response):
        """
        Try to extract a csv from response data
        TODO Chama metodo do Caio
        """
        pass

    def store_html(self, response):
        """
        """
        assert response.headers['Content-type'] == b'text/html'
        
        content = {
            "url": response.url,
            "crawler_id": self.crawler_id,
            "crawled_at_date": str(datetime.datetime.today()),
            "html": str(response.body),
        }

        with open(f"data/{self.crawler_id}/raw_pages/{self.hash(response.url)}.json", "w+") as f:
            f.write(json.dumps(content, indent=2))

    def parse(self, response):
        # self.logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>> {response.url}")
        self.logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {response.headers['Content-type']}")
        
        self.extract_and_store_csv(response)

        if response.headers['Content-type'] == b'text/html':
            self.store_html(response)

            if "link_extractor" in self.config:
                # self.logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>> {self.config['link_extractor']}")
                if_present = lambda key, default: key if key in self.config["link_extractor"] else default
                links_extractor = LinkExtractor(
                    # TODO: cant make regex tested on https://regexr.com/ to work here for some reason
                    # allow=if_present("allow", ())
                    deny=if_present("deny", ()),
                    allow_domains=if_present("allow_domains", ()),
                    deny_domains=if_present("deny_domains", ()),
                    # Note here: changed the default value. It would ignore all links with extensions
                    deny_extensions=if_present("deny_extensions", []), 
                    restrict_xpaths=if_present("restrict_xpaths", ()),
                    restrict_css=if_present("restrict_css", ()),
                    tags=if_present("tags", 'a'),
                    attrs=if_present("attrs", 'href'),
                    canonicalize=if_present("canonicalize", False),
                    unique=if_present("unique", True),
                    process_value=if_present("process_value", None),
                    strip=if_present("strip", True) 
                )

                # As I could not make the allow parameter work, the code check the regex on the urls here
                for url in links_extractor.extract_links(response):
                    match = False
                    if "allow" in self.config["link_extractor"]:
                        for pattern in self.config["link_extractor"]["allow"]:
                            match = match or (re.search(pattern, url.url) is not None)
                    else:
                        match = True
                    
                    if match:
                        # self.logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> would call: {url.url}")
                        yield scrapy.Request(url=url.url, callback=self.parse)
                # Fixing the allow parameter, just change the code above by the code commented below
                # for url in links_extractor.extract_links(response):
                #     yield scrapy.Request(url=url.url, callback=self.parse)
                # END CODE
        else:
            self.store_raw(response)