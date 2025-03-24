import datetime
import time
import os
import requests
from telethon.sync import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, CHAT_ID, MONITORED_USERS

client = TelegramClient('session_name_aws', API_ID, API_HASH)


THRESHOLD_DAYS = 9
CHECK_INTERVAL = 7200
NOTIFICATION_COOLDOWN_DAYS = 3

last_notification = {}


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    try:
        resp = requests.post(url, data=data)
        if resp.status_code != 200:
            print(f"Sending error: {resp.text}")
        else:
            print("Message sent!")
    except Exception as e:
        print("Telegram send message exception:", e)


def check_user_last_interaction(user_id: int):
    """
    Retrieves the last message from the user by their ID and calculates
    how many days have passed since that message.
    """
    messages = client.get_messages(user_id, limit=1)
    if messages:
        last_message = messages[0]
        last_date = last_message.date
        # Use timezone information from last_date if available
        now = datetime.datetime.now(last_date.tzinfo) if last_date.tzinfo else datetime.datetime.now()
        inactivity_days = (now - last_date).days
        return last_date, inactivity_days
    return None, None


def main_loop():
    global last_notification
    while True:
        print("Checking user activity...")
        for user_id, name in MONITORED_USERS.items():
            last_date, inactivity_days = check_user_last_interaction(user_id)
            if last_date:
                print(f"{name} (ID: {user_id}): last message at {last_date} ({inactivity_days} days ago)")
                if inactivity_days >= THRESHOLD_DAYS:
                    now = datetime.datetime.now()
                    # Check if a notification was already sent recently
                    if user_id in last_notification:
                        diff = now - last_notification[user_id]
                        if diff.days < NOTIFICATION_COOLDOWN_DAYS:
                            print(f"Notification for {name} was already sent {diff.days} days ago. Skipping.")
                            continue
                    notification = f"You haven't interacted with {name} (ID: {user_id}) for {inactivity_days} days."
                    send_telegram_message(notification)
                    print(f"Notification sent: {notification}")
                    last_notification[user_id] = now
            else:
                print(f"No messages found for {name} (ID: {user_id}).")
        print(f"Waiting {CHECK_INTERVAL} seconds until next check...")
        time.sleep(CHECK_INTERVAL)


def main():
    # Start the client (on first run, you'll need to input your phone number and confirmation code)
    client.start()
    try:
        main_loop()
    except KeyboardInterrupt:
        print("User interruption. Shutting down.")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        client.disconnect()
        print("Client disconnected.")


if __name__ == '__main__':
    main()
