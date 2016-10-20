from flask import Flask, render_template, request, abort, redirect, url_for
import json
from Client import *
app = Flask(__name__)

# Dictionnary contains every customers added with createCustomer method
customers = []

@app.route("/")
def index():
    return 'Hello World !'

@app.route("/list")
def listCustomer():
    return json.dumps(customers)

@app.route('/create', methods=['POST'])
def createCustomer():
    # Send data in POST method
    if request.method == 'POST':
        customers.append(request.form)
    return json.dumps(customers)

if __name__ == "__main__":
    app.run('192.168.33.22', debug=True)
