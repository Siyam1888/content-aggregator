from flask import Flask
from flask import render_template, Response
from scraper import Scraper
import time
import json
from datetime import datetime
from threading import Thread


# creating the flask app
app = Flask(__name__, template_folder='./Templates')
updated_at = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
data = dict()


# scrapes the data and saves it to a json file
def scrape_data():
    global updated_at, data
    scraper = Scraper()
    data = scraper.scrape_all_news()
    # print('-' * 50, 'Scraper Ran', '-'*50)
    updated_at = datetime.now().strftime('%d/%m/%Y %H:%M:%S')


# infinite loop for scraping data with an interval
def scraper_loop():

    while True:
        scrape_data()
        time.sleep(60*60)


@app.route('/')
def home():
    return render_template('home.html', news=data, updated_at=updated_at)


@app.route('/api/news')
def run_scraper():
    data_json = json.dumps(data, ensure_ascii=False)
    return Response(data_json, mimetype='application/json')


# creating and starting the scraper loop thread
scraper_thread = Thread(target=scraper_loop)
scraper_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
    