"""@Kaizuryu"""
## thanks to Moezilla (Pranav) for this awesome code

import ErinaBot.modules.mongo.is_karma_mongo as kk

from ErinaBot.modules.sql import log_channel_sql as logsql
import html

from telegram import ParseMode
from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup, ParseMode, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler)
from telegram.utils.helpers import mention_html

from ErinaBot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from ErinaBot import  dispatcher
from ErinaBot.modules.log_channel import gloggable, loggable

bot_name = f"{dispatcher.bot.first_name}"

from ErinaBot import MONGO_DB_URL

from pymongo import MongoClient

worddb = MongoClient(MONGO_DB_URL) 
k = worddb["erina"]["karma_status"]
 

@user_admin_no_reply
def karmaadd(update: Update, context:CallbackContext):
    query= update.callback_query
    bot = context.bot
    user = update.effective_user
    if query.data == "add_karma":
        chat = update.effective_chat
        done = k.insert_one({"chat_id": chat.id})    
        update.effective_message.edit_text(
            f"{bot_name} Karma System Disabled by {mention_html(user.id, user.first_name)}.",
            parse_mode=ParseMode.HTML,
        )
               


@user_admin_no_reply
def karmarem(update: Update, context:CallbackContext):
    query= update.callback_query
    bot = context.bot
    user = update.effective_user
    if query.data == "rem_karma":
        chat = update.effective_chat
        done = k.delete_one({"chat_id": chat.id})            
        update.effective_message.edit_text(
            f"{bot_name} Karma System Enabled by {mention_html(user.id, user.first_name)}.",
            parse_mode=ParseMode.HTML,
        )           

@user_admin
@loggable
def karma_toggle(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    is_chatbot = k.find_one({"chat_id": chat.id})
    if is_chatbot:
        msg = "Karma Toggle\n Mode : DISABLE"
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                text="Enable",
                callback_data=r"rem_karma")]])     
        message.reply_text(
            msg,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )
    if not is_chatbot:
        msg = "Karma Toggle\n Mode : ENABLE"
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                text="Disable",
                callback_data=r"add_karma")]])     
        message.reply_text(
            msg,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )

KARMA_STATUS_HANDLER = CommandHandler("karma", karma_toggle, run_async = True)
ADD_KARMA_HANDLER = CallbackQueryHandler(karmaadd, pattern=r"add_karma", run_async = True)
RM_KARMA_HANDLER = CallbackQueryHandler(karmarem, pattern=r"rem_karma", run_async = True)

dispatcher.add_handler(ADD_KARMA_HANDLER)
dispatcher.add_handler(KARMA_STATUS_HANDLER)
dispatcher.add_handler(RM_KARMA_HANDLER)

__handlers__ = [
    ADD_KARMA_HANDLER,
    KARMA_STATUS_HANDLER,
    RM_KARMA_HANDLER,
]