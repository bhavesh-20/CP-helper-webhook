import atexit, requests, os, threading, time
from flask import Flask
from services.cphelper_service import CpHelper
from triggers.contest_schedule_trigger import ContestTrigger

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


@app.before_first_request
def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()

    scheduler.add_job(
        func=ContestTrigger.trigger, trigger="cron", hour="2", minute="30", day="*"
    )

    atexit.register(lambda: scheduler.shutdown())


def send_first_request():
    def event_loop():
        not_started, flag = True, True
        while not_started:
            try:
                SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:5000")
                response = requests.get(SITE_URL)
                if response.status_code == 200:
                    requests.post(
                        ContestTrigger.ERR_WEBHOOK_URL,
                        data={"content": "Server started"},
                    )
                    not_started = False
                flag = True
            except Exception as e:
                if flag:
                    requests.post(
                        ContestTrigger.ERR_WEBHOOK_URL,
                        data={"content": f"{SITE_URL} not started."},
                    )
                    flag = False
            time.sleep(2)

    thread = threading.Thread(target=event_loop)
    thread.start()


@app.route("/")
def docs():
    return "Server is up"


@app.route("/contests")
def contests():
    return CpHelper.get_contest_schedules()


if __name__ == "__main__":
    send_first_request()
    app.run()
