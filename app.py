import time

import redis
from flask import Flask, render_template

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def generateStub(title, contents):
    S  = "<!DOCTYPE html>\n"
    S += "<html>\n"
    S += "  <head>\n"
    S += f"    <title>{title}</title>\n"
    S += "  </head>\n"
    S += "  <body>\n"
    S += "     <a href='/help'>help</a>\n"
    S += "     <a href='/'>back</a>\n"
    S += f"     <h1>{title}</h1>\n"
    S += f"     {contents}\n"
    S += "  </body>\n"
    S += "</html>\n"
    return S

@app.route('/')
def mainpage():
    lis = "<ol>\n"
    lis += "         <li><a href='/help'>help</a></li>\n"
    lis += "         <li><a href='/hello'>hello</a></li>\n"
    lis += "     </ol>"
    return generateStub("Main Page", lis)

@app.route('/help')
def help_page():
    return generateStub("Be Cool!", "<p>Everything's fine! Be cool!</p>")

@app.route('/hello/')
@app.route('/hello/<name>')
@app.route('/hello/<name>/')
def hello(name=None):
    return render_template("hello.html", name=name)

