# # -*- coding: utf-8 -*-
# #from __future__ import unicode_literals
# import telepot
# import os
# import pickle
# from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
# from pprint import pprint
#
#
# #the main list that contains all messages
# data_list = list()
#
# #list of all the information of users who have sent a message
# user_list = list()
#
# #list of chats requested investigation
# investigation_list = list()
#
#
#
# #a class with 3 attributes: count(for number of repeats), text(for every words in the message)
# #and id(for the message sender)
# class AllMessages:
#     def __init__(self, count, text, id):
#         self.count = int(count)
#         self.text = text
#         self.id = id
#         print("allmessage is creating")
#
#     def showdetails(self):
#         print("details: ")
#         print(self.count)
#         print(self.text)
#         print(self.id)
#
# #open the file and read the corpse from it, or if the file does not exits; data_list should be created as an empty list
# if  os.path.exists('corpse_file.txt'):
#     with open("corpse_file.txt", "rb") as fp:
#         data_list = pickle.load(fp)
#
#
#
# #open the file and read the ids from it, or if the file does not exits; user_list should be created as an empty list
# if  os.path.exists('people_file.txt'):
#     with open("people_file.txt", "rb") as fp:
#         user_list = pickle.load(fp)
#
#
#
#
# #a function that will execute the probability of sending the message by each user
# def Investigate(message):
#     message[u"text"] = message[u"text"].replace(","," ")
#     message[u"text"] = message[u"text"].replace("."," ")
#     message[u"text"] = message[u"text"].replace("?"," ")
#     message[u"text"] = message[u"text"].replace("!"," ")
#     message[u"text"] = message[u"text"].replace(":"," ")
#     message[u"text"] = message[u"text"].replace("("," ")
#     message[u"text"] = message[u"text"].replace(")"," ")
#
#     #a list of all the words in the text and number of its uses in corpse and id of users
#     extract_list = list()
#
#     anonymous_msg = message[u"text"].split()
#     #for each word, we will check the corpes for same and store the counts of it by each id
#     for word in anonymous_msg:
#         temp_list = list()
#         temp_list.append(word.encode('UTF-8'))
#         for item in data_list:
#             if(item.text == word.encode('UTF-8')):
#                 temp_list.append([item.id, item.count])
#
#         #for each user that has not been using this word, set the count 0
#         for user in user_list:
#             if user[0] not in [row[0] for row in temp_list]:
#                 temp_list.append([user[0], 0])
#
#         extract_list.append(temp_list)
#
#     pprint(extract_list)
#
#     #here we will compute counts of each word despite of its user
#     N_list = list()
#
#     for List in extract_list:
#         N = 0
#         if(len(List) > 1):
#             for i in range(1,len(List)):
#                 N = N + List[i][1]
#         N_list.append([List[0], N])
#
#     pprint(N_list)
#
#     #a list that contains all the words in the corpse without repeat
#     V_list = list()
#     for word in data_list:
#         if word.text not in V_list:
#             V_list.append(word.text)
#
#     #number of words in the corpse without repeat
#     v = len(V_list) + 1
#
#     #now we will compute probability of using each word by every users by dividing counts by N
#     p_list = list()
#
#     for n_list in N_list:
#         tmp_list = list()
#         tmp_list.append(n_list[0])
#         n = n_list[1]
#         for e_list in extract_list:
#             if(e_list[0] == n_list[0]):
#                 for i in range(1,len(e_list)):
#                     #handling zero count
#                     x = (e_list[i][1] + 1) / (v + float(n))
#                     tmp_list.append([e_list[i][0], x])
#                 break
#         p_list.append(tmp_list)
#
#     pprint(p_list)
#
#     #here we will compute probability of each user sending the message and sort the list from max to min
#     p_total = list()
#
#     for id in user_list:
#         p = 1
#         for word in p_list:
#             for i in range(1,len(word)):
#                 if(word[i][0] == id[0]):
#                     p = p * word[i][1]
#         p_total.append([p, id[0], id[1], id[2], id[3]])
#         p_total = sorted(p_total, key = lambda x: x[0], reverse = True) # sort from mux to min
#
#     pprint(p_total)
#
#     #here we will return the 3 most possible senders (the first 3 of the p_total list)
#     if(len(p_total) > 3):
#         return(p_total[0:3])
#     else:
#         return p_total
#
#
#
# #every time a message in recieved; this function starts performing
# def HandleChat(msg):
#     content_type, chat_type, chat_id = telepot.glance(msg)
#     print ("msg:")
#     pprint(str(telepot.glance(msg)))
#     pprint(msg)
#     message = msg[u"text"] #extracting the text of message
#     pprint(message)
#
#     # creating a keyboard
#     main_keyboard = {'keyboard': [["about", "contact us"], ["investigate"]], \
#                      'one_time_keyboard': True, \
#                      'resize_keyboard': True}
#
#     #if someone send the message wants to investigate on, after requesting investigation
#     if chat_id in investigation_list:
#
#         investigation_list.remove(chat_id)
#
#         #use this method when you need to tell the user that something is happening on the bot's side
#         TelegramBot.sendChatAction(chat_id, 'typing')
#
#         suspect_list = list()
#         suspect_list = Investigate(msg)
#
#         TelegramBot.sendMessage(chat_id, "<b>here's the 3 most possible senders:</b>",
#                                 reply_markup = main_keyboard, parse_mode = 'html')
#         n = 1
#         for suspect in suspect_list:
#             TelegramBot.sendMessage(chat_id, "<b>{}. {}, {}, {} </b>\n".format(n, suspect[2], suspect[3].encode('UTF-8'), suspect[4].encode('UTF-8')),
#                                     reply_markup = main_keyboard, parse_mode = 'html')
#             n += 1
#
#
#
#
#
#     else:
#         #when someone send the '/start' message; the bot will show them this message
#         if message == '/start':
#             TelegramBot.sendMessage(chat_id, "<b>Welcome!</b>\n"
#                                              "<b>Here you can know all the anonymous message senders.</b>\n"
#                                              "<b>Just press the investigate button to proceed...</b>", \
#                                              reply_markup = main_keyboard, parse_mode = 'html')
#
#         #when someone press the 'about' button; the bot will answer them as shown below
#         elif message == 'about':
#             Bot = InlineKeyboardButton(text = "Bot", callback_data = "Bot")
#             Institution = InlineKeyboardButton(text = "Institution", callback_data = "Institution")
#             Developers = InlineKeyboardButton(text = "Developers", callback_data = "Developers")
#             nested_list = [[Bot],[Institution], [Developers]]
#             my_inline_keyboard = InlineKeyboardMarkup(inline_keyboard = nested_list)
#             TelegramBot.sendMessage(chat_id, "What do you want to know about?", reply_markup = my_inline_keyboard, parse_mode = 'markdown')
#
#         #when someone press the 'contact us' button; the bot will show them some e-mail contacts
#         elif message == 'contact us':
#             TelegramBot.sendMessage(chat_id, "<b>Here is some e-mail addresses to contact us:</b>\n"
#                                              "<b>azade.alizade96@gmail.com</b>\n"
#                                              "<b>m.eslami46@gmail.com</b>", \
#                                              reply_markup = main_keyboard, parse_mode = 'html')
#
#         #in progress
#         elif message == 'investigate':
#             TelegramBot.sendMessage(chat_id, "<b>please send the message you want to investigate</b>\n" , parse_mode = 'html')
#             if chat_id not in investigation_list:
#                 investigation_list.append(chat_id)
#
#
#         #if someone send any other messages; the bot will save them as evidence
#         else:
#             #check if this id is a new message sender, add its information to user_list
#             tmp_value1 = msg.get('forward_from', "Not Forwarded")
#             tmp_value2 = msg[u"from"]
#             tmp_list = list()
#             #if the message is forwarded, the real sender is the one who has sent the original message
#             if(tmp_value1 == "Not Forwarded"):
#                 tmp_list.append(tmp_value2.get('id'))
#                 tmp_list.append(tmp_value2.get('username' , "Null"))
#                 tmp_list.append(tmp_value2.get('first_name' , "Null"))
#                 tmp_list.append(tmp_value2.get('last_name' , "Null"))
#             else:
#                 tmp_list.append(tmp_value1.get('id'))
#                 tmp_list.append(tmp_value1.get('username' , "Null"))
#                 tmp_list.append(tmp_value1.get('first_name' , "Null"))
#                 tmp_list.append(tmp_value1.get('last_name' , "Null"))
#
#             if tmp_list not in user_list:
#                 user_list.append(tmp_list)
#
#             print (user_list)
#
#             #save the users in the file
#             with open("people_file.txt", "wb") as fp:
#                 pickle.dump(user_list, fp)
#
#             #first we will delete marks so the word Hello and Hello! won't be different
#             msg[u"text"] = msg[u"text"].replace(","," ")
#             msg[u"text"] = msg[u"text"].replace("."," ")
#             msg[u"text"] = msg[u"text"].replace("?"," ")
#             msg[u"text"] = msg[u"text"].replace("!"," ")
#             msg[u"text"] = msg[u"text"].replace(":"," ")
#             msg[u"text"] = msg[u"text"].replace("("," ")
#             msg[u"text"] = msg[u"text"].replace(")"," ")
#             #now we split the message to have all the words in it
#             msg_split = msg[u"text"].split()
#
#             #now for every word, we will compute counts of it(by spesific sender), text of it and id of sender
#             for word in msg_split:
#                 detail = AllMessages(1, " ", " ") #for all words, we will construct a class with count 1 and the other attributes' null
#                 detail.text = word.encode('UTF-8') #encode persian texts
#                 #if the message is forwarded, get the real sender's ID
#                 if(tmp_value1 == "Not Forwarded"):
#                     detail.id = tmp_value2.get('id')
#                 else:
#                     detail.id = tmp_value1.get('id')
#
#                 isNew = True
#                 count = 0
#                 itemNum = 0
#
#                 #if this word is not included in the main list, isNew will be True
#                 for i in range(len(data_list)):
#                     item = data_list[i]
#                     if (item.text == detail.text and item.id == detail.id):
#                         isNew = False
#                         itemNum = i
#                         count = item.count
#                         break
#
#                 #if this word is not included in the main list, add it to the list
#                 if isNew:
#                     data_list.append(detail)
#                 #if this word is included in the main list, increase its count by 1
#                 else:
#                     detail.count = count + 1
#                     data_list[itemNum] = detail
#
#             print("\ngetallmessage def: \n")
#             for i in data_list:
#                 print( "(count = %d, text = %s, id = %d)" %(i.count, i.text, i.id))
#
#             #save the data in the file
#             with open("corpse_file.txt", "wb") as fp:
#                 pickle.dump(data_list, fp)
#
#
#
# #a function to handle the buttons
# def HandleCallback(msg):
#     main_keyboard = {'keyboard': [["about", "contact us"], ["investigate"]], \
#                      'one_time_keyboard': True, \
#                      'resize_keyboard': True}
#
#
#     query_id, from_id, query_data = telepot.glance(msg, flavor = "callback_query")
#     if query_data == "Bot":
#         TelegramBot.sendMessage(from_id, "<b>a bot that can recognize digital hand-writing (determines the writer of a specific message)</b>", reply_markup = main_keyboard, parse_mode = 'html')
#
#     elif query_data == "Institution":
#         TelegramBot.sendMessage(from_id, "<b>University of Tehran, College of Farabi!</b>", reply_markup = main_keyboard, parse_mode = 'html')
#
#     elif query_data == "Developers":
#         TelegramBot.sendMessage(from_id, "<b>Azade FirouzAlizade, Maryam Sadat Eslami!</b>", reply_markup = main_keyboard, parse_mode = 'html')
#
#
#
# token = '669710756:AAHJMMUNgF8atcnp1mrRNMck3-6u82kwvYI'
# TelegramBot = telepot.Bot(token)
# TelegramBot.message_loop({'chat':HandleChat, 'callback_query':HandleCallback})
# while True:
#     pass
import time
from os import path
from random import randint
from requests import get
from random import randint
from time import sleep
from json import loads
from os import path, mkdir

