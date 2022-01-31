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
def add_channel_id_by_post(message):
    try:
        args =  message.text.split("?")
        dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
        df = pd.read_excel('Book.xlsx', index_col=0, engine='openpyxl')
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
def add_channel_id_by_message(message):
    try:
        args =  message.text.split("?")
        dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
        df = pd.read_excel('Book.xlsx', index_col=0)
        for index, row in df.iterrows():
            if row['id канала'] == args[1]:
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
        
@bot.message_handler(commands=['addAdmin'])
def add_admin(message):
    try:
        dropbox_download_file("/hitler-bot/Admins.xlsx", "Admins.xlsx")    
        admins = pd.read_excel("Admins.xlsx", index_col= 0, engine='openpyxl')
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

@bot.message_handler(commands=['editChannelTag'])
def edit_channel_tag(message):
    try:
        args = message.text.split("?")
        dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
        df = pd.read_excel('Book.xlsx', index_col=0)
        for index, row in df.iterrows():
            print(row['id канала'])
            print(str(args[1]) + '\n')
            print(args[2])
            print("I AM IN FOR")
            if (str(row['id канала']).replace(' ', '') == str(args[1]).replace(' ', '')):
                print("FOUND ID")
                df.at[index,'Тег канала'] = args[2]
                df.to_excel("Book.xlsx", sheet_name = "channels")
                dbx = dropbox_connect()
                dbx.files_delete("/hitler-bot/Book.xlsx")
                dropbox_upload_file("Book.xlsx", "/hitler-bot/Book.xlsx")
                bot.send_message(message.chat.id, text = "Операция успешна")
                return
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['editChannelTitle'])
def edit_channel_title(message):
    args = message.text.split("?")
    dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
    df = pd.read_excel('Book.xlsx', index_col=0)
    try:
        for index, row in df.iterrows():
            if (str(row['id канала']).replace(' ', '') == str(args[1]).replace(' ', '')):
                df.at[index,'Название канала'] = args[2]
                df.to_excel("Book.xlsx", sheet_name = "channels")
                dbx = dropbox_connect()
                dbx.files_delete("/hitler-bot/Book.xlsx")
                dropbox_upload_file("Book.xlsx", "/hitler-bot/Book.xlsx")

                bot.send_message(message.chat.id, text = "Операция успешна")
                return
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['editAdminTag'])
def edit_admin_tag(message):
    args = message.text.split("?")
    dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
    df = pd.read_excel('Book.xlsx', index_col=0)
    try:
        for index, row in df.iterrows():
            if (str(row['id канала']).replace(' ', '') == str(args[1]).replace(' ', '')):
                df.at[index,'Тег админа'] = args[2]
                df.to_excel("Book.xlsx", sheet_name = "channels")
                dbx = dropbox_connect()
                dbx.files_delete("/hitler-bot/Book.xlsx")
                dropbox_upload_file("Book.xlsx", "/hitler-bot/Book.xlsx")

                bot.send_message(message.chat.id, text = "Операция успешна")
                return
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['editAdminTitle'])
def edit_admin_title(message):
    args = message.text.split("?")
    dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
    df = pd.read_excel('Book.xlsx', index_col=0)
    try:
        for index, row in df.iterrows():
            if (str(row['id канала']).replace(' ', '') == str(args[1]).replace(' ', '')):
                df.at[index,'Имя админа'] = args[2]
                df.to_excel("Book.xlsx", sheet_name = "channels")
                dbx = dropbox_connect()
                dbx.files_delete("/hitler-bot/Book.xlsx")
                dropbox_upload_file("Book.xlsx", "/hitler-bot/Book.xlsx")
                bot.send_message(message.chat.id, text = "Операция успешна")
                return
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

@bot.message_handler(commands=['editCategory'])
def edit_category(message):
    args = message.text.split("?")
    dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
    df = pd.read_excel('Book.xlsx', index_col=0)
    try:
        for index, row in df.iterrows():
            if (str(row['id канала']).replace(' ', '') == str(args[1]).replace(' ', '')):
                df.at[index,'Категория'] = args[2]
                df.to_excel("Book.xlsx", sheet_name = "channels")
                dbx = dropbox_connect()
                dbx.files_delete("/hitler-bot/Book.xlsx")
                dropbox_upload_file("Book.xlsx", "/hitler-bot/Book.xlsx")
                bot.send_message(message.chat.id, text = "Операция успешна")
                return
    except:
        bot.send_message(message.chat.id, text = "Произошла ошибка!")

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

        
@bot.message_handler(commands=['link'])
def list_channels(message):
    link = "https://www.dropbox.com/sh/zhjlyve0ak9lpn6/AAATEZLXs00tUowdEpZdP6mua?dl=0"
    bot.send_message(message.chat.id, text = link)
@bot.message_handler(commands=['list'])
def list_channels(message):
    strrrr = ""
    dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
    df = pd.read_excel('Book.xlsx', index_col=0)
    df = df.drop(columns=['id канала'])
    for i in range(0, df.shape[0]):
         strr = df.iloc[i].to_string()
         strrr = ' '.join(strr.split()) + '\n' + '\n'
         strrr = strrr.replace('Название канала', ' ')
         strrr = strrr.replace('Тег админа', '\nАдмин - ')
         strrr = strrr.replace('Имя админа', ' ')
         strrr = strrr.replace('Тег канала', 'Канал ')
         strrr = strrr.replace('Категория', '\nКатегории:')
         strrrr += strrr
