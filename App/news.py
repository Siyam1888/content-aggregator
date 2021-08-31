from flask import Flask
from flask import render_template, Response
import json


# creating the flask app
app = Flask(__name__, template_folder='./Templates')


def get_data():
    with open('App/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        updated_at = data.get('updated_at')
        del data['updated_at']
    return (data, updated_at)


@app.route('/')
def home():
    data, updated_at = get_data()
    return render_template('home.html', news=data, updated_at=updated_at)


@app.route('/sources')
def sources():
    data, updated_at = get_data()
    source_list = [data[source]["info"] for source in data]
    return render_template('sources.html', source_list=source_list)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api/news')
def api():
    data, updated_at = get_data()
    data_json = json.dumps(data, ensure_ascii=False)
    return Response(data_json, mimetype='application/json')



if __name__ == '__main__':
    app.run()
    