# Setup
1. python -m venv venv
1. venv\Scripts\activate
1. pip install -r requirements.txt

# running the app
1. Start poweshell. Your prompt should look like: C:\Users\mii24_000
1. cd content-recs
1. venv\Scripts\activate
1. $env:FLASK_APP='application.py'
1. flask run
1. to stop the webserver, control + c (twice)
1. to start it again, flask run (you only need to do the other stuff if you close powershell)