#         strr = df.to_string()
#         strrr = ' '.join(strr.split())
    bot.send_message(message.chat.id, text = strrrr)
#     except:
#         bot.send_message(message.chat.id, text = "Произошла ошибка!")
 
@bot.message_handler(commands = ['help'])
def help(message):
    message1 = "Порядок действий: \n" 
    message2 = "1. Добавить бота на каналы и сделать админом \n" 
    message3 = "2. / addChannel ? @тег админа ? имя админа ? категория канала \n" 
    message4 = "ИЛИ \n переслать пост с канала боту в лс \n \n \n" 
    message5 = "/ addChannel ? @тег админа ? имя админа ? категория канала - добавить КАНАЛ в список"
    message6 = "/ addChat - добавить ЧАТ для рассылки (нужно быть суперадмином) \n"
    message7 = "/ addAdmin - добавить суперадмина \n"
    message8 = "/ edit... ? id ? новое значение - изменить соответствующий параметр канала с id \n"
    message9 = "/ delChannel <id> - удалить канал, нужно быть суперадмином (можно на канале без использования id) \n" 
    message10 = "/ delChat - удалить текущий чат (нужно быть суперадмином) \n" 
    message11 = "/ getId - внутри чата, получить свой текущий id, на канале - id канала \n" 
    message12 = "/ link - ссылка на базу данных \n"  
    message13 = "/ list - список каналов \n" 
    text = message1 + message2 + message3 + message4 + message5 + message6 + message7 + message8 + message9 + message10 + message11
    bot.send_message(message.chat.id, text = text)

@bot.message_handler(commands=['getId'])
def get_user_id(message):
    bot.send_message(message.chat.id, str(message.from_user.id))


@bot.channel_post_handler(commands=['getId'])
def get_channel_id(message):
    bot.send_message(message.chat.id, str(message.chat.id))        
# dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
# df = pd.DataFrame(columns=['id канала', 'Тег канала', 'Название канала', 'Тег админа', 'Имя админа', 'Категория'])
# df.loc[df.shape[0]] = ['0', '0', '0', '0', '0', '0']
# temp = df.to_excel("Book.xlsx")
# dbx = dropbox_connect()
# dbx.files_delete("/hitler-bot/Book.xlsx")
# dropbox_upload_file("Book.xlsx", "/hitler-bot/Book.xlsx")


@bot.channel_post_handler(content_types=["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact", "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo", "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id", "migrate_from_chat_id" , "pinned_message"])
def reposts(message):
    text = ""
#     print(str(message.forward_from_chat.id))
    dropbox_download_file("/hitler-bot/Chats.xlsx", "Chats.xlsx")
    dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
    channels = pd.read_excel('Book.xlsx', index_col=0)
    chats = pd.read_excel('Chats.xlsx', index_col=0)
#     print("")
    if message.forward_from_chat != None:
        print("FIRST IF")
        if (channels['id канала'].isin([message.forward_from_chat.id]).any()):
            print("SECOND IF")
            for index, row in channels.iterrows():
                if(row['id канала'] == message.chat.id):
                    print("THIRD IF")
                    text += str(row['Тег админа']).replace(' ', '') + " " + str(row['Тег канала']).replace(' ', '') + " репостнул "
            for index, row in channels.iterrows():
                if(row['id канала'] == message.forward_from_chat.id):
                    print("FOURTH IF")
                    text += str(row['Тег канала']).replace(' ', '') + " " + str(row['Тег админа']).replace(' ', '')
            for index, row in chats.iterrows():
                print("FIFTH IF")
                bot.send_message(chat_id = row['id'], text = text)
@bot.message_handler(content_types=["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact", "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo", "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id", "migrate_from_chat_id" , "pinned_message"])        
def add_channel_id_by_forward(message):        
    if (message.forward_from_chat != None and message.chat.type == 'private'):
        dropbox_download_file("/hitler-bot/Book.xlsx", "Book.xlsx")
        df = pd.read_excel('Book.xlsx', index_col=0)
        for index, row in df.iterrows():
            if row['id канала'] == message.forward_from_chat.id:
                bot.send_message(message.chat.id, text = "Канал уже добавлен!")
                return
        channel_id = message.forward_from_chat.id
        channel_tag = "@" + str(message.forward_from_chat.username)
        channel_title = message.forward_from_chat.title
        admin_tag = message.from_user.username
        print(message.from_user.first_name)
        print( message.from_user.last_name)
        admin_title = message.from_user.first_name   
        df.loc[df.shape[0]] = [channel_id, channel_tag, channel_title, admin_tag, admin_title, "Empty"]    
        df.to_excel("Book.xlsx", sheet_name = "channels")
        dbx = dropbox_connect()
        dbx.files_delete("/hitler-bot/Book.xlsx")
        dropbox_upload_file("Book.xlsx", "/hitler-bot/Book.xlsx") 
        bot.send_message(message.chat.id, text = "Операция успешна")
        print(df)
#     except:
#     bot.send_message(message.chat.id, text = "Произошла ошибка!")                        
                
bot.polling(none_stop=True)


