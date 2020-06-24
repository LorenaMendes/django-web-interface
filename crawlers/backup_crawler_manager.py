import json
import time
import random
from multiprocessing import Process
import os
import sys
import shutil

import scrapy
from scrapy.crawler import CrawlerProcess

from crawlers.constants import *

import requests

# from .crawlers.static_page import StaticPageSpider
# from .crawlers.static_page import StaticPageSpider
# from .crawlers.static_page import StaticPageSpider
from crawlers.static_page import StaticPageSpider

def get_crawler_base_settings():
    """Returns scrapy base configurations."""
    return {
        "BOT_NAME": "crawlers",
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 1,
        "SELENIUM_DRIVER_NAME": "chrome",
        "SELENIUM_DRIVER_EXECUTABLE_PATH": shutil.which("{CURR_FOLDER_FROM_ROOT}/webdriver/chromedriver_win32_chr_81.exe"),
        # SELENIUM_DRIVER_ARGUMENTS: [],
        "SELENIUM_DRIVER_ARGUMENTS": ["--headless"],
        "DOWNLOADER_MIDDLEWARES": {"scrapy_selenium.SeleniumMiddleware": 0},
        "DOWNLOAD_DELAY": 1,
    }

def crawler_process(crawler_id, config):
    """Starts crawling."""
    # Redirects process logs to files
    sys.stdout = open(f"{CURR_FOLDER_FROM_ROOT}/log/{crawler_id}.out", "a", buffering=1)
    sys.stderr = open(f"{CURR_FOLDER_FROM_ROOT}/log/{crawler_id}_error.out", "a", buffering=1)

    process = CrawlerProcess(settings=get_crawler_base_settings())

    if config["crawler_type"] == "single_file":
        # process.crawl(StaticPageSpider, crawler_id=crawler_id)
        raise NotImplementedError
    elif config["crawler_type"] == "file_bundle":
        # process.crawl(StaticPageSpider, crawler_id=crawler_id)
        raise NotImplementedError
    elif config["crawler_type"] == "deep_crawler":
        # process.crawl(StaticPageSpider, crawler_id=crawler_id)
        raise NotImplementedError
    elif config["crawler_type"] == "static_page":
        process.crawl(StaticPageSpider, crawler_id=crawler_id)
    
    def spider_error():
        print(f"Error at: {crawler_id}")
        # TODO: get port as variable
        port = 8000
        requests.get(f'http://localhost:{port}/detail/stop_crawl/{config["id"]}/{crawler_id}')

    for crawler in process.crawlers:
        crawler.signals.connect(
            spider_error,
            signal=scrapy.signals.spider_error
        )

    process.start()

def gen_key():
    """Generates a unique key based on time and a random seed."""
    return str(int(time.time()*100)) + str((int(random.random() * 1000)))

def start_crawler(config):
    """Create and starts a crawler as a new process."""
    crawler_id = gen_key()
    print(os.getcwd())
    
    with open(f"{CURR_FOLDER_FROM_ROOT}/config/{crawler_id}.json", "w+") as f:
        f.write(json.dumps(config, indent=2))
    
    with open(f"{CURR_FOLDER_FROM_ROOT}/flags/{crawler_id}.json", "w+") as f:
        f.write(json.dumps({"stop": False}))

    # starts new process
    p = Process(target=crawler_process, args=(crawler_id, config))
    p.start()

    return crawler_id

def stop_crawler(crawler_id):
    """Sets the flags of a crawler to stop."""
    with open(f"{CURR_FOLDER_FROM_ROOT}/flags/{crawler_id}.json", "w+") as f:
        f.write(json.dumps({"stop": True}))

def remove_crawler(crawler_id, are_you_sure=False):
    """
    CAUTION: Delete ALL files and folders created by a crawler run.
    This includes all data stored under {CURR_FOLDER_FROM_ROOT}/data/{crawler_id}.
    Save data before deleting.
    """

    if are_you_sure == False:
        msg = "ERROR: Delete ALL files and folders created by a crawler run. " \
            f"This includes all data stored under {CURR_FOLDER_FROM_ROOT}/data/{crawler_id}. " \
            "Save data before deleting. "
        raise Exception(msg)

    files = [
        f"{CURR_FOLDER_FROM_ROOT}/config/{crawler_id}.json",
        f"{CURR_FOLDER_FROM_ROOT}/flags/{crawler_id}.json",
        f"{CURR_FOLDER_FROM_ROOT}/log/{crawler_id}.out",
        f"{CURR_FOLDER_FROM_ROOT}/log/{crawler_id}_error.out",

    ]
    for f in files:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass

    folders = [
        f"{CURR_FOLDER_FROM_ROOT}/data/{crawler_id}",
    ]
    for f in folders:
        try:
            shutil.rmtree(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

if __name__ == '__main__':
    start_crawler(
        {
            "id": 17,
            "source_name": "Di\u00e1rio Oficial de S\u00e3o Louren\u00e7o",
            "base_url": "https://saolourenco.mg.gov.br/poficiais.php",
            "obey_robots": True,
            "antiblock": "ip",
            "ip_type": "tor",
            "proxy_list": None,
            "max_reqs_per_ip": 4,
            "max_reuse_rounds": 3,
            "reqs_per_user_agent": None,
            "user_agents_file": None,
            "delay_secs": None,
            "delay_type": "random",
            "cookies_file": None,
            "persist_cookies": False,
            "captcha": "none",
            "img_xpath": None,
            "img_url": None,
            "sound_xpath": None,
            "sound_url": None,
            "crawler_type": "static_page",
            "explore_links": True,
            "link_extractor_max_depht": 1,
            "link_extractor_allow_extensions": "pdf",
            "link_extractor_allow": "(^https\\:\\/\\/saolourenco\\.mg\\.gov\\.br\\/poficiais\\.php|^https\\:\\/\\/saolourenco\\.mg\\.gov\\.br\\/arquivos\\/publicacaooficial\\/)"
        }
    )

    #config = {"id": 17,"source_name": "Di\u00e1rio Oficial de S\u00e3o Louren\u00e7o","base_url": "https://saolourenco.mg.gov.br/poficiais.php","obey_robots": True,"antiblock": "ip","ip_type": "tor","proxy_list": None,"max_reqs_per_ip": 4,"max_reuse_rounds": 3,"reqs_per_user_agent": None,"user_agents_file": None,"delay_secs": None,"delay_type": "random","cookies_file": None,"persist_cookies": False,"captcha": "none","img_xpath": None,"img_url": None,"sound_xpath": None,"sound_url": None,"crawler_type": "static_page","explore_links": True,"link_extractor_max_depht": 1,"link_extractor_allow": "(^https\\:\\/\\/saolourenco\\.mg\\.gov\\.br\\/poficiais\\.php|^https\\:\\/\\/saolourenco\\.mg\\.gov\\.br\\/arquivos\\/publicacaooficial\\/)", "link_extractor_allow_extensions": "pdf",}