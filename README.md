# CP-helper-webhook
A webhook for sending daily reminders about competitive programming contests in a discord channel.

Used https://clist.by API for implementation.

Before getting started go to https://clist.by API and create a user account and get the API key from there.
Also you would need your username to access their API so make note of it as well.


create an environment file(.env) and add the following variables to the .env file or you can directly add them to your environment as well.

```
API_KEY=<the api key you got from clist>
API_USERNAME=<your clist.by's username>
```

This isn't enough to finish your setup!

- Go to your discord server and create a webhook for a channel, using this webhook we are going to trigger discord's API endpoint which allows us to send messages.
Make note of this Webhook and add it to .env file using the name `CONTEST_WEBHOOK_URL`
- In some cases something might go wrong sending notifications to discord and you would like to be notified of what went wrong
in your discord channel itself to minimize your efforts, for this scenario create a channel and a webhook for it where you recieve messages when some error occurs in sending notifications
via discord like "no contests are scheduled" or "error formatting contests" so that you know why you didn't get any message that particular day.
- So `ERR_WEBHOOK_URL` is a webhook for notifying you in case something went wrong and `CONTEST_WEBHOOK_URL` is the main webhook where you get contest updates.
- personally i recommend you to create a personal server and add webhook for error notifications there so that it disturbs no one and you are in control.

```
ERR_WEBHOOK_URL=<your error webhook>
CONTEST_WEBHOOK_URL=<your main webhook>
```

Download the required dependencies using `pip install -r requirements.txt`

This is it!, you are Done with the setup.

More about the web server, There are two useful endpoints that you can use.
- `/contests` this returns the contest data for the contests that are in an interval (now+3hrs), (now+27hrs)
- `/trigger_notification` using this endpoint you can manually trigger notifications to discord.

Now there is an apscheduler's BackgroundScheduler(cron job) running which takes care of sending notifications to discord in the given time. Basically
we are executing a cron job in this scheduler, which you can configure in `main.py` file.
