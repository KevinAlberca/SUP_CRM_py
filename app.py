from flask import Flask, render_template, request, abort, redirect, url_for
import json
from Client import *
app = Flask(__name__)
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

BASE_GS_URL = "https://docs.google.com/spreadsheets/d/"

# When you want to open a Google Sheet, you have to share with the e-mail in your credential.json
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('MyCRM_StupidCredentials.json', scope)


# Dictionnary contains every customers added with createCustomer method
# customers = []
customers = [{"company": "ChnewCompany", "state": "prospect", "firstname": "Chi", "lastname": "Noa"}, {"company": "AwH", "state": "partner", "firstname": "K", "lastname": "A"}]

@app.route("/")
def index():
    # Return possibles action for the API
    actions = {
        "/list" : "[GET] List of all customers",
        "/create" : "[POST] Create a customer in HTTP POST method",
        "/view/:value:/:action:" : "[GET] Take a look on a customer, searched by his :action:",
        "/save" : "[GET] Save your customers list on a local file",
        "/save/:google_spread_sheet:" : "[GET] Save your customers list on a Google SpeadSheet",
    }
    return json.dumps(actions)

@app.route("/list", methods=['GET'])
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

@app.route('/save/<string:spreadsheet_id>', methods=['GET'])
def saveInSpreadSheet(spreadsheet_id):
    c = gspread.authorize(credentials)
    gs = c.open_by_key(spreadsheet_id)

    wks_width = len(customers[0])
    wks_height = len(customers)
    today = str(datetime.datetime.today())

    wks = gs.add_worksheet(title=today, rows=wks_height, cols=wks_width)
    wks.append_row(customers[0].keys())

    if wks != None:
        for key, customer in enumerate(customers):
            wks.append_row(customer.values())
    else :
        return json.dumps('Error : The worksheet already exists')

    return True

if __name__ == "__main__":
    app.run('192.168.33.22', debug=True)
