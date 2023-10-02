import configparser # pip install configparser
import telethon
from telethon import TelegramClient, events, Button # pip install telethon
import requests
import json
import telebot
from telethon.sync import TelegramClient, events
import pandas as pd
from io import StringIO
import csv
import mysql.connector
# Create a sample DataFrame





#url = "https://smsplus.sslwireless.com"
#response = requests.get(url)
#print("res: ", response.content)
### Initializing Configuration
print("Initializing configuration...")
config = configparser.ConfigParser()
config.read('config.ini')




API_ID = config.get('default','api_id') 
API_HASH = config.get('default','api_hash')
BOT_TOKEN = config.get('default','bot_token')
session_name = "sessions/Bot"


# Read values for MySQLdb
HOSTNAME = config.get('default','hostname')
USERNAME = config.get('default','username')
PASSWORD = config.get('default','password')
DATABASE = config.get('default','database')


# Start the Client (telethon)
client = TelegramClient(session_name, API_ID, API_HASH).start(bot_token=BOT_TOKEN)


r =requests.get("https://api.telegram.org/bot6121403424:AAE9VIKmd_eiOMbMKtpAHJ1jcrsDjdYlMrA/getUpdates")
#print(r.text)

chat_id = 1387217956



# reply_markup = ReplyKeyboardMarkup([[KeyboardButton('Employ'), KeyboardButton('Leave')],
#                                    [KeyboardButton('Attend'), KeyboardButton('Blood S')],
#                                    [KeyboardButton('HR Con'), KeyboardButton('Write a message...')]])
# bot.sendMessage(chat_id='1234567890', text='Menu:', reply_markup=reply_markup)


#print(chat_id)


# @client.on(events.NewMessage)
# async def handle_message(event):
#     if event.raw_text == "/help":
#         button1 = Button.inline("Guideline", b'button1_data')
#         #button2 = Button.inline("Button 2", b'button2_data')
        
#         #await event.respond("Choose an option:", buttons=[[button1, button2]])
#         await event.respond("know how to ask: ", buttons=[button1,])

# @client.on(events.CallbackQuery)
# async def callback_query(event):
#     if event.data == b'button1_data':
#         await event.respond('Incorrect format. Write down as following to get desired output: \n MSISDN"<SPACE>"FromDate[yyyy-mm-dd]"<SPACE>"Todate[yyyy-mm-dd]')
#     #elif event.data == b'button2_data':
#     #    await event.respond("You clicked Button 2!")
# ### START COMMAND



'''
@client.on(events.NewMessage(pattern="(?i)/start"))
async def start(event):
    # Get sender
    sender = await event.get_sender()
    SENDER = sender.id

    # set text and send message
    text = "Hello i am a bot that give you SMS Success or fail status\nWrite down as following to get desired output:\nMSISDN<SPACE>FromDate[yyyy-mm-dd]<SPACE>todate[yyyy-mm-dd]\n ex: 01712345678 2023-08-17 2023-08-17"
    await client.send_message(SENDER, text )

'''
def authenticate(chatid, username, request_details):
    cursor = None  # Initialize the cursor variable
    try:
        cursor = conn.cursor()
        #if result is None or len(result) >= 3:
        chatid = str(chatid)
        username = str(username)
        request_details = str(request_details)
        #to track all queries of users    
        insert_query = "INSERT INTO logs (chatid, username, requestDetails) VALUES (%s, %s, %s)"
        val = (chatid, username, request_details)
        cursor.execute(insert_query, val)
        #to check if the user exists or not
        query = "SELECT * FROM smsbot WHERE chatid = %s"
        cursor.execute(query, (chatid,))
        result = cursor.fetchone()
        conn.commit()
        print("credentials: ", result)

        if result is not None and len(str(result)) >= 3:

            if str(result[2]) == str(chatid):
                print(f"Chat ID {chatid} exists in the database.")
                return True
            else:
                print(f"Chat ID {chatid} does not exist in the database.")
                return False
        else:
            return False
        
        
    
    except Exception as e:
        print(f"Error: {e}")
        return False    

    # finally:
    #     if cursor:
    #         cursor.close()  # Close the cursor only if it's not None
    #     conn.close()

        

