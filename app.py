from flask import Flask, render_template, request, abort, redirect, url_for
import json
from Client import *
app = Flask(__name__)

# Dictionnary contains every customers added with createCustomer method
customers = []

@app.route("/")
def index():
    print(crmSheet)
    # Return possibles action for the API
    actions = {
        "/list" : "[GET] List of all customers",
        "/create" : "[POST] Create a customer in HTTP POST method",
        "/view/:value:/:action:" : "[GET] Take a look on a customer, searched by his :action:",
        "/save" : "[GET] Save your customers list on a local file",
        "/save/:google_spread_sheet:" : "[GET] Save your customers list on a Google SpeadSheet",
    }

    return json.dumps(actions)

@app.route("/list")
def listCustomer():
    return json.dumps(customers)

@app.route('/create', methods=['POST'])
def createCustomer():
    # Send data in POST method
    if request.method == 'POST':
        customers.append(request.form)
    return json.dumps(customers)

@app.route('/view/<string:value>/<string:action>', methods=['GET'])
def getClientsByValueWithAction(value, action):
    c = []
    for customer in customers:
        if action in customer.keys():
            if customer[action] == value:
                c.append(customer)
    return json.dumps(c)
if __name__ == "__main__":
    app.run('192.168.33.22', debug=True)
