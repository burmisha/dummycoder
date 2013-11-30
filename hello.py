import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
import requests
import json
import re
import sys
from urllib import urlencode
from collections import OrderedDict

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def hello():
	# token = request.cookies.get("access_token")
	token = "97ae087c18351e1b53a41a5f3779413bd020f32c"
	q=""
	if request.method == 'GET':
		return render_template('hello.html')
	if request.method == 'POST':
		p = OrderedDict()
		p["q"] = request.form["query"]
		p["language"] = request.form["language"]
		p["access_token"] = token
		r = requests.get('https://api.github.com/search/issues', params=urlencode(p))
		j = r.json()
		# q = j
		issues=[]
		i = 1
		for item in j["items"]:
			i = i + 1;
			if i < 4:
				cut_prefix = re.sub("^https://github.com/", "", item["html_url"])
				[user, repo_url, _] = cut_prefix.split("/", 2)
				repo = requests.get('https://api.github.com/repos/' + user + "/" + repo_url + '?access_token=' + token).json()
				issue = dict()
				issue["description"] = repo["description"]
				issue["html_url"] = item["html_url"]
				issue["homepage"] = repo["homepage"]
				issues.append(issue)
			else: 
				issues.append(dict({'description': "sample_desc", "html_url": item["html_url"]}))
		return render_template('layout.html', items=issues, q=q)
	return "Hello!"


@app.route('/login')
def login():
	return redirect("https://github.com/login/oauth/authorize?client_id=c0eade59a21038cda641")

@app.route('/authorise')
def authorise():
	code = request.args.get('code', '')
	r = requests.post("https://github.com/login/oauth/access_token", 
		data={"client_id": "c0eade59a21038cda641", "client_secret": "ac9c1d3856d9cf53135af23245aaa86fb92ced79", "code": code}
		)
	token = r.text.split("&", 1)[0].split("=")[1]
	resp = make_response(redirect(url_for('hello')))
	resp.set_cookie("access_token", token)
	return resp 

