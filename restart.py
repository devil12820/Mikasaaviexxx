import os
import requests
import sys
from pyrogram import Client, filters

# Create a new Pyrogram Client
app = Client(
    "my_bot",
    api_id=os.environ.get("API_ID"),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN")
)

# Function to restart the bot using Heroku API
def restart_heroku_app():
    heroku_api_key = os.environ.get('HEROKU_API_KEY')
    heroku_app_name = os.environ.get('HEROKU_APP_NAME')

    if not heroku_api_key or not heroku_app_name:
        print("Heroku API key or app name not found in environment variables.")
        return

    url = f"https://api.heroku.com/apps/{heroku_app_name}/dynos"
    headers = {
        "Authorization": f"Bearer {heroku_api_key}",
        "Accept": "application/vnd.heroku+json; version=3",
        "Content-Type": "application/json"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 202:
        print("Heroku app is restarting...")
    else:
        print(f"Failed to restart Heroku app: {response.status_code}, {response.text}")

# /restart command handler
@app.on_message(filters.command("re-start") & filters.user(int(os.environ.get("OWNER_ID"))))
def restart_command(client, message):
    message.reply_text("Restarting the bot...")
    restart_heroku_app()

# If you prefer to restart by simply exiting the process (Heroku will restart it):
def restart_bot():
    sys.exit(0)

# Alternatively, to use the simple sys.exit() restart, you could do:
# @app.on_message(filters.command("restart") & filters.user(int(os.environ.get("OWNER_ID"))))
# def restart_command(client, message):
#     message.reply_text("Restarting the bot...")
#     restart_bot()

# Run the bot
app.run()
