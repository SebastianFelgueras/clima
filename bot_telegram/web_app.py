from flask import Flask
import pickle

app = Flask(__name__)

@app.route("/")
def hello_world():
    return ""