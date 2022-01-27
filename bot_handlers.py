# -*- coding: utf-8 -*-
import telebot
import dropbox

DROPBOX_TOKEN = "0c2FLOlpeLMAAAAAAAAAAb9obp9hAZUxInCh5qCRoUh2A094mQOTrCJLvvpNP4gx"
TOKEN = "5298849535:AAEAcppc5zfA1D88YTOZGxPqaYLBUnOtNmE"
bot=telebot.TeleBot(TOKEN)
import pandas as pd
def dropbox_connect():
    try:
        dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    except AuthError as e:
        print(e)
    return dbx
def dropbox_list_files(path):
    dbx = dropbox_connect()
    try:
        files = dbx.files_list_folder(path).entries
        files_list = []
        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                metadata = {
                    'name': file.name,
                    'path_display': file.path_display,
                    'client_modified': file.client_modified,
                    'server_modified': file.server_modified
                }
                files_list.append(metadata)
        df = pd.DataFrame.from_records(files_list)
        return df.sort_values(by='server_modified', ascending=False)
    except Exception as e:
        print('Error getting list of files from Dropbox: ' + str(e))
def dropbox_download_file(dropbox_file_path, local_file_path):
    try:
        dbx = dropbox_connect()
        with open(local_file_path, 'wb') as f:
            metadata, result = dbx.files_download(path=dropbox_file_path)
            f.write(result.content)
    except Exception as e:
        print('Error downloading file from Dropbox: ' + str(e))
def dropbox_upload_file(local_file, dropbox_file_path):
    try:
        dbx = dropbox_connect()
        with open(local_file, 'rb') as f:
            meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))
        # f.close()
        return meta
        
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))

@bot.channel_post_handler(commands=['addChannel'])
def add_channel_id(message):
    try:
        args =  message.text.split("?")
        dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
        df = pd.read_excel('Book.xlsx', index_col=0)
        id_ = message.chat.id
        tag_ = str(message.chat.username)
        title_ = str(message.chat.title)
        for index, row in df.iterrows():
            if row['id канала'] == id_:
                bot.send_message(message.chat.id, text = "Канал уже добавлен!")
                return
        df.loc[df.shape[0]] = [id_, tag_, title_, args[1], args[2], args[3]]
        print(df)
        # print(df[df['id'] == -1001662709181].index.values)
        df.to_excel("Book.xlsx", sheet_name = "channels")
        dbx = dropbox_connect()
        dbx.files_delete("/hitler-bot/Book.xlsx")
        dropbox_upload_file("Book.xlsx", "/hitler-bot/Book.xlsx")
        bot.send_message(message.chat.id, text = "Операция успешна")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")
        

@bot.message_handler(commands=['addChannel'])
def add_channel_id(message):
    try:
        args =  message.text.split("?")
        dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
        df = pd.read_excel('Book.xlsx', index_col=0)
#         id_ = message.chat.id
#         tag_ = str(message.chat.username)
#         title_ = str(message.chat.title)
        for index, row in df.iterrows():
            if row['id канала'] == id_:
                bot.send_message(message.chat.id, text = "Канал уже добавлен!")
                return
        df.loc[df.shape[0]] = [args[1], args[2], args[3], args[4], args[5], args[6]]
        print(df)
        # print(df[df['id'] == -1001662709181].index.values)
        df.to_excel("Book.xlsx", sheet_name = "channels")
        dbx = dropbox_connect()
        dbx.files_delete("/hitler-bot/Book.xlsx")
        dropbox_upload_file("Book.xlsx", "/hitler-bot/Book.xlsx")
        bot.send_message(message.chat.id, text = "Операция успешна")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")        
        
@bot.message_handler(commands=['link'])
def list_channels(message):
    link = "https://www.dropbox.com/sh/zhjlyve0ak9lpn6/AAATEZLXs00tUowdEpZdP6mua?dl=0"
    bot.send_message(message.chat.id, text = link)
