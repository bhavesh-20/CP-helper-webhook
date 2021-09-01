from flask import Flask
from services.cphelper_service import CpHelper

app = Flask(__name__)

@app.route("/")
def docs():
    return "Server is up"

@app.route("/contests")
def contests():
    return CpHelper.get_contest_schedules()