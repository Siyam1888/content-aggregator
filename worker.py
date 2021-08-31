from scraper import Scraper
import json
from datetime import datetime
from pytz import timezone
import time


def main():
    """Update the news json file"""
    scraper = Scraper()
    data = scraper.scrape_all_news()

    bst = timezone('ASIA/DHAKA')
    data["updated_at"] = datetime.now(bst).strftime('%d/%m/%Y %H:%M:%S')

    with open('App/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    
    print(f"Scraper at {data['updated_at']}")


if __name__ == '__main__':
    while True:
        main()
        time.sleep(120)