@bot.message_handler(commands=['list'])
def list_channels(message):
    try:
        text = ""
        dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
        df = pd.read_excel('Book.xlsx', index_col=0)
        for item in range(0, df.shape[0]):
            stringg = str(item) + ". \n" + df.iloc[item].to_string()
            bot.send_message(message.chat.id, text = stringg)
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")
 
@bot.message_handler(commands = ['help'])
def help(message):
    message1 = "Порядок действий: \n" 
    message2 = "1. Добавить бота на каналы и прописать НА КАНАЛЕ: \n" 
    message3 = "/ addChannel ? @тег админа ? имя админа ? категория канала \n" 
    message4 = "2. / addChat внутри ЧАТА куда будут пересылаться сообщения \n" 
    message5 = "/ addChannel ? @тег админа ? имя админа ? категория канала - добавить КАНАЛ в список"
    message6 = "/ addChat - добавить ЧАТ (нужно быть суперадмином)"
    message7 = "/ addAdmin - добавить суперадмина \n"
    message8 = "/ delChannel <id> - удалить канал, нужно быть суперадмином (можно на канале без использования id) \n" 
    message9 = "/ delChat - удалить текущий чат (нужно быть суперадмином) \n" 
    message10 = "/ getId - внутри чата, получить свой текущий id, на канале - id канала \n" 
    message11 = "/ link - ссылка на базу данных \n"  
    message12 = "/ list - список каналов \n" 
    text = message1 + message2 + message3 + message4 + message5 + message6 + message7 + message8 + message9 + message10 + message11
    bot.send_message(message.chat.id, text = text)

@bot.message_handler(commands = ['delChannel'])
def del_channel(message):
    try:
        dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
        df = pd.read_excel('Book.xlsx', index_col=0)
        dropbox_download_file("/hitler-bot/Admins.xlsx", "Admins.xlsx")    
        admins = pd.read_excel("Admins.xlsx", index_col= 0)
        for index, row in admins.iterrows():
            if row['id канала'] == message.from_user.id:
                id_ = message.text.split()[1]
                i = df[df['id канала'] == id_].index.values
                df.drop(i, axis = 0, inplace = True)
                df.to_excel("Book.xlsx", sheet_name = "channels")
                dbx = dropbox_connect()
                dbx.files_delete("/hitler-bot/Book.xlsx")
                dropbox_upload_file("Book.xlsx", "/hitler-bot/Book.xlsx") 
                bot.send_message(message.chat.id, text = "Операция успешна")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['addAdmin'])
def add_admin():
    try:
        dropbox_download_file("/hitler-bot/Admins.xlsx", "Admins.xlsx")    
        admins = pd.read_excel("Admins.xlsx", index_col= 0)
        for index, row in admins.iterrows():
            if row['id'] == message.text.split()[1]:
                bot.send_message(message.chat.id, text = "Админ уже добавлен!")
                return
        for index, row in admins.iterrows():
            if row['id'] == message.from_user.id:
                id_ = message.text.split()[1]
                i = df[df['id'] == id_].index.values
                df.drop(i, axis = 0, inplace = True)
                df.to_excel("Admins.xlsx", sheet_name = "channels")
                dbx = dropbox_connect()
                dbx.files_delete("/hitler-bot/Admins.xlsx")
                dropbox_upload_file("Admins.xlsx", "/hitler-bot/Admins.xlsx") 
                bot.send_message(message.chat.id, text = "Операция успешна")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")



@bot.channel_post_handler(commands=['delChannel'])
def del_channel_id(message):
    try:
        dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
        df = pd.read_excel('Book.xlsx', index_col=0)
        id_ = message.chat.id
        tag_ = str(message.chat.username)
        title_ = str(message.chat.title)
        i = df[df['id канала'] == id_].index.values
        df.drop(i, axis = 0, inplace = True)
        df.to_excel("Book.xlsx", sheet_name = "channels")
        dbx = dropbox_connect()
        dbx.files_delete("/hitler-bot/Book.xlsx")
        dropbox_upload_file("Book.xlsx", "/hitler-bot/Book.xlsx") 
        bot.send_message(message.chat.id, text = "Операция успешна")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['addChat'])
