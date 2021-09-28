from flask import Flask, render_template, redirect
from challenge import scrape
import pymongo

app = Flask(__name__)

# create a connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# define the travel_db database in Mongo
db = client.mars_db

@app.route("/scrape")
def scrape_mars_data():
    mars_collection = scrape()
    
    db.mars.update({}, mars_collection, upsert=True)
    # redirect this back to the main page
    return redirect("/")

@app.route("/")
def home():
    mars_info = db.mars.find_one()
    return render_template('index.html', mars_info=mars_info)

if __name__ == "__main__":
    app.run(debug=True)
    # db.mars.delete_one({})
    # mars_collection = scrape()
    # db.mars.insert_one(mars_collection)