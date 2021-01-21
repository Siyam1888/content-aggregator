from flask import Flask
from flask import render_template, Response
from scraper import Scraper
import time
import json
from pytz import timezone
from datetime import datetime
from threading import Thread


# creating the flask app
app = Flask(__name__, template_folder='./Templates')
bst = timezone('ASIA/DHAKA')
updated_at = datetime.now(bst).strftime('%d/%m/%Y %H:%M:%S')
data = dict()


# scrapes the data and saves it to a json file
def scrape_data():
    global updated_at, data
    scraper = Scraper()
    data = scraper.scrape_all_news()
    updated_at = datetime.now(bst).strftime('%d/%m/%Y %H:%M:%S')


# infinite loop for scraping data with an interval
def scraper_loop():

    while True:
        scrape_data()
        time.sleep(60*60)




@app.route('/')
def home():
    return render_template('home.html', news=data, updated_at=updated_at)


@app.route('/sources')
def sources():
    source_list = [data[source]["info"] for source in data]
    return render_template('sources.html', source_list=source_list)

@app.route('/api/news')
def api():
    data_json = json.dumps(data, ensure_ascii=False)
    return Response(data_json, mimetype='application/json')


# creating and starting the scraper loop thread
scraper_thread = Thread(target=scraper_loop)
scraper_thread.start()

if __name__ == '__main__':
    app.run()
    