def add_chat(message):
    try:
        dropbox_download_file("/hitler-bot/Chats.xlsx", "Chats.xlsx")
        df = pd.read_excel('Chats.xlsx', index_col=0)
        dropbox_download_file("/hitler-bot/Admins.xlsx", "Admins.xlsx")    
        admins = pd.read_excel("Admins.xlsx", index_col= 0)
        for index, row in df.iterrows():
            if row['id'] == message.chat.id:
                bot.send_message(message.chat.id, text = "Чат уже добавлен в рассылку!")
                return
        for index, row in admins.iterrows():
            if row['id'] == message.from_user.id:
                id_ = message.chat.id
                df.loc[df.shape[0]] = [id_]
                print(df)
                df.to_excel("Chats.xlsx")
                dbx = dropbox_connect()
                dbx.files_delete("/hitler-bot/Chats.xlsx")
                dropbox_upload_file("Chats.xlsx", "/hitler-bot/Chats.xlsx")
                bot.send_message(message.chat.id, text = "Операция успешна")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['delChat'])
def del_channel_id(message):
    try:
        dropbox_download_file("/hitler-bot/Chats.xlsx", "Chats.xlsx")
        df = pd.read_excel('Chats.xlsx', index_col=0)
        dropbox_download_file("/hitler-bot/Admins.xlsx", "Admins.xlsx")    
        admins = pd.read_excel("Admins.xlsx", index_col= 0)
        for index, row in admins.iterrows():
            if row['id канала'] == message.from_user.id:
                id_ = message.chat.id
                i = df[df['id канала'] == id_].index.values
                df.drop(i, axis = 0, inplace = True)
                df.to_excel("Chats.xlsx", sheet_name = "channels")
                dbx = dropbox_connect()
                dbx.files_delete("/hitler-bot/Chats.xlsx")
                dropbox_upload_file("Chats.xlsx", "/hitler-bot/Chats.xlsx") 
                bot.send_message(message.chat.id, text = "Операция успешна")
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

# dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
# df = pd.DataFrame(columns=['id канала', 'Тег канала', 'Название канала', 'Тег админа', 'Имя админа', 'Категория'])
# df.loc[df.shape[0]] = ['0', '0', '0', '0', '0', '0']
# temp = df.to_excel("Book.xlsx")
# dbx = dropbox_connect()
# dbx.files_delete("/hitler-bot/Book.xlsx")
# dropbox_upload_file("Book.xlsx", "/hitler-bot/Book.xlsx")

@bot.message_handler(commands=['getId'])
def get_user_id(message):
    bot.send_message(message.chat.id, str(message.from_user.id))


@bot.channel_post_handler(commands=['getId'])
def get_channel_id(message):
    bot.send_message(message.chat.id, str(message.chat.id))

@bot.channel_post_handler()
def reposts(message):
    text = ""
    dropbox_download_file("/hitler-bot/Chats.xlsx", "Chats.xlsx")
    dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
    channels = pd.read_excel('Book.xlsx', index_col=0)
    chats = pd.read_excel('Chats.xlsx', index_col=0)
    if message.forward_from_message_id != None:
        if (channels['id канала'].isin([message.forward_from_chat.id]).any() and channels['id канала'].isin([message.chat.id]).any()):
            for index, row in channels.iterrows():
                if(row['id канала'] == message.chat.id):
                    text += "Админ " + str(row['Тег админа']) + "канала " + str(row['Тег канала']) + " репостнул "
            for index, row in channels.iterrows():
                if(row['id канала'] == message.forward_from_chat.id):
                    text += " канал"+ str(row['Тег канала']) + " админа " + str(row['Тег админа']) 
            for index, row in chats.iterrows():
                bot.send_message(chat_id = row['id'], text = text)
bot.polling(none_stop=True)
