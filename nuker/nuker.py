import datetime
import os
from twilio.rest import Client
from slack_cleaner2 import *

def instantiate_slack_client():
    print("Instantiating slack client")
    api_key = os.getenv("SLACK_API_KEY")
    sc = SlackCleaner(api_key)
    return sc

def nuke_channel(sc, channel="announcements", date_to_nuke_before="2021-07-01"): # change these
    date_intermediate = datetime.datetime.strptime(date_to_nuke_before, "%Y-%m-%d")
    date_to_nuke_before_unix = datetime.datetime.timestamp(date_intermediate)
    for msg in sc.msgs(filter(match(channel), sc.conversations)):
        ts = float(str(msg).partition(":")[2].split()[0])
        if ts < date_to_nuke_before_unix:
            print(f"deleting {msg}\n")
            msg.delete(replies=True, files=True)
    return

def notify_via_text(message="nuker failed, check it out"):
    phones_list = ["+19175493139"] # change this
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    for recipient in phones_list:
        message = client.messages.create(
                         body=message,
                         from_="+18623079274",
                         to=recipient)
    return

def main():
    sc = instantiate_slack_client()
    try:
        nuke_channel(sc)
    except Exception as e:
        print(e)
        notify_via_text(message=e)

if __name__ == '__main__':
    main()
