from instagram_bot import GetRecentPics
from telegram.ext import Updater, RegexHandler, Filters
import logging
import os
import random

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

token = os.environ['BOT_TOKEN']

def kitty(bot, update):
    """Sends a random picture from patrick_and_hank's Instagram page to chat."""
    logger.info("Sending kitty pic...")
    instagram_photos = GetRecentPics().pics
    random_number = random.randint(1, len(instagram_photos) + 1)
    photo_url=instagram_photos[random_number]
    update.message.reply_photo(photo=photo_url, quote=False)

def error(bot, update, error):
    """Log errors caused by updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    logger.info("Starting bot...")

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(RegexHandler('.*\/kitty.*', kitty))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
