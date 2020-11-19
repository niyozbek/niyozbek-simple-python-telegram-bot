#python3, text-to-speach, telegram-bot-api, simple responsive bot
from dotenv import load_dotenv   #for python-dotenv method
import requests, json, os, threading, pyttsx3

load_dotenv()                    #for python-dotenv method

YOURAPIKEY = os.environ.get('YOURAPIKEY')

URL = f"https://api.telegram.org/bot{YOURAPIKEY}/"

session = {}

def index():
    
    response = requests.get(URL + "getUpdates")
    get_updates = response.json()  

    results = get_updates['result']
    if len(results) > 0:
        #not to send two responses
        if 'last_update_id' not in session:
            last_update_num = len(results)-1
            update = results[last_update_num]
            update_id = update['update_id']
            session['last_update_id'] = update_id
            # how to clean session
            # session.pop('username', None)
        else:
            #respond to all new messages, and save the last update_id to the session
            for update in results:
                update_id = update['update_id']
                if(update_id > session['last_update_id']):
                    print("new update")

                    message         = update['message']
                    chat_id         = message['chat']['id']
                    text            = message['text']
                    #first_name      = message['chat']['first_name']
                    first_name      = "Clement"
                    username        = message['chat']['username']
                    if (text in ["/start", "I love you"]):
                        if(text == "I love you"):
                            #extra logic
                            answer = "❤️"
                            requests.get(f'{URL}sendMessage?chat_id={chat_id}&text={answer}&parse_mode=HTML')
                            answer = f"I love you too {first_name}"
                            generateVoice(answer)
                            files = {'voice': open('voice.mp3','rb')}
                            print(requests.post(f'{URL}sendVoice?chat_id={chat_id}', files=files).json())
                        else:
                            answer = f"Hello {first_name} I am a chatbot coded with php."
                    else:
                        answer = "I don't know what u are trying to say, please say something like \n<b>I love you</b>"
                    response = requests.get(f'{URL}sendMessage?chat_id={chat_id}&text={answer}&parse_mode=HTML')
                    print(response.json())
                    session['last_update_id'] = update_id
    return 0


def runUpdate():
  threading.Timer(1.0, runUpdate).start()
  index()

runUpdate()


#for text-to-speach google
#from gtts import gTTS 
#import os

#online version - good quality, stable if used free
def generateVoiceGoogle(text):
    #free version breaks a lot, blocked by google if abused too much
    text = "I love you too niyozbek!"
    language = 'en'
    speech = gTTS(text = text, lang = language, slow = False)
    speech.save("voice.mp3")
    #os.system("mpg123 voice.mp3")

#offline version - low quality, stable
def generateVoice(text):
    engine = pyttsx3.init()
    #engine.setProperty('rate', 125)     # setting up new voice rate
    #engine.say("I will speak this text")
    engine.save_to_file(text, 'voice.mp3')
    engine.runAndWait()