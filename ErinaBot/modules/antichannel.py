
"""@Kaizuryu"""

import html
from telegram.ext.filters import Filters
from telegram import Update, message, ParseMode
from telegram.ext import CallbackContext

from ErinaBot.modules.helper_funcs.decorators import ErinaBotcmd, ErinaBotmsg
from ErinaBot.modules.helper_funcs.anonymous import user_admin, AdminPerms
from ErinaBot.modules.sql.antichannel_sql import antichannel_status, disable_antichannel, enable_antichannel

@ErinaBotcmd(command="antichannelmode", group=100)
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
def set_antichannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            enable_antichannel(chat.id)
            message.reply_html(f"Enabled Antichannel in {html.escape(chat.title)}")
        elif s in ["off", "no"]:
            disable_antichannel(chat.id)
            message.reply_html(f"Disabled Antichannel in {html.escape(chat.title)}")
        else:
            message.reply_text(f"Unrecognized arguments {s}")
        return
    message.reply_html(
        f"Antichannel setting is currently {antichannel_status(chat.id)} in {html.escape(chat.title)}"
    )

@ErinaBotmsg(Filters.chat_type.groups, group=110)
def eliminate_channel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    bot = context.bot
    if not antichannel_status(chat.id):
        return
    if message.sender_chat and message.sender_chat.type == "channel" and not message.is_automatic_forward:
        message.delete()
        sender_chat = message.sender_chat
        bot.ban_chat_sender_chat(sender_chat_id=sender_chat.id, chat_id=chat.id)
        

__mod_name__ = "Anti Channel"

__help__ ="""

    ⚠️ WARNING ⚠️
 
IF YOU USE THIS MODE, THE RESULT IS, IN THE GROUP, YOU CAN'T CHAT USING THE CHANNEL FOR FOREVER IF YOU GET BANNED ONCE

Anti Channel Mode is a mode to automatically ban users who chat using Channels. 
This command can only be used by Admins.

/antichannelmode <'on'/'yes'> : enables anti-channel-mode
/antichannelmode <'off'/'no'> : disabled anti-channel-mode
"""
