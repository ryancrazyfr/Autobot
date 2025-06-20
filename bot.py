import logging
import random
import os
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

# ==== CONFIGURATION ====
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNEL_ID = -1002838163479
TARGET_CHANNEL_ID = -1002413978959
TIMEZONE = pytz.timezone('Asia/Colombo')

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store recent messages to rotate
recent_posts = []

# ==== HANDLERS ====
def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Auto-posting bot is running!\nAds will post at 6 AM and 5 PM daily.")

def fetch_recent_posts(context: CallbackContext):
    logger.info("Fetching posts from source channel...")

def post_random_ad(context: CallbackContext):
    if not recent_posts:
        logger.warning("No posts available to send.")
        return

    try:
        context.bot.send_message(chat_id=TARGET_CHANNEL_ID, text="🟢 This is a test ad from AutoBot!")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")

# ==== MAIN FUNCTION ====
def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    scheduler = BackgroundScheduler(timezone=TIMEZONE)
    scheduler.add_job(lambda: fetch_recent_posts(None), 'interval', hours=1)
    scheduler.add_job(lambda: post_random_ad(None), 'cron', hour=6, minute=0)
    scheduler.add_job(lambda: post_random_ad(None), 'cron', hour=17, minute=0)
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
