from services.cphelper_service import CpHelper
from flask_api import status

import requests


class ContestTrigger:

    ERR_WEBHOOK_URL = "https://discord.com/api/webhooks/882575945859498014/8h0dSCyKoQwHZuadGM4S7gW0E7YzKBusisWsxi4TOx3s6FXeAzZxO5DwBfncGOAWMydU"
    CONTEST_WEBHOOK_URL = "https://discord.com/api/webhooks/882514149731622932/nPY-RUPjxzLqP9v3k8HrMBWK1j2-NTSHcRW4PcLHDiugbiZcP6Vm81EZ8ojbtExbIkqJ"

    @classmethod
    def trigger(
        cls,
    ):
        op_status, resp = cls.get_dicord_message()
        if not op_status:
            data = {
                "content": resp["message"],
            }
            requests.post(cls.ERR_WEBHOOK_URL, data=data)
        else:
            message = resp.get("message")
            data = {
                "content": message,
            }
            requests.post(cls.CONTEST_WEBHOOK_URL, data=data)
        return None

    @classmethod
    def get_dicord_message(
        cls,
    ):
        resp, status_code = CpHelper.get_contest_schedules()
        if status_code != status.HTTP_200_OK:
            return False, {"message": "Failed" + "\n" + resp["message"]}

        contest_details = resp.get("data")

        if len(contest_details) == 0:
            return False, {"message": "No Contest data available for today."}

        reminder_message = "Hey @everyone, Daily Contest Reminder" + "\n"

        for contest in contest_details:
            message = (
                f"{contest['event']} starts {contest['starts_at']['type']} at {contest['starts_at']['value']}, hosted by {contest['host']}"
                + "\n"
            )
            message += f"Duration - {contest['duration']}" + "\n"
            message += f"Link - {contest['link']}" + "\n"
            reminder_message += message

        return True, {"message": reminder_message}
