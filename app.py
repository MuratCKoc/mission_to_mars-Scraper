from flask import Flask, render_template, jsonify
from werkzeug.utils import redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape_data
from config import username, password

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb+srv://"+username+":"+password +
                "@cluster0.ow6cz.mongodb.net/mars_db?retryWrites=true&w=majority")

@app.route('/')
def index():
    mars_data = {}
    collections_ = mongo.db.list_collection_names()
    #print(mars_data)
    print(collections_)
    print(mongo.db)
    print(mongo.db.list_collection_names())
    for col_ in collections_:
        mars_data[col_] = list(mongo.db[col_].find())
    #mars_data['news'] = list(mongo.db['news'].find())
    print(mars_data.keys())
    print(mars_data['news'][0]['title'])
    #print(mars_data.news)
    return render_template('index.html', mars_mission=mars_data)


@app.route('/scrape')
def data_scrape():

    mars_data = scrape_data()
    print(mars_data)
    # Update Mongo database
    #mongo.db.update({}, mars_data, upsert=True)
    # Redirect to index
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)

