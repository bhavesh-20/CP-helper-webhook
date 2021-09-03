import atexit, os
from dotenv import load_dotenv
from flask import Flask
from services.cphelper_service import CpHelper
from triggers.contest_schedule_trigger import ContestTrigger

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.start()

scheduler.add_job(
    func=ContestTrigger.trigger, trigger="cron", hour="9", minute="0", day="*"
)

atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def docs():
    return "Server is up"


@app.route("/contests")
def contests():
    return CpHelper.get_contest_schedules()


@app.route("/trigger_notification")
def trigger_notification():
    ContestTrigger.trigger()
    return "Notifications sent to Discord"


if __name__ == "__main__":
    load_dotenv()
    app.run(
        debug=False,
        use_reloader=False,
        port=os.environ.get("PORT", 5000),
        host="0.0.0.0",
    )
