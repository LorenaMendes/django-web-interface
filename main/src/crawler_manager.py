import json
import time
import random

def gen_random_key():
    return str(int(time.time()*100)) + str((int(random.random() * 1000)))

def start_crawler(config):
    crawler_id = gen_random_key()
    with open(f"crawlers/config/{crawler_id}_config.json", "w+") as f:
        f.write(json.dumps(config, indent=2))
    
    

    return crawler_id

def stop_crawler(cofing):
    pass


if __name__ == '__main__':
    print(start_crawler({
        "url": {"url":"https://saolourenco.mg.gov.br/poficiais.php", "type": "simple"},
        "crawler_type": "static_page",
        "link_extractor": {"allow": "(^https\:\/\/saolourenco\.mg\.gov\.br\/poficiais\.php|^https\:\/\/saolourenco\.mg\.gov\.br\/arquivos\/publicacaooficial\/)"}
    }))