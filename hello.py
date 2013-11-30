import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():

	if request.method == 'GET':
		return render_template('hello.html')
	if request.method == 'POST':
		return render_template('layout.html')
	return "Hello!"
