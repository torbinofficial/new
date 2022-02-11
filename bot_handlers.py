# -*- coding: utf-8 -*-
import telebot
DATABASE_URL = "postgres://kinuwoksbixpeq:61a9ec589a4c8c51797a5583aa6acffd447fd6f252d5c724f75f336cf8fd7272@ec2-54-247-137-184.eu-west-1.compute.amazonaws.com:5432/dc8d90g8j6g8ts"
TOKEN = "5298849535:AAEAcppc5zfA1D88YTOZGxPqaYLBUnOtNmE"
PASSWORD = "cbhtytdtymrbq70"
bot=telebot.TeleBot(TOKEN)
debug_chat_id = -608867877
import pandas as pd
import psycopg2

@bot.message_handler(commands=['add_admin'])
def add_admin(message):
    try:
        bot.send_message(message.chat.id, text = "Операция успешна")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['add_chat'])
def add_chat(message):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("SELECT * FROM chats WHERE id = %s ;", (message.chat.id, ))
        res = cur.fetchall()
        if res != []:
            bot.send_message(message.chat.id, text = "Этот чат уже добавлен в рассылку!")
            cur.close()
            conn.close()
            return
        cur.execute("""SELECT * FROM admins WHERE id = %s ;""", (message.from_user.id, ))
        res = cur.fetchall()
        if res != []:
            id_ = message.chat.id
            cur.execute("""INSERT INTO chats (id) VALUES (%s);""", (id_,))
            conn.commit()
            curr.close()
            conn.close()
            bot.send_message(message.chat.id, text = "Операция успешна")
        else:
            bot.send_message(message.chat.id, text = "Необходимо быть администратором!")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['chat_id'])
def chat_id(message):
    bot.send_message(message.chat.id, text=str(message.chat.id))

@bot.message_handler(commands=['edit_channel_tag'])
def edit_channel_tag(message):
    try:
        args = message.text.split("?")
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM admins WHERE id = %s""", (message.from_user.id, ))
        res = cur.fetchall()
        if res != []:
            cur.execute(""" UPDATE channels SET channel_tag = (%s) 
            WHERE id = (%s); """, (args[2], args[1] ))
            conn.commit()
            cur.execute("SELECT * FROM channels")
            res = cur.fetchall()
            for item in res:
                print(item)
            cur.close()
            conn.close()
            bot.send_message(message.chat.id, text = "Операция успешна")
        else:
            bot.send_message(message.chat.id, text = "Необходимо быть администратором")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['edit_channel_title'])
def edit_channel_title(message):
    try:
        args = message.text.split("?")
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM admins WHERE id = %s""", (message.from_user.id, ))
        res = cur.fetchall()
        if res != []:
            cur.execute(""" UPDATE channels SET channel_title = (%s) 
            WHERE id = (%s); """, (args[2], args[1] ))
            conn.commit()
            cur.execute("SELECT * FROM channels")
            res = cur.fetchall()
            for item in res:
                print(item)
            cur.close()
            conn.close()
            bot.send_message(message.chat.id, text = "Операция успешна")
        else:
            bot.send_message(message.chat.id, text = "Необходимо быть администратором")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['edit_admin_tag'])
def edit_admin_tag(message):
    try:
        args = message.text.split("?")
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM admins WHERE id = %s""", (message.from_user.id, ))
        res = cur.fetchall()
        if res != []:
            cur.execute(""" UPDATE channels SET admin_tag = (%s) 
            WHERE id = (%s); """, (args[2], args[1] ))
            conn.commit()
            cur.execute("SELECT * FROM channels")
            res = cur.fetchall()
            for item in res:
                print(item)
            cur.close()
            conn.close()
            bot.send_message(message.chat.id, text = "Операция успешна")
        else:
            bot.send_message(message.chat.id, text = "Необходимо быть администратором")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['edit_admin_title'])
def edit_admin_title(message):
    try:
        args = message.text.split("?")
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM admins WHERE id = %s""", (message.from_user.id, ))
        res = cur.fetchall()
        if res != []:
            cur.execute(""" UPDATE channels SET admin_title = (%s) 
            WHERE id = (%s); """, (args[2], args[1] ))
            conn.commit()
            cur.execute("SELECT * FROM channels")
            res = cur.fetchall()
            for item in res:
                print(item)
            cur.close()
            conn.close()
            bot.send_message(message.chat.id, text = "Операция успешна")
        else:
            bot.send_message(message.chat.id, text = "Необходимо быть администратором")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['edit_after_add'])
def edit_after_add(message):
    try:
        args = message.text.split("?")
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM admins WHERE id = %s""", (message.from_user.id, ))
        res = cur.fetchall()
        if res != []:
            cur.execute(""" UPDATE channels 
            SET admin_tag = (%s),
            admin_title = (%s),
            category = (%s)
            WHERE id = (%s); """, (args[2], args[3], args[4], args[1]))
            conn.commit()
            cur.execute("SELECT * FROM channels")
            res = cur.fetchall()
            for item in res:
                print(item)
            cur.close()
            conn.close()
            bot.send_message(message.chat.id, text = "Операция успешна")
        else:
            bot.send_message(message.chat.id, text = "Необходимо быть администратором")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")


@bot.message_handler(commands=['edit_category'])
def edit_category(message):
    try:
        args = message.text.split("?")
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM admins WHERE id = %s;""", (message.from_user.id, ))
        res = cur.fetchall()
        if res != []:
            cur.execute(""" UPDATE channels SET category = (%s) 
            WHERE id = (%s); """, (args[2], args[1] ))
            conn.commit()
            cur.execute("SELECT * FROM channels")
            res = cur.fetchall()
            for item in res:
                print(item)
            cur.close()
            conn.close()
            bot.send_message(message.chat.id, text = "Операция успешна")
        else:
            bot.send_message(message.chat.id, text = "Необходимо быть администратором")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands = ['del_channel'])
