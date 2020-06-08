import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor

import requests
import logging
import os
import re
import json
import random

import sys
sys.path.append("../")
from param_injection import ParamInjector

class SeleniumSpider(scrapy.Spider):
    name = 'static_page'    

    def __init__(self, crawler_id, *a, **kw):
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

    def start_requests(self):
        if self.config["url"]["type"] == "simple":
            urls = [self.config["url"]["url"]]
        elif self.config["url"]["type"] == "template":
            urls = ParamInjector.generate_format(
                self.config["url"]["tamplate_params"]["code_format"],
                self.config["url"]["tamplate_params"]["param_limits"],
                self.config["url"]["tamplate_params"]["verif"],
                self.config["url"]["tamplate_params"]["verif_index"],
            )
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

    def store_raw(self, response):
        """TODO Save a non-html file"""
        pass

    def extract_and_store_csv(self, response):
        """
        Try to extract a csv from response data
        TODO Chama metodo do Caio
        """
        pass

    def store_html(self, response):
        """TODO Save html file"""
        pass

    def parse(self, response):
        # self.logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>> {response.url}")
        self.logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>> {response.headers['Content-type']}")
        
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

                for url in links_extractor.extract_links(response):
                    match = False
                    if "allow" in self.config["link_extractor"]:
                        for pattern in self.config["link_extractor"]["allow"]:
                            if re.search(pattern, url.url) is not None:
                                match = True               
                    else:
                        match = True
                    
                    if match:
                        # self.logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>> {temp} found: {url}")
                        yield scrapy.Request(url=url.url, callback=self.parse)
                    else:
                        # self.logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>> excluded: {url}")
                        pass
            else:
                self.store_raw(response)


"""
TODO:
- make kafka start crawlers
- take log from kafka and show in the UI
- the generic spiders for the other type of crawlers
"""