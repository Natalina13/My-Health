from __future__ import print_function # Python 2/3 compatibility
import boto3
import decimal
from flask import Flask
from flask import request
from flask import render_template,flash
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from flask.ext.api import status
import boto3

app = Flask(__name__)

@app.route('/')
def index():
   return render_template("UserLogin.html")

@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form['Username']
    password = request.form['Password']

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://dynamodb.us-west-2.amazonaws.com")
    table = dynamodb.Table('User')

    try:
        response = table.get_item(
            Key={
                'UserName': username,
                'Password': password
            }
        )
    except KeyError:
        error = 'Invalid credentials'
        render_template('UserLogin.html', error=error)
    else:

        if(status.is_success(response.status_code))
            item = response['Item']
        else:
            render_template('UserLogin.html', error=error)
    return render_template("dashboard.html")

@app.route('/registerUser', methods=['POST'])
def register_user():
    fname = request.form['fName']
    lname = request.form['lName']
    eid = request.form['EId']
    age = request.form['age']
    height = request.form['height']
    weight = request.form['Weight']
    demailid = request.form['dEmailId']
    familyid = request.form['FamilyId']
    secretcode = request.form['secretCode']
    cid = request.form['cId']
    username = request.form['Username']
    secretcode = request.form['secretCode']
    password = request.form['password']

    print("fName:",  fname)
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://dynamodb.us-west-2.amazonaws.com")

    table = dynamodb.Table('User')
    table.put_item(
           Item={
               'UserName': username,
               'Password': password,
               'info': {
                   'FirstName': fname,
                   'LastName': lname,
                   'EmailId': eid,
                   'Age': age,
                   'Height': height,
                   'Weight': weight,
                   'DoctEmailId': demailid,
                   'FamilyEId': familyid,
                   'SecretCode': secretcode,
                   'ClientId': cid
               }
            }
        )
    return render_template("UserLogin.html")

app.debug = True
app.run()
app.run(debug = True)