import requests
from bs4 import BeautifulSoup
import random


class Scraper:
    """
    Contain all the functions for scraping selected news websites.
    """

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
            "kalerkantha": "https://www.kalerkantho.com/print-edition/first-page",
            "prothomalo": "https://www.prothomalo.com/",
        }

    # sends a request and returns a response
    def get_response(self, url):
        """Take an url, send a request and return the response."""

        session = requests.Session()
        HEADER = {
            "User-Agent": random.choice(self.headers_list),
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Language": "bn",
        }
        session.headers.update(HEADER)
        response = session.get(url)
        return response

    # Scrapes kalerkantha
    def scrape_kalerkantha(self):
        """Scrape the newspaper website Daily Kalerkantha."""

        response = self.get_response(self.news_urls["kalerkantha"])
        if response:
            soup = BeautifulSoup(response.content, "lxml")

            # Top news
            top_news_div_grp = soup.find("div", {"class": "col-xs-12 top_news"})
            top_news_div = top_news_div_grp.find(
                "div", {"class": "col-xs-12 col-sm-12 col-md-6 summary"}
            )
            top_news = {
                "headline": top_news_div.a.text,
                "link": top_news_div.a.attrs["href"],
                "summary": top_news_div.p.text,
            }

            # Mid news
            mid_news_div_grp = soup.find("div", {"class": "col-xs-12 mid_news"})
            mid_news_divs = mid_news_div_grp.findAll(
                "div", {"class": "col-xs-12 col-sm-6 col-md-6 n_row"}
            )

            news_list = [top_news]

            # adding the mid news to the list
            for div in mid_news_divs:
                news = {
                    "headline": div.a.text,
                    "link": div.a.attrs["href"],
                    "summary": div.p.text,
                }
                news_list.append(news)

            return news_list

    # Scrapes Protham Alo
    def scrape_prothomalo(self):
        """Scrape the newspaper website Daily Pratham Alo."""

        # List containing the news
        news_list = []

        # Taking the response and parsing it
        response = self.get_response(self.news_urls["prothomalo"])
        soup = BeautifulSoup(response.content, "lxml")

        # Scraping the primary headline
        primary_news_div = soup.find("div", {"class": "organism1-m__text__1Qbhv"})
        primary_news_headline_a = primary_news_div.find(
            "a", {"class": "newsHeadline-m__title-link__1puEG"}
        )
        primary_news_summary_a = primary_news_div.find("a", {"class": ""})
        primary_news = {
            "headline": primary_news_headline_a.text,
            "link": primary_news_headline_a.attrs["href"],
            "summary": primary_news_summary_a.text,
        }
        news_list.append(primary_news)

        # Other news scraping
        news_with_no_image_div = soup.findAll("div", {"class": "news_with_no_image"})
        for div in news_with_no_image_div:
            headline_a = div.find("a", {"class": "newsHeadline-m__title-link__1puEG"})
            summary_a = div.find("a", {"class": ""})
            news = {
                "headline": headline_a.text,
                "link": headline_a.attrs["href"],
                "summary": summary_a.text,
            }
            news_list.append(news)

        return news_list

    def scrape_jugantor(self):
        """Scrape the newspaper website Daily Jugantor."""

        pass

    def scrape_dailystar(self):
        """Scrape the newspaper website Daily Star."""

        pass

    def scrape_dailysun(self):
        """Scrape the newspaper website Daily Sun."""

        pass


if __name__ == "__main__":
    s = Scraper()
    print(s.scrape_prothomalo())
