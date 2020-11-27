#python3, image-to-text, telegram-bot-api, simple responsive bot
from dotenv import load_dotenv   #for python-dotenv method
import requests, json, os, threading, pyttsx3, time

load_dotenv()                    #for python-dotenv method

class TelegramBot:
    def __init__(self):
        self.__YOURAPIKEY = os.environ.get('YOURAPIKEY')
        self.__URL = f"https://api.telegram.org/bot{self.__YOURAPIKEY}/"
        self.__last_update_id = 0
        self.__setLastUpdate()
    
    def runUpdate(self):
        #process updates every 3 seconds
        threading.Timer(3.0, self.runUpdate).start()
        self.index()

    #online version is provided by google cloud services and not free
        #use paid services for commercial projects
        #https://scriptverse.academy/tutorials/python-text-to-speech.html
    #offline version - low quality, but stable
        #use offline version for testing purposes
    def generateVoice(self, text):
        #https://pypi.org/project/pyttsx3/
        engine = pyttsx3.init()
        # On linux make sure that 'espeak' and 'ffmpeg' are installed
        engine.save_to_file(text, 'tutorial3.mp3')
        engine.runAndWait()
        time.sleep(5)
        return 'tutorial3.mp3'

    def __setLastUpdate(self):
        #not to send two responses
        response = requests.get(self.__URL + "getUpdates").json()
        result = response['result']
        if len(result) > 0:
            self.__last_update_id = result[len(result)-1]['update_id']
            
    def __letters(self, input):
        return "".join([x for x in input if x.isalpha() or x == ' '])
        #return ''.join(filter(str.isalpha, input))

    def index(self):
        offset = self.__last_update_id + 1

        response = requests.get(self.__URL + "getUpdates?offset={offset}").json()
        result = response['result']

        if len(result) > 0:
            #respond to all new messages, and save the last update_id to the session
            for update in result:
                update_id = update['update_id']
                if(update_id > self.__last_update_id):
                    #line below should be here, otherwise bot sends us more than one replies, 
                    # because code doesn't catch up with the logic sometimes 
                    self.__last_update_id = update_id
                    #print("new update")

                    message         = update['message']
                    chat_id         = message['chat']['id']
                    first_name      = message['chat']['first_name']
                    username        = message['chat']['username']

                    if("photo" in message):
                        #https://api.telegram.org/file/bot<token>/<file_path>
                        #getFile file_id
                        file_id = message['photo'][len(message['photo'])-1]['file_id']
                        getFile = requests.get(f'{self.__URL}getFile?file_id={file_id}').json()
                        file_path = getFile['result']['file_path']
                        photo_url = f"https://api.telegram.org/file/bot{self.__YOURAPIKEY}/{file_path}"
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
                        
                        ready_text = self.__letters(pytesseract.image_to_string(Image.open("image.png")))

                        response = requests.get(f'{self.__URL}sendMessage?chat_id={chat_id}&text={ready_text}&parse_mode=HTML')
                       
                        file_name = self.generateVoice(ready_text)
                        
                        files = {'voice': open(file_name, 'rb')}
                        #send a voice message
                        print(requests.post(f'{self.__URL}sendVoice?chat_id={chat_id}', files=files).json())

        return 0

telegramBot = TelegramBot()
telegramBot.runUpdate()



