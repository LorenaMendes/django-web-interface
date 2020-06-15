import json
import time
import random
from multiprocessing import Process
import os
import sys
from shutil import which

import scrapy
from scrapy.crawler import CrawlerProcess

import importlib
# from .crawlers.static_page import StaticPageSpider
# from .crawlers.static_page import StaticPageSpider
# from .crawlers.static_page import StaticPageSpider
from main.src.static_page import StaticPageSpider

def get_crawler_base_settings():
    """Returns scrapy base configurations."""
    return {
        "BOT_NAME": "crawlers",
        "SPIDER_MODULES": ["crawlers.spiders"],
        "NEWSPIDER_MODULE": "crawlers.spiders",
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 1,
        "SELENIUM_DRIVER_NAME": "chrome",
        "SELENIUM_DRIVER_EXECUTABLE_PATH": which("main/src/webdriver/chromedriver_win32_chr_81.exe"),
        # SELENIUM_DRIVER_ARGUMENTS: [],
        "SELENIUM_DRIVER_ARGUMENTS": ["--headless"],
        "DOWNLOADER_MIDDLEWARES": {"scrapy_selenium.SeleniumMiddleware": 0},
        "DOWNLOAD_DELAY": 1,
    }

def crawler_process(crawler_id, config):
    """Starts crawling."""
    # Redirects process logs to files
    sys.stdout = open(f"main/src/log/{crawler_id}.out", "a", buffering=1)
    sys.stderr = open(f"main/src/log/{crawler_id}_error.out", "a", buffering=1)

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

    process.start()

def gen_key():
    """Generates a unique key based on time and a random seed."""
    return str(int(time.time()*100)) + str((int(random.random() * 1000)))

def start_crawler(config):
    """Create and starts a crawler as a new process."""
    crawler_id = gen_key()
    print(os.getcwd())
    
    with open(f"main/src/config/{crawler_id}.json", "w+") as f:
        f.write(config)
    
    with open(f"main/src/flags/{crawler_id}.json", "w+") as f:
        f.write(config)

    # starts new process
    p = Process(target=crawler_process, args=(crawler_id, config))
    p.start()

    return crawler_id

def stop_crawler(crawler_id):
    """Sets the flags of a crawler to stop."""
    with open(f"main/src/flags/{crawler_id}.json", "w+") as f:
        f.write(json.dumps({"stop": True}))

if __name__ == '__main__':
    start_crawler(
        "{" +
        "  \"id\": 17," +
        "  \"source_name\": \"Di\u00e1rio Oficial de S\u00e3o Louren\u00e7o\"," +
        "  \"base_url\": \"https://saolourenco.mg.gov.br/poficiais.php\"," +
        "  \"obey_robots\": true," +
        "  \"antiblock\": \"ip\"," +
        "  \"ip_type\": \"tor\"," +
        "  \"proxy_list\": null," +
        "  \"max_reqs_per_ip\": 4," +
        "  \"max_reuse_rounds\": 3," +
        "  \"reqs_per_user_agent\": null," +
        "  \"user_agents_file\": null," +
        "  \"delay_secs\": null," +
        "  \"delay_type\": \"random\"," +
        "  \"cookies_file\": null," +
        "  \"persist_cookies\": false," +
        "  \"captcha\": \"none\"," +
        "  \"img_xpath\": null," +
        "  \"img_url\": null," +
        "  \"sound_xpath\": null," +
        "  \"sound_url\": null," +
        "  \"crawler_type\": \"static_page\"," +
        "  \"explore_links\": true," +
        "  \"link_extractor_max_depht\": 1," +
        "  \"link_extractor_allow\": \"(^https\\:\\/\\/saolourenco\\.mg\\.gov\\.br\\/poficiais\\.php|^https\\:\\/\\/saolourenco\\.mg\\.gov\\.br\\/arquivos\\/publicacaooficial\\/)\"" +
        "}"
    )

    # config = "{  \"id\": 17,  \"source_name\": \"Di\u00e1rio Oficial de S\u00e3o Louren\u00e7o\",  \"base_url\": \"https://saolourenco.mg.gov.br/poficiais.php\",  \"obey_robots\": true,  \"antiblock\": \"ip\",  \"ip_type\": \"tor\",  \"proxy_list\": null,  \"max_reqs_per_ip\": 4,  \"max_reuse_rounds\": 3,  \"reqs_per_user_agent\": null,  \"user_agents_file\": null,  \"delay_secs\": null,  \"delay_type\": \"random\",  \"cookies_file\": null,  \"persist_cookies\": false,  \"captcha\": \"none\",  \"img_xpath\": null,  \"img_url\": null,  \"sound_xpath\": null,  \"sound_url\": null,  \"crawler_type\": \"static_page\",  \"explore_links\": true,  \"link_extractor_max_depht\": 1,  \"link_extractor_allow\": \"(^https\\:\\/\\/saolourenco\\.mg\\.gov\\.br\\/poficiais\\.php|^https\\:\\/\\/saolourenco\\.mg\\.gov\\.br\\/arquivos\\/publicacaooficial\\/)\"}" 