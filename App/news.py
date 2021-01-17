from flask import Flask
from flask import render_template, jsonify
from scraper import Scraper
import json

with open('data.json', 'r+', encoding='utf-8') as f:
    scraper = Scraper()
    if not f.read():
        data = scraper.scrape_all_news()
        json.dump(data, f, ensure_ascii=False)
        print('SCRAPER RAN...\a', '*'*100)


app = Flask(__name__)

@app.route('/')
def home():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('home.html', news=data)


if __name__ == '__main__':
    app.run(debug=True)