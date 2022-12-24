import telebot

TOKEN = '5719165771:AAE4hbcTJgatvg-GYd3wLq64u4axRPDdnPE'
bot = telebot.TeleBot(TOKEN)

users = {}

@bot.message_handler(content_types=['new_chat_members'])
def hello_message(message):
    users.update({message.from_user.username: message.from_user.id})
    bot.send_message(message.chat.id, "Как поживаешь?")


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, f"Сделай админом @username - сделать пользователя @username админом \n"
                                      f"Свергни админа @username - удалить пользователя @username из админов \n"
                                      f"Забань @username - забанить пользователя @username \n"
                                      f"Разбань @username - разбанить пользователя @username \n"
                                      f"Сколько участников в чате? - узнать количество участников чата \n"
                                      f"Сколько админов в чате? - узнать количество администраторов чата \n"
                                      f"Бот, уходи - изгнать бота"
                     )


@bot.message_handler()
def message_reply(message):
    users.update({message.from_user.username: message.from_user.id})

    if message.text[:14] == "Сделай админом":
        try:
            bot.promote_chat_member(message.chat.id, users[message.text[16:]], can_change_info=True,
                                    can_delete_messages=True, can_invite_users=True,
                                    can_restrict_members=True, can_promote_members=True,
                                    is_anonymous=True, can_manage_chat=True,
                                    can_manage_video_chats=True)
        except KeyError:
            bot.send_message(message.chat.id, "Юзер не в базе")

    if message.text[:14] == "Свергни админа":
        try:
            bot.promote_chat_member(message.chat.id, users[message.text[16:]], can_change_info=False,
                                    can_delete_messages=False, can_invite_users=False,
                                    can_restrict_members=False, can_promote_members=False,
                                    is_anonymous=False, can_manage_chat=False,
                                    can_manage_video_chats=False)
        except KeyError:
            bot.send_message(message.chat.id, "Юзер не в базе")

    if message.text[:6] == "Забань":
        try:
            bot.ban_chat_member(message.chat.id, users[message.text[8:]])
        except KeyError:
            bot.send_message(message.chat.id, "Юзер не в базе")

    if message.text[:7] == "Разбань":
        try:
            bot.unban_chat_member(message.chat.id, users[message.text[9:]])
        except KeyError:
            bot.send_message(message.chat.id, "Юзер не в базе")

    if message.text == "Сколько админов в чате?":
        administrators = bot.get_chat_administrators(message.chat.id)
        bot.send_message(message.chat.id, len(administrators))

    if message.text == "Сколько участников в чате?":
        bot.send_message(message.chat.id, bot.get_chat_member_count(message.chat.id))

    if message.text == "Бот, уходи":
        bot.leave_chat(message.chat.id)


bot.polling(none_stop=True, interval=0, timeout=200)
