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

def wow(bot, update):
    wowstrings = [
            'Wow',
            'Like wow',
            'Just wow',
            'W O W'
            ]
    random_number = random.randint(1, len(wowstrings) + 1)
    bot.send_message(chat_id=update.message.chat_id, text=wowstrings[random_number])

def beautiful(bot, update):
    beautifulstrings = [
            'Beautiful',
            'So beautiful',
            "It's beautiful",
            'And beautiful'
            ]
    random_number = random.randint(1, len(beautifulstrings) + 1)
    bot.send_message(chat_id=update.message.chat_id, text=beautifulstrings[random_number])

def triggered(bot, update):
    if update.message.from_user.username == 'grandmachine':
        triggered_gif_url = 'https://media.giphy.com/media/vk7VesvyZEwuI/giphy.gif'
        bot.send_animation(chat_id=update.message.chat_id, animation=triggered_gif_url)

def sorry(bot, update):
    sorry_gif_url = 'https://media.giphy.com/media/CfaK14cY4CXao/giphy.gif'
    bot.send_animation(chat_id=update.message.chat_id, animation=sorry_gif_url)

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

    # Post picture of kitty when '/kitty' is said
    dp.add_handler(RegexHandler('.*\/kitty.*', kitty))

    # Allo wow spam
    dp.add_handler(RegexHandler('.*(?i)wow.*', wow))

    # Allo beautiful spam
    dp.add_handler(RegexHandler('.*(?i)beautiful.*', beautiful))

    # grandmachine triggered auto response
    dp.add_handler(RegexHandler('.*((?i)exposed|(?i)trash|(?i)lonzo|(?i)garbage|(?i)lakers|(?i)jesus|(?i)wtf|(?i)triggered).*', triggered))

    # sorry gif
    dp.add_handler(RegexHandler('.*((?i)sorry|(?i)sohrry|(?i)sorey|(?i)soarry).*', sorry))

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
