import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import requests
import json

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def hello():

	if request.method == 'GET':
		return render_template('hello.html')
	if request.method == 'POST':
		q = request.form['query']
		r = requests.get('https://api.github.com/search/issues?q=' + q)
		j = r.json()
		# urls = [ a["url"] for a in j["items"] ]
		return render_template('layout.html', items=j["items"])
	return "Hello!"
