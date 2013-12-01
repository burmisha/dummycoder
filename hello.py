import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
import requests
import json
import re
from urllib import urlencode
from collections import OrderedDict

import time
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
	token = "978ca3a1c15d3ca0dc6789f30bc5bf2b45f3ffee"
	q = ""
	logged_in = sanitize(request.cookies.get("logged_in"))
	user = sanitize(request.cookies.get("user"))
	if request.method == 'GET':
		return render_template('hello.html', logged_in=logged_in)
	if request.method == 'POST':
		params = OrderedDict()
		params["q"] = request.form["query"]
		params["language"] = request.form["language"]
		if token: 
			params["access_token"] = token
		j = requests.get('https://api.github.com/search/issues', params=urlencode(params)).json()
		issues=[]
		i = 1
		for item in j["items"]:
			i = i + 1;
			cut_prefix = re.sub("^https://github.com/", "", item["html_url"])
			[repo_user, repo_name, _] = cut_prefix.split("/", 2)
			issue = dict()
			issue["html_url"] = item["html_url"]			
			issue["body"] = item["body"]
			issue["title"] = item["title"]
			created_at = time.strptime(item["created_at"], "%Y-%m-%dT%H:%M:%SZ")
			issue["created_at"] = time.strftime("%B %d, %Y %H:%M", created_at)
			issue["repo_name"] = repo_name
			issue["repo_user"] = repo_user
			if i < 4:
				params = OrderedDict()
				if token:
					params["access_token"] = token
				repo = requests.get('https://api.github.com/repos/' + repo_user + "/" + repo_name, 
									 params=urlencode(params)).json()
				issue["description"] = sanitize(repo["description"])
				issue["homepage"] = sanitize(repo["homepage"])
			issues.append(issue)
		return render_template('layout.html', issues=issues, q=q, user=user)
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
	resp.set_cookie("logged_in", "yes")

	params = OrderedDict()
	if token: 
		params["access_token"] = token
	user = requests.get('https://api.github.com/user', params=urlencode(params)).json()
	resp.set_cookie("user", user["login"])
	return resp 

@app.route('/logout')
def logout():
	# token = request.cookies.get("access_token")
	# token = "97ae087c18351e1b53a41a5f3779413bd020f32c"
	# params = OrderedDict()
	# params["access_token"] = token

	# r = requests.get("https://api.github.com/authorizations")
	# j = r.json()
	# return ', '.join([str(key) + ' ' + str(value) for key, value in j.items()])
	# for i in j:
	# 	requests.delete("https://api.github.com/authorizations/" + i["id"], urlencode(params))
	resp = make_response(redirect(url_for('hello')))
	resp.set_cookie("access_token", "")
	resp.set_cookie("logged_in", "")
	resp.set_cookie("user", "")
	return resp 

@app.route('/about')
def about():
	logged_in = sanitize(request.cookies.get("logged_in"))
	return render_template('about.html', logged_in=logged_in)

@app.route('/user', methods=['GET', 'POST'])
def user():
	# token = request.cookies.get("access_token")
	token = "978ca3a1c15d3ca0dc6789f30bc5bf2b45f3ffee"
	q = ""
	params = OrderedDict()
	if token: 
		params["access_token"] = token
	user = requests.get('https://api.github.com/user', params=urlencode(params)).json()
	return render_template('user.html', user=user)