#@client.on(events.NewMessage(pattern="(?i)/send"))
@client.on(events.NewMessage(pattern=""))
async def start(event):
    # Get sender
    
    sender = await event.get_sender()
    SENDER = sender.id
    sendername = sender.username
    print("CHATID", SENDER)
    print("senderrrrrrrrrrrrrrrrrrrrname: ", sendername)
    
    loggin = authenticate(SENDER, sendername, event.message.text)
    
    if loggin == True:
        list_of_params = event.message.text.split()
        
        #print(event.message.text)
        Dict = {}
        if len(list_of_params ) == 4: 
            
            record = {
                "msisdn": list_of_params[0],
                "from_date": list_of_params[1],
                "to_date": list_of_params[2],
                "masking": list_of_params[3]
            }
            #Dict = record
            #url = "http://127.0.0.1:8080/smsai/v1?msisdn="+list_of_params[1]+"&fsmstime="+list_of_params[2]+"&tsmstime="+list_of_params[3]
            url = "http://127.0.0.1:8080/smsai/v1?msisdn="+list_of_params[0]+"&from_date="+list_of_params[1]+"&to_date="+list_of_params[2]+"&masking="+list_of_params[3]

        # print("record: ", record)
        
            response = requests.get(url)
            
            # Sending a GET request with parameters
            #response = requests.post(url,  data = record) 
    
            # set text and send message
            if response.status_code == 200:
                msg = response.content.decode('utf-8')
                
                # Split the multi-line string into a list of lines
                i = 0
                lines = msg.split('\t')
                await client.send_message(SENDER, "<b>LOG INFORMATION WITH MASKING.</b>\n", parse_mode='html')
                #print(lines)
                
                for line in lines:  
                    #print(line)
                    i = i + 1
                    await client.send_message(SENDER,  str(i) + ". "+ line, parse_mode='html')
                await client.send_message(SENDER, "Response ended.")   

        elif len(list_of_params ) == 3: 
            masking='1'
            url = "http://127.0.0.1:8080/smsai/v1?msisdn="+list_of_params[0]+"&from_date="+list_of_params[1]+"&to_date="+list_of_params[2]+"&masking="+masking
            response = requests.get(url)
            if response.status_code == 200:
                msg = response.content.decode('utf-8')
                print(response.content)
                # Split the multi-line string into a list of lines
                i = 0
                lines = msg.split('\t')
                await client.send_message(SENDER, "LOG INFORMATION.\n")
                #print(lines)
                
                for line in lines:  
                    #print(line)
                    i = i + 1
                    await client.send_message(SENDER,  str(i) + ". "+ line, parse_mode='html')
                await client.send_message(SENDER, "Response ended.")
        else:
            text= "Incorrect format. Write down as following to get desired output:\nMSISDN<SPACE>FromDate[yyyy-mm-dd]<SPACE>todate[yyyy-mm-dd]<SPACE>MASKING\nIf there is any space between masking name, use + only.\nex: 01712345678 2023-08-17 2023-08-18 SSL"
            await client.send_message(SENDER, text)
    else:
        text = "You are not permitted to use this bot! Please contact to Administrator to register"
        await client.send_message(SENDER, text) 



##### MAIN
if __name__ == '__main__':
    try:
        
        conn = mysql.connector.connect(
        host=HOSTNAME, 
        user=USERNAME, 
        passwd=PASSWORD, 
        database= DATABASE )
        if conn.is_connected():
            print("Connected to MySQL database")
            cursor = conn.cursor()
            client.start()
            print("Bot Started...")
            client.run_until_disconnected()
        
    except Exception as error:
        print('Cause: {}'.format(error))
