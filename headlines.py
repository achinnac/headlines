import feedparser
from flask import Flask, render_template
from flask import request
import json
import urllib.request
import urllib.parse

app = Flask(__name__)

# BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"
# API_KEY = "ff2e26de65de614be51a7ce6364396a3"

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'rt': 'http://feeds.reuters.com/reuters/technologyNews',
             'abc': 'https://abcnews.go.com/abcnews/topstories'}

@app.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("London, UK")
    return render_template("home.html", articles=feed['entries'], weather=weather)

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&unit=metric&appid=ff2e26de65de614be51a7ce6364396a3"
    query = urllib.parse.quote(query)
    url = api_url.format(query)

    # print(query)
    # print(url)

    data = urllib.request.urlopen(url).read().decode("utf8")
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                    parsed["weather"][0]["description"],
                    "temperature":parsed["main"]["temp"],
                    "city":parsed["name"]}
        return weather

if __name__ == "__main__":
    app.run(port=5000, debug=True)