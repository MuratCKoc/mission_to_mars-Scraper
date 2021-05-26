from flask import Flask, render_template, jsonify
from werkzeug.utils import redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape_data
from config import username, password

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb+srv://"+username+":"+password +
                "@cluster0.ow6cz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

@app.route('/')
def index():
    mars_data = mongo.db.mars_db.find_one()
    print(mars_data)
    return render_template('index.html', mars_mission=mars_data)


@app.route('/scrape')
def data_scrape():

    mars_data = scrape_data()
    print(mars_data)
    # Update Mongo database
    mongo.db.mars_db.update({}, mars_data, upsert=True)
    # Redirect to index
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)

