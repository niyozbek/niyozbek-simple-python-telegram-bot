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
                    #line below should be here, otherwise bot sends us more than one replies, 
                    # because code doesn't catch up with the logic sometimes 
                    session['last_update_id'] = update_id
                    #print("new update")

                    message         = update['message']
                    chat_id         = message['chat']['id']
                    first_name      = message['chat']['first_name']
                    username        = message['chat']['username']

                    if("text" in message):
                        text            = message['text']
                        if (text in ["/start", "I love you"]):
                            if(text == "I love you"):
                                #extra logic
                                #send a big heart
                                answer = "❤️"
                                requests.get(f'{URL}sendMessage?chat_id={chat_id}&text={answer}&parse_mode=HTML')
                                #send i love you back message
                                answer = f"I love you too {first_name}"
                                if(generateVoice(answer)):
                                    files = {'voice': open('voice.mp3','rb')}
                                    #send a voice message
                                    print(requests.post(f'{URL}sendVoice?chat_id={chat_id}', files=files).json())
                            else:
                                answer = f"Hello {first_name} I am a chatbot coded with php."
                        else:
                            answer = "I don't know what u are trying to say, please say something like \n<b>I love you</b>"
                        response = requests.get(f'{URL}sendMessage?chat_id={chat_id}&text={answer}&parse_mode=HTML')
                        print(response.json())
                    elif("photo" in message):
                        #https://api.telegram.org/file/bot<token>/<file_path>
                        #getFile file_id
                        file_id = message['photo'][len(message['photo'])-1]['file_id']
                        getFile = requests.get(f'{URL}getFile?file_id={file_id}').json()
                        file_path = getFile['result']['file_path']
                        photo_url = f"https://api.telegram.org/file/bot{YOURAPIKEY}/{file_path}"
                        #print(photo_url)
                        answer = f"You have just sent a photo: = {photo_url}"
                        #https://linuxhint.com/install-tesseract-ocr-linux/

                        #https://pypi.org/project/pytesseract/
                        try:
                            from PIL import Image
                        except ImportError:
                            import Image
                        import pytesseract

                        # Simple image to string
                        import urllib.request 
                        urllib.request.urlretrieve(photo_url, "image.png")
                        
                        ready_text = letters(pytesseract.image_to_string(Image.open("image.png")))

                        response = requests.get(f'{URL}sendMessage?chat_id={chat_id}&text={ready_text}&parse_mode=HTML')
                        
                        if(generateVoice(ready_text)):
                            files = {'voice': open('voice.mp3','rb')}
                            #send a voice message
                            print(requests.post(f'{URL}sendVoice?chat_id={chat_id}', files=files).json())
    return 0

def letters(input):
    return "".join([x for x in input if x.isalpha() or x == ' '])
    #return ''.join(filter(str.isalpha, input))

def runUpdate():
  threading.Timer(1.0, runUpdate).start()
  index()

runUpdate()


#for text-to-speach google
#from gtts import gTTS 
#import os


#offline version - low quality, stable
def generateVoice(text):
    engine = pyttsx3.init()
    #engine.setProperty('rate', 125)     # setting up new voice rate
    #engine.say("I will speak this text")
    engine.save_to_file(text, 'voice.mp3')
    #actually saves the file and waits
    engine.runAndWait()
    return engine