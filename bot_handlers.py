# -*- coding: utf-8 -*-
import telebot

TOKEN = "5215290543:AAEzpfrfbNN4pAGzEn66oCskb-CxafDwFlk"
bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['test'])
def handle_start_help(message):
    print("FUCK")
    # week = date.today().isocalendar()[1] % 2 + 1
    # day = calendar.day_name[date.today().weekday()]
    # if ((day != "Sunday") and (day != "Saturday")):
    #     name = "src/" + day + '_' + str(week)
    #     handle = open(name, "r")
    #     data = handle.read()
    #     handle.close()
    # else:
    #     data = "Сегодня пар нет!"
    # bot.reply_to(message, data)

bot.polling(none_stop=True)