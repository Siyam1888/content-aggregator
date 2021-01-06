import requests
from bs4 import BeautifulSoup
import random


class Scraper:
    def __init__(self):
        self.headers_list = [
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13",
            "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201",
            "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
            "Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone9,1;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]",
        ]

        self.news_urls = {
            "kalerkantha": "https://www.kalerkantho.com/print-edition/first-page"
        }

    def get_response(self, url):
        session = requests.Session()
        HEADER = {
            "User-Agent": random.choice(self.headers_list),
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Language": "bn",
        }
        session.headers.update(HEADER)
        response = session.get(url)
        return response

    def scrape_kalerkantha(self):
        response = self.get_response(self.news_urls["kalerkantha"])
        soup = BeautifulSoup(response.content, "html.parser")
        top_news_div = soup.find("div", {"class": "col-xs-12 top_news"})
        mid_news_div = soup.find("div", {"class": "col-xs-12 mid_news"})