import telepot

token = '669710756:AAHJMMUNgF8atcnp1mrRNMck3-6u82kwvYI'
TelegramBot = telepot.Bot(token)


# print(TelegramBot.getMe())
# print(TelegramBot.getUpdates())

def get_file_path(token, file_id):
    get_path = get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(token, file_id))
    json_doc = loads(get_path.text)
    try:
        file_path = json_doc['result']['file_path']
    except Exception as e:  # Happens when the file size is bigger than the API condition
        print(e)
        # bot.sendMessage(chat_id, 'Failed for {}'.format(singer, song_name))
        return None

    return 'https://api.telegram.org/file/bot{}/{}'.format(token, file_path)


def get_file(msg_list, chat_id):
    if len(msg_list) > 1:
        msg_count = len(msg_list)
        print('Total files: {}'.format(msg_count))

    for msg in msg_list:
        print(msg)
        try:
            oggid = msg['message']['voice']['file_id']
        except KeyError:
            continue

        try:
            singer = msg['message']['voice']['performer']
        except:
            singer = 'Unknown'

        # Remove / and - characters to create directory
        singer_dir = singer.replace('/', '-').strip()

        try:
            song_name = msg['message']['voice']['title']
        except:
            song_name = str(randint(120, 1900000000))

        if path.exists('{}/{}_{}.ogg'.format(singer_dir, singer, song_name)):
            print('{} {} --> File exists'.format(singer, song_name))
            continue

        print('Working on --> {} {}'.format(singer, song_name))
        # Get file download path
        download_url = get_file_path(token, oggid)
        oggfile = get(download_url)

        if not path.exists(singer_dir):
            mkdir(singer_dir)

        try:
            with open('{}/{}_{}.ogg'.format(singer_dir, singer, song_name), 'wb') as f:
                f.write(oggfile.content)
        except FileNotFoundError:
            with open('{}.ogg'.format(randint(120, 1900000000)), 'wb') as f:
                f.write(oggfile.content)

        bot.sendMessage(chat_id, 'Done: {} {}'.format(singer, song_name))


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    usermsg = bot.getUpdates(allowed_updates='message')
    get_file(usermsg, chat_id)


def main():
    bot.message_loop(handle)
    # Keep the program running
    while 1:
        time.sleep(20)


if __name__ == '__main__':
    bot = telepot.Bot(token)
    main()
