import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor

from main.src.base_spider import BaseSpider

import requests
import logging
import os
import re
import json
import random
import datetime
import hashlib

class StaticPageSpider(BaseSpider):
    name = 'static_page'    

    def start_requests(self):
        urls = [self.config["base_url"]]
        # if self.config["url"]["type"] == "simple":
        #     urls = [self.config["url"]["url"]]
        # elif self.config["url"]["type"] == "template":
        #     # urls = ParamInjector.generate_format(
        #     #     self.config["url"]["tamplate_params"]["code_format"],
        #     #     self.config["url"]["tamplate_params"]["param_limits"],
        #     #     self.config["url"]["tamplate_params"]["verif"],
        #     #     self.config["url"]["tamplate_params"]["verif_index"],
        #     # )
        #     pass
        # else:
        #     raise ValueError
        
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

    def parse(self, response):
        """
        Parse responses of static pages.
        Will try to follow links if config["explor_links"] is set.
        """
        # self.logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>> {response.url}")
        self.logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {response.headers['Content-type']}")
        
        self.extract_and_store_csv(response)

        if response.headers['Content-type'] == b'text/html':
            self.store_html(response)

            if self.config["explore_links"]:
                # self.logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>> {self.config['link_extractor']}")
                # if_present = lambda key, default: key if key in self.config["link_extractor"] else default
                links_extractor = LinkExtractor(
                    # # TODO: cant make regex tested on https://regexr.com/ to work here for some reason
                    # # allow=if_present("allow", ())
                    # deny=if_present("deny", ()),
                    # allow_domains=if_present("allow_domains", ()),
                    # deny_domains=if_present("deny_domains", ()),
                    # # Note here: changed the default value. It would ignore all links with extensions
                    # deny_extensions=if_present("deny_extensions", []), 
                    # restrict_xpaths=if_present("restrict_xpaths", ()),
                    # restrict_css=if_present("restrict_css", ()),
                    # tags=if_present("tags", 'a'),
                    # attrs=if_present("attrs", 'href'),
                    # canonicalize=if_present("canonicalize", False),
                    # unique=if_present("unique", True),
                    # process_value=if_present("process_value", None),
                    # strip=if_present("strip", True) 
                )

                # As I could not make the allow parameter work, the code check the regex on the urls here
                for url in links_extractor.extract_links(response):
                    match = False
                    if self.config["link_extractor_allow"] != "":
                        # for pattern in self.config["link_extractor_allow"]:
                        #     match = match or (re.search(pattern, url.url) is not None)
                        match = match or (re.search(self.config["link_extractor_allow"], url.url) is not None)

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