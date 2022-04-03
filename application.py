from flask import Flask, render_template, jsonify
from title_evaluator import TitleEvalutor

application = Flask(__name__)


print("starting")

@application.route("/")
def index():
    return render_template('index.html')

@application.route("/api/content-recs/<url>", methods=['GET'])
def get_title_recs(url):
    
    print("hi!")
    #TODO use beautiful soup to get the page and get the title attribute 
    print(url)
    te = TitleEvalutor()
    evaluation = te.evaluator(url)
    print(evaluation)

    return jsonify(evaluation)