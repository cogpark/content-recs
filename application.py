from flask import Flask, render_template, jsonify
from title_evaluator import TitleEvalutor
from web_scraper import WebScraper

application = Flask(__name__)

@application.route("/")
def index():
    return render_template('index.html')

@application.route("/api/content-recs/<url>", methods=['GET'])
def get_title_recs(url):
    
    # If you submit strings w/ "/" in them, it messes up the routing, e.g. flask thinks you are trying to submit a request to /api/content-recs/www.mass.gov/net-metering
    url = url.replace('|','/')
    
    print(f'URL as entered by user: {url}')

    ws = WebScraper()
    title = ws.get_title(url)

    print(f'Title returned: {title}')

    te = TitleEvalutor()
    evaluation = te.evaluator(title, url)
    print(evaluation)

    return jsonify(evaluation)