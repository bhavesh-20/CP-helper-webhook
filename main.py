import atexit
from flask import Flask
from services.cphelper_service import CpHelper
from triggers.contest_schedule_trigger import ContestTrigger

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


scheduler = BackgroundScheduler()
scheduler.start()

scheduler.add_job(
    func=ContestTrigger.trigger, trigger="cron", hour="8", minute="0", day="*"
)

atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def docs():
    return "Server is up"


@app.route("/contests")
def contests():
    return CpHelper.get_contest_schedules()


if __name__ == "__main__":
    app.run()
