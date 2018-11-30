from __future__ import print_function
import boto3
import decimal
from flask import Flask, session
from flask import request
from flask import render_template, flash
from boto3.dynamodb.conditions import Key, Attr
import os
import base64
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets

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

key = "----"

@app.route('/')
def index():
    return render_template("UserLogin.html")


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    username = request.form['Username']
    password = request.form['Password']
    session['uname'] = username
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

@app.route('/sendemail', methods=['GET', 'POST'])
def sendemail():
    username = encode(key, session.get('uname', None))
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://dynamodb.us-west-2.amazonaws.com")
    table = dynamodb.Table('User')
    response = table.query(
        KeyConditionExpression=Key('UserName').eq(username)
    )
    for i in response['Items']:
        doctemail = i['DoctEmailId']
        familyemail = i['FamilyEId']
        token = i['Token']
        SENDERNAME = i['FirstName']
    SENDER = '------'
    recip = []
    recip.append(doctemail)
    recip.append(familyemail)
    USERNAME_SMTP = "-----"
    PASSWORD_SMTP = "------"
    HOST = "email-smtp.us-west-2.amazonaws.com"
    PORT = 587
    SUBJECT = str(SENDERNAME)+' view My Dashboard'
    BODY_TEXT = ("My Health Dashboard")
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>My Health Dashboard</h1>
      <p>
      Username: """+str(username)+"""</br>
      Link: <a href='http://127.0.0.1:5000/closedashboard1'>"""+str(username)+""" Dashboard's link </a></br>
      Token: """+str(token)+"""
        </p>
    </body>
    </html>
                """
    for RECIPIENT in recip:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
        msg['To'] = RECIPIENT
        part1 = MIMEText(BODY_TEXT, 'plain')
        part2 = MIMEText(BODY_HTML, 'html')
        msg.attach(part1)
        msg.attach(part2)
        try:
            server = smtplib.SMTP(HOST, PORT)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(USERNAME_SMTP, PASSWORD_SMTP)
            server.sendmail(SENDER, RECIPIENT, msg.as_string())
            server.close()
        except Exception as e:
            print("Error: ", e)
    return render_template("Dashboard.html")

@app.route('/closedashboard1', methods=['Get'])
def closedashboard1():
    return render_template("Closelogin.html")

@app.route('/closedashboard', methods=['Post'])
def closedashboard():
    username = request.form['Username']
    email = request.form['Email']
    token = request.form['Token']
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2',
                              endpoint_url="http://dynamodb.us-west-2.amazonaws.com")
    table = dynamodb.Table('User')
    response = table.scan()
    u=[]
    e=[]
    t=[]
    for r in response['Items']:
        u.append(r['UserName'])
        e.append(r['DoctEmailId'])
        e.append(r['FamilyEId'])
        t.append(r['Token'])
    if username in u:
        if email in e:
            if token in t:
                return render_template("Dashboard1.html")
            else:
                return render_template("Closelogin.html")
        else:
            return render_template("Closelogin.html")
    else:
        return render_template("Closelogin.html")


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
    token = secrets.token_urlsafe(16)

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
            'ClientId': cid,
            'Token': token
        }
    )
    return render_template("UserLogin.html")

app.secret_key = os.urandom(24)
app.debug = True
app.run()
app.run(debug=True)
