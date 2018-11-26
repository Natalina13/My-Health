from __future__ import print_function
import boto3
import decimal
from flask import Flask
from flask import request
from flask import render_template, flash
from boto3.dynamodb.conditions import Key, Attr
import os
import base64

import boto3

app = Flask(__name__)

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

key = "hello"

@app.route('/')
def index():
    return render_template("UserLogin.html")


@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form['Username']
    password = request.form['Password']
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://dynamodb.us-west-2.amazonaws.com")
    table = dynamodb.Table('User')
    response = table.scan()
    username_plain = []
    password_plain = []
    for r in response['Items']:
        u = decode(key, r['UserName'])
        p = decode(key, r['Password'])
        username_plain.append(u)
        password_plain.append(p)
    if username in username_plain:
        if password in password_plain:
            return render_template("Dashboard.html")
        else:
            return render_template("UserLogin.html")
    else:
        return render_template("UserLogin.html")

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
    uname = request.form['Username']
    username = encode(key, uname)
    pword = request.form['password']
    password = encode(key, pword)

    print("fName:", fname)
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://dynamodb.us-west-2.amazonaws.com")

    table = dynamodb.Table('User')
    table.put_item(
        Item={
            'UserName': username,
            'Password': password,
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
    )
    return render_template("UserLogin.html")

app.secret_key = os.urandom(24)
app.debug = True
app.run()
app.run(debug=True)
