import json
import time
import random
import os

def gen_random_key():
    return str(int(time.time()*100)) + str((int(random.random() * 1000)))

def start_crawler(config):
    crawler_id = gen_random_key()
    with open(f"crawlers/config/{crawler_id}_config.json", "w+") as f:
        f.write(json.dumps(config, indent=2))
    
    start = f"nohup scrapy crawl static_page -a crawler_id={crawler_id}"
    redirect_output = f"> log/{crawler_id}.txt 2>&1"
    get_pid = f"& echo $! > crawler_pid/{crawler_id}.txt"

    command = start + redirect_output + get_pid

    return (command, crawler_id)

def stop_crawler(crawler_id):
    kill = f"kill -9 `cat crawler_pid/{crawler_id}.txt`"
    rm_file = "rm crawler_pid/{crawler_id}.txt"
    return (kill, rm_file)

if __name__ == '__main__':
    print(start_crawler({
        "url": {
            "url": "https://saolourenco.mg.gov.br/poficiais.php",
            "type": "simple"
        },
        "crawler_type": "static_page",
        "link_extractor": {
            "allow": [
            "^https\\:\\/\\/saolourenco\\.mg\\.gov\\.br\\/poficiais\\.php",
            "^https\\:\\/\\/saolourenco\\.mg\\.gov\\.br\\/arquivos\\/publicacaooficial\\/"
            ]
        }
    }))
