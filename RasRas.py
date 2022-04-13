#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
RASRAS the BESTBEST

"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tokens import TOKEN as TOKEN, telegram_master as TM
from RasSpotipy import *
from responses import *
from RasSmartThings import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Checks if the user is me
def verify_boss(update, context):
    user = update.message.from_user
    if user['username'] == TM:
        return 1
    else:
        update.message.reply_text('Hey! This feature is only for my boss!')

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    #update.message.reply_text('Hi!')
    user = update.message.from_user
    update.message.reply_text('Hi {}!'.format(user['first_name']))
    
    #update.message.reply_text('You talk with user {} and his user ID: {} '.format(user['username'], update.message.chat_id))

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    #update.message.reply_text(update.message.text)
    user = update.message.from_user
    text = update.message.text
    if "Hi" in text:
        update.message.reply_text('Hi {}!'.format(user['first_name']))
    if "What song is this?" in text:
        nowplaying(update, context)
    if "turn on" in text.lower() or "turn off" in text.lower():
        ST(update, context)
#need to add volume and shuffle

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def my_id(update, context):
    user = update.message.from_user
    update.message.reply_text('Your Chat ID: {}'.format(update.message.chat_id))
	
def test(update, context):
    update.message.reply_text('TEST!')
##################################################################################
#
#
#                                    SPOTIFY
#
#
##################################################################################
def nowplaying(update, context):
    if bool(verify_boss(update, context)):
        #refresh_token()
        if get_currently_playing() == 1:
            update.message.reply_text(resp_nothing_is_playing())
        else:
            update.message.reply_text(get_currently_playing())

def next_track(update, context):
    if bool(verify_boss(update, context)):
        #refresh_token()
        try:
            play_next()
            update.message.reply_text("{}{}".format(resp_now_playing(),get_currently_playing()))
        except:
            update.message.reply_text(resp_nothing_is_playing())
            

def previous_track(update, context):
    if bool(verify_boss(update, context)):
        #refresh_token()
        try:
            play_previous()
            update.message.reply_text("{}{}".format(resp_now_playing(),get_currently_playing()))
        except:
            update.message.reply_text(resp_nothing_is_playing())

def pause_track(update, context):
    if bool(verify_boss(update, context)):
        #refresh_token()
        try:
            play_pause()
            update.message.reply_text("Done!")
        except:
            update.message.reply_text(resp_nothing_is_playing())	
	
def play_track(update, context):
    if bool(verify_boss(update, context)):
        #refresh_token()
        try:
            play_play()
            update.message.reply_text("{}{}".format(resp_now_playing(),get_currently_playing()))
        except:
            update.message.reply_text(resp_already_playing())
	
##################################################################################
#
#
#                                    SMARTTHINGS
#
#
##################################################################################
def ST(update, context):
    if bool(verify_boss(update, context)):
        text = update.message.text
        #update.message.reply_text(text)
        update.message.reply_text(RasRas_ST_Input(text))

def ST_list(update, context):
    if bool(verify_boss(update, context)):
        text = update.message.text
        update.message.reply_text(RasRas_ST_getDevices())
		
		
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("my_id", my_id))
    dp.add_handler(CommandHandler("test", test))
    #Spotify
    dp.add_handler(CommandHandler("nowplaying", nowplaying))
    dp.add_handler(CommandHandler("nexttrack", next_track))
    dp.add_handler(CommandHandler("previoustrack", previous_track))
    dp.add_handler(CommandHandler("pausetrack", pause_track))
    dp.add_handler(CommandHandler("playtrack", play_track))
    dp.add_handler(CommandHandler("st", ST))
    dp.add_handler(CommandHandler("stlist", ST_list))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

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