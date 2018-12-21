from kitty_pics import KittyPics
from telegram.ext import Updater, RegexHandler, Filters
import logging
import os
import random
import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

token = os.environ['BOT_TOKEN']

class CoolDown(object):
    def __init__(self):
        self.last_time = {}

    def check(self, func, chat_id, cooldown):
        if not func in self.last_time.keys():
            self.last_time[func] = {}

        if not chat_id in self.last_time[func].keys():
            self.last_time[func][chat_id] = time.strptime("01 Jan 1970", "%d %b %Y")
            
        if (time.mktime(time.localtime()) - time.mktime(self.last_time[func][chat_id])) >= cooldown:
            self.last_time[func][chat_id] = time.localtime()
            return True
        else:
            return False

cooldown = CoolDown()

def kitty(bot, update):
    """Sends a random picture from shared kittypics Google Drive folder to chat."""
    cooldown_ended = cooldown.check('kitty', update.message.chat_id, 15)
    if cooldown_ended:
        logger.info("Sending kitty pic...")
        kitty_photos = KittyPics().pics
        random_number = random.randint(0, len(kitty_photos) - 1)
        photo_url=kitty_photos[random_number]
        update.message.reply_photo(photo=photo_url, quote=False)

def wow(bot, update):
    random_number = random.randint(1, 5)
    if random_number == 3:
        cooldown_ended = cooldown.check('wow', update.message.chat_id, 30)
        if cooldown_ended:
            wowstrings = [
                    'Wow',
                    'Like wow',
                    'Just wow',
                    'W O W'
                    ]
            random_number = random.randint(0, len(wowstrings) - 1)
            bot.send_message(chat_id=update.message.chat_id, text=wowstrings[random_number])

def beautiful(bot, update):
    random_number = random.randint(1, 5)
    if random_number == 3:
        cooldown_ended = cooldown.check('beautiful', update.message.chat_id, 30)
        if cooldown_ended:
            beautifulstrings = [
                    'Beautiful',
                    'So beautiful',
                    "It's beautiful",
                    'Absolutely beautiful',
                    'And beautiful'
                    ]
            random_number = random.randint(0, len(beautifulstrings) - 1)
            bot.send_message(chat_id=update.message.chat_id, text=beautifulstrings[random_number])

def triggered(bot, update):
    if update.message.from_user.username == 'grandmachine':
        random_number = random.randint(1, 3)
        if random_number == 2:
            cooldown_ended = cooldown.check('triggered', update.message.chat_id, 30)
            if cooldown_ended:
                triggered_gif_url = 'https://media.giphy.com/media/vk7VesvyZEwuI/giphy.gif'
                bot.send_animation(chat_id=update.message.chat_id, animation=triggered_gif_url)

def sorry(bot, update):
    random_number = random.randint(1, 10)
    if random_number == 7:
        cooldown_ended = cooldown.check('sorry', update.message.chat_id, 30)
        if cooldown_ended:
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
    dp.add_handler(RegexHandler('.*(?i)(exposed|trash|lonzo|garbage|lakers|jesus|wtf|triggered).*', triggered))

    # sorry gif
    dp.add_handler(RegexHandler('.*(?i)(sorry|sohrry|sorey|soarry).*', sorry))

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
