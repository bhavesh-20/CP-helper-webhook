from dateutil.relativedelta import relativedelta
from datetime import datetime, time, timedelta
from enum import Enum
import requests

from flask_api import status


class CpHelper:

    API_KEY = "3bca1c1a54cbdabbda22f365c159f9243155c398"
    USERNAME = "darkangel007"
    BASE_URL = (
        f"https://clist.by:443/api/v1/contest/?api_key={API_KEY}&username={USERNAME}"
    )

    class StartdateEnum(Enum):
        TODAY = 0
        TOMORROW = 1

    @classmethod
    def get_contest_parameters(
        cls,
    ):
        try:
            now = datetime.utcnow()
            start_time = now + timedelta(hours=5)
            end_time = now + timedelta(days=1, hours=5)
            resource_names = [
                "codechef.com",
                "codeforces.com",
                "codingcompetitions.withgoogle.com/kickstart",
                "leetcode.com",
                "atcoder.jp",
            ]

            url_params = {
                "start__gte": start_time,
                "start__lt": end_time,
                "order_by": "start",
                "resource__name__in": resource_names,
            }
            return True, {"data": url_params}
        except Exception as e:
            return False, {"message": str(e)}

    @classmethod
    def get_contest_schedules(
        cls,
    ):
        op_status, resp = cls.get_contest_parameters()
        if not op_status:
            return (
                {
                    "status": "failure",
                    "message": "something went wrong with fetching query parameters."
                    + resp["message"],
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        url_params = resp.get("data")
        response = requests.get(cls.BASE_URL, params=url_params)
        resp_data = response.json()
        contest_details = resp_data.get("objects")
        op_status, resp = cls._format_contest_details(contest_details)
        if not op_status:
            return (
                {
                    "status": "failure",
                    "message": "Error when formatting." + resp["message"],
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        contest_details = resp.get("data")
        return {"status": "success", "data": contest_details}, status.HTTP_200_OK

    @classmethod
    def _format_contest_details(cls, contest_details):
        try:
            formatted_contest_details = []
            now = datetime.utcnow() + timedelta(hours=5, minutes=30)
            for contest in contest_details:

                start_time = datetime.strptime(
                    contest.get("start"), "%Y-%m-%dT%H:%M:%S"
                )
                end_time = datetime.strptime(contest.get("end"), "%Y-%m-%dT%H:%M:%S")

                start_time += timedelta(hours=5, minutes=30)  # converting to ist.
                end_time += timedelta(hours=5, minutes=30)  # converting to ist.

                delta = relativedelta(end_time, start_time)
                duration = ""
                if delta.days != 0:
                    duration += f"{delta.days} days "
                if delta.hours != 0:
                    duration += f"{delta.hours} hours "
                if delta.minutes != 0:
                    duration += f"{delta.minutes} minutes"

                if now.day == start_time.day:
                    starts_at_type = cls.StartdateEnum.TODAY.name
                else:
                    starts_at_type = cls.StartdateEnum.TOMORROW.name

                formatted_contest_details.append(
                    {
                        "event": contest.get("event"),
                        "link": contest.get("href"),
                        "host": contest.get("resource").get("name").split(".")[0],
                        "host_icon": f"https://clist.by{contest.get('resource').get('icon')}",
                        "starts_at": {
                            "type": starts_at_type,
                            "value": start_time.strftime("%H:%M"),
                        },
                        "duration": duration,
                    }
                )
            return True, {"message": "success", "data": formatted_contest_details}
        except Exception as e:
            return False, {"message": str(e)}
