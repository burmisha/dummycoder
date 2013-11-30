import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('layout.html')

# def hello():
    # return 'Hello World!'
