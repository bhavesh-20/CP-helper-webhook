import atexit
from flask import Flask
from services.cphelper_service import CpHelper

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


scheduler = BackgroundScheduler()
scheduler.start()

scheduler.add_job(
    func=lambda: print("hey"), trigger="cron", hour="8", minute="0", day="*"
)

atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def docs():
    return "Server is up"


@app.route("/contests")
def contests():
    return CpHelper.get_contest_schedules()
