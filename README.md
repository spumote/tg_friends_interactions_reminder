# tg_friends_interactions_reminder

This project monitors your Telegram interactions with selected users and sends notifications if you haven't interacted with them for a specified period.

# Configuration

Create a file named config.py (and add it to your .gitignore) to store your sensitive data. For example:

```python
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR CHAT_ID"

MONITORED_USERS = {
    123456789: "Alice",
    987654321: "Bob",
    555555555: "Charlie"
}