def del_channel(message):
    try:
        args = message.text.split("?")
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM admins WHERE id = %s""", (message.from_user.id, ))
        res = cur.fetchall()
        if res != []:
            cur.execute(""" DELETE FROM channels WHERE id = (%s); """ , (args[1], ))
            conn.commit()
            cur.execute("SELECT * FROM channels")
            res = cur.fetchall()
            for item in res:
                print(item)
            cur.close()
            conn.close()
            bot.send_message(message.chat.id, text = "Операция успешна")
        else:
            bot.send_message(message.chat.id, text = "Необходимо быть администратором")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['del_chat'])
def del_channel_id(message):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM admins WHERE id = %s""", (message.from_user.id, ))
        res = cur.fetchall()
        if res != []:
            cur.execute(""" DELETE FROM chats WHERE id = (%s); """, (message.chat.id, ))
            conn.commit()
            cur.execute("SELECT * FROM chats")
            res = cur.fetchall()
            for item in res:
                print(item)
            cur.close()
            conn.close()
            bot.send_message(message.chat.id, text = "Операция успешна")
        else:
            bot.send_message(message.chat.id, text = "Необходимо быть администратором")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.channel_post_handler(content_types=["animation", "text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact", "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo", "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id", "migrate_from_chat_id" , "pinned_message"])
def reposts(message):
    text = ""
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    if message.forward_from_chat != None:
        cur.execute("SELECT * FROM channels WHERE id = (%s) ;", (message.forward_from_chat.id, ))
        forwarded_from = cur.fetchall()
        if forwarded_from != []:
            cur.execute("SELECT * FROM channels WHERE id = (%s) ;", (message.chat.id, ))
            current_channel = cur.fetchall()
            if current_channel != []:
                text += current_channel[0][3] + " " + current_channel[0][1] + " репостнул " + forwarded_from[0][1] + " " + forwarded_from[0][3]  
                cur.execute("SELECT * FROM chats")
                chats = cur.fetchall()
                for item in chats:
                    bot.send_message(item[0] , text = text)

@bot.message_handler(commands=['link'])
def link(message):
    link = "https://www.dropbox.com/sh/zhjlyve0ak9lpn6/AAATEZLXs00tUowdEpZdP6mua?dl=0"
    bot.send_message(message.chat.id, text = link)

@bot.message_handler(commands=['list'])
def list_channels(message):
    args = message.text.split("?")
    texxt = ""
    try:    
        if args[1].replace(" ", "") == PASSWORD:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute(" SELECT * FROM channels ")
            channels = cur.fetchall()
            for item in channels:
                texxt += "Канал " + item[2] + "( " + item[1] + " ) \nАдмин - " + item[4] + "(" + item[3] + ") \nКатегории - " + item[5] + "\n \n"
            bot.send_message(message.chat.id,text = texxt) 
        else:
            bot.send_message(message.chat.id, text = "Неверный пароль!")
    except IndexError:
        bot.send_message(message.chat.id, text = "Введите пароль после знака ?")
 
@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.chat.id, text = "https://telegra.ph/Nachalo-raboty-i-spisok-kanalov-02-02")

@bot.message_handler(commands=['getId'])
def get_user_id(message):
    bot.send_message(message.chat.id, str(message.from_user.id))


@bot.channel_post_handler(commands=['getId'])
def get_channel_id(message):
    bot.send_message(message.chat.id, str(message.chat.id))

@bot.message_handler(content_types=["animation","text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact", "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo", "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id", "migrate_from_chat_id" , "pinned_message"])        
def add_channel_id_by_forward(message):        
    try:        
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM admins WHERE id = %s ; """, (message.from_user.id ,))
        is_admin = cur.fetchall()
        if (is_admin != []):
            if (message.forward_from_chat != None and message.chat.type == 'private'):
                channel_id = message.forward_from_chat.id
                channel_tag = "@" + str(message.forward_from_chat.username).replace("@", "")
                channel_title = message.forward_from_chat.title
                cur.execute("""INSERT INTO channels (id, channel_tag, channel_name, admin_tag, admin_title, category) 
                VALUES (%s, %s, %s, %s, %s, %s);""", 
                ( channel_id, 
                channel_tag, 
                channel_title, 
                "@Empty", 
                "Empty Empty",
                "Empty" ) )
                conn.commit()
                cur.execute("SELECT * FROM channels")
                db_version = cur.fetchall()
                for item in db_version:
                    print(item)   
                bot.send_message(message.chat.id, text = "Операция успешна, id канала: " + str(channel_id))
                cur.close()
                conn.close()
        else:
            bot.send_message(message.chat.id, text = "Необходимо быть администратором!")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")        


bot.polling(none_stop=True)
