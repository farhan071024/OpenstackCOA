import smtplib

import json
import requests
from flask import Flask, render_template, flash, request,jsonify,redirect,url_for



# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

sourceip='10.245.135.69:9095'

SERVER = "localhost"
FROM = "root@mydomain.com"

TO = [] # must be a list

SUBJECT = "Malware Alert"


@app.route("/email/<emailid>/<malwaretype>")
def email(emailid,malwaretype):
	TO.append(emailid)
	TEXT = malwaretype +" has been deteced! Use cautions!"

	# Prepare actual message
	message = """\
	From: %s
	To: %s
	Subject: %s
	%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

	# Send the mail

	server = smtplib.SMTP(SERVER)
	server.sendmail(FROM, TO, message)
	server.quit()
	return "done"

app.run(host='192.170.0.11',port= 9095)
