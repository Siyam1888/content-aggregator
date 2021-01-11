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
            "Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre",
        ]

        self.news_urls = {
            "kalerkantho": "https://www.kalerkantho.com/print-edition/first-page",
            "prothomalo": "https://www.prothomalo.com/",
            "dailystar": "https://www.thedailystar.net/newspaper",
            "jugantor": "https://www.jugantor.com/todays-paper/first-page",
            "bd-pratidin": "https://www.bd-pratidin.com/first-page",
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

    # Scrapes kalerkantho
    def scrape_kalerkantho(self):
        """Scrape the newspaper website Daily kalerkantho."""

        response = self.get_response(self.news_urls["kalerkantho"])
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

    # Scrapes The Daily Jugantor
    def scrape_jugantor(self):
        """Scrape the newspaper website Daily Jugantor."""

        news_list = []
        response = self.get_response(self.news_urls["jugantor"])
        soup = BeautifulSoup(response.content, "lxml")
        lead_news = soup.find("div", {"id": "lead-news"})
        a_tags = lead_news.findAll("a")

        for a in a_tags:
            news = {
                "headline": a.text.strip(),
                "link": a.attrs["href"],
                "summary": a.text.strip() + "...",
            }
            news_list.append(news)

        return news_list

    # Scrapes The Daily Star
    def scrape_dailystar(self):
        """Scrape the newspaper website Daily Star."""

        news_list = []
        response = self.get_response(self.news_urls["dailystar"])
        soup = BeautifulSoup(response.content, "lxml")
        news_divs = soup.findAll("div", {"class": "list-content"})

        for div in news_divs[:5]:
            news_list.append(
                {
                    "headline": div.a.text,
                    "link": div.a.attrs["href"],
                    "summary": div.p.text,
                }
            )

        return news_list

    # scrapes the first page of Bangladesh Pratidin news paper
    def scrape_bd_pratidin(self):
        """Scrape the newspaper website Bangladesh Pratidin."""

        news_list = []
        response = self.get_response(self.news_urls["bd-pratidin"])
        soup = BeautifulSoup(response.content, "lxml")

        lead_news_div = soup.find("div", {"class": "lead-news-2nd"})
        link = lead_news_div.a.attrs["href"]
        link = (
            "https://www.bd-pratidin.com/" + link
            if not link.startswith("http")
            else link
        )
        lead_news = {
            "headline": lead_news_div.span.text,
            "link": link,
            "summary": lead_news_div.p.text,
        }
        news_list.append(lead_news)

        secondary_news_divs = soup.find("div", {"class": "lead-news-3nd"}).findAll(
            "div", {"class": "news-row"}
        )
        for div in secondary_news_divs[:4]:
            headline = div.span.text
            link = div.a.attrs["href"]
            link = (
                "https://www.bd-pratidin.com/" + link
                if not link.startswith("http")
                else link
            )
            summary = div.span.text

            news = {"headline": headline, "link": link, "summary": summary}
            news_list.append(news)

        return news_list

    # runs all the scrapers and stores the values in a dictionary
    def scrape_all_news(self):
        pass


if __name__ == "__main__":
    s = Scraper()
    print(s.scrape_bd_pratidin())
