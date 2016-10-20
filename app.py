from flask import Flask, render_template, request, abort, redirect, url_for
import json
from Client import *
app = Flask(__name__)

@app.route("/")
def index():
    return 'Hello World !'

if __name__ == "__main__":
    app.run('192.168.33.22', debug=True)
