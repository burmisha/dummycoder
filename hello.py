import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
import requests
import json
import re
from urllib import urlencode
from collections import OrderedDict

app = Flask(__name__)
app.debug = True

def sanitize(value):
	if value:
		return value
	else:
		return ""

@app.route('/', methods=['GET', 'POST'])
def hello():
	# token = request.cookies.get("access_token")
	token = "97ae087c18351e1b53a41a5f3779413bd020f32c"
	q = ""
	if request.method == 'GET':
		return render_template('hello.html')
	if request.method == 'POST':
		params = OrderedDict()
		params["q"] = request.form["query"]
		params["language"] = request.form["language"]
		params["access_token"] = token
		j = requests.get('https://api.github.com/search/issues', params=urlencode(params)).json()
		issues=[]
		i = 1
		for item in j["items"]:
			i = i + 1;
			cut_prefix = re.sub("^https://github.com/", "", item["html_url"])
			[user, repo_url, _] = cut_prefix.split("/", 2)
			issue = dict()
			issue["html_url"] = item["html_url"]			
			issue["body"] = item["body"]
			issue["title"] = item["title"]
			issue["created_at"] = item["created_at"]
			if i < 4:
				params = OrderedDict()
				params["access_token"] = token
				repo = requests.get('https://api.github.com/repos/' + user + "/" + repo_url, 
									 params=urlencode(params)).json()
				issue["description"] = sanitize(repo["description"])
				issue["homepage"] = sanitize(repo["homepage"])
			issues.append(issue)
		return render_template('layout.html', issues=issues, q=q)
	return "Hello!"


@app.route('/login')
def login():
	return redirect("https://github.com/login/oauth/authorize?client_id=c0eade59a21038cda641")

@app.route('/authorise')
def authorise():
	params = OrderedDict()
	params["client_id"] = "c0eade59a21038cda641"
	params["client_secret"] = "ac9c1d3856d9cf53135af23245aaa86fb92ced79"
	params["code"] = request.args.get('code', '')
	r = requests.post("https://github.com/login/oauth/access_token", params=urlencode(params))
	token = r.text.split("&", 1)[0].split("=")[1]
	resp = make_response(redirect(url_for('hello')))
	resp.set_cookie("access_token", token)
	return resp 

