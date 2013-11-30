import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
import requests
import json
import re
import sys

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
	token = request.cookies.get("access_token")
	if request.method == 'GET':
		return render_template('hello.html')
	if request.method == 'POST':
		q = request.form['query']
		r = requests.get('https://api.github.com/search/issues?access_token=' + token + '&q=' + q)
		j = r.json()
		# urls = [ a["url"] for a in j["items"] ]
		items=[]
		i = 1
		for item in j["items"]:
			i = i + 1;
			if i < 3:
				cut_prefix = re.sub("^https://github.com/", "", item["html_url"])
				[user, repo_url, _] = cut_prefix.split("/", 2)
				repo = requests.get('https://api.github.com/repos/' + user + "/" + repo_url + '?access_token=' + token).json()
				# return 
				items.append(dict({'description': repo["description"], "html_url": item["html_url"]}))
			else: 
				items.append(dict({'description': "sample_desc", "html_url": item["html_url"]}))
		return render_template('layout.html', items=j["items"])
	return "Hello!"


@app.route('/login')
def login():
	return redirect("https://github.com/login/oauth/authorize?client_id=c0eade59a21038cda641")

@app.route('/authorise')
def authorise():
	code = request.args.get('code', '')
	# headers = {'content-type': 'application/json'}
	r = requests.post("https://github.com/login/oauth/access_token", 
		data={"client_id": "c0eade59a21038cda641", "client_secret": "ac9c1d3856d9cf53135af23245aaa86fb92ced79", "code": code}
		# , headers=headers
		)
	# token = "aa"
	# token = request.args.get('access_token', r.json()["access_token"])
	token = r.text.split("&", 1)[0].split("=")[1]
	# sys.stderr.write(headers["content-type"])
	resp = make_response(redirect(url_for('hello')))
	resp.set_cookie("access_token", token)
	return resp 

