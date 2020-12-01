#python3, speech to text, telegram-bot-api, simple responsive bot

#1. record voice in telegram bot
#2. download and save this ogg file
#3. convert into .wav
#4. recognize .wav into text
#5. send to telegram bot as a response
#               
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
        engine.setProperty('rate', 125)     # setting up new voice rate

        # On linux make sure that 'espeak' and 'ffmpeg' are installed
        engine.save_to_file(text, 'tutorial4.mp3')
        engine.runAndWait()
        time.sleep(5)
        return 'tutorial4.mp3'

    def __setLastUpdate(self):
        #not to send two responses
        response = requests.get(self.__URL + "getUpdates").json()
        result = response['result']
        if len(result) > 0:
            self.__last_update_id = result[len(result)-1]['update_id']
            
    def __letters(self, input):
        return "".join([x for x in input if x.isalpha() or x == ' '])
        #return ''.join(filter(str.isalpha, input))

    def speechToText(self, file_name):
        import speech_recognition as sr 

        from os import path
        #pip3 install pydub
        from pydub import AudioSegment

        # files                                                                         
        src = f"{file_name}"
        dst = f"{file_name}.wav"

        # convert wav to mp3     
        # https://pythonbasics.org/convert-mp3-to-wav/                                                       
        sound = AudioSegment.from_ogg(src)
        sound.export(dst, format="wav")
        
        
        #https://pypi.org/project/SpeechRecognition/

        # Initialize the recognizer  
        r = sr.Recognizer()  

        AUDIO_FILE = f"{file_name}.wav"
        with sr.AudioFile(AUDIO_FILE) as source:
            audio2 = r.record(source)  # read the entire audio file
            #pip3 install pocketsphinx
            # Using ggogle to recognize audio 
            #MyText = r.recognize_google(audio2) 
            MyText = r.recognize_sphinx(audio2) 
            MyText = MyText.lower() 
            return MyText
        return -1
            
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

                    if("voice" in message):
                        print(message)

                        #https://api.telegram.org/file/bot<token>/<file_path>
                        #getFile file_id
                        
                        #for add. info
                        #https://core.telegram.org/bots/api

                        file_id = message['voice']['file_id']
                        getFile = requests.get(f'{self.__URL}getFile?file_id={file_id}').json()
                        file_path = getFile['result']['file_path']
                        voice_url = f"https://api.telegram.org/file/bot{self.__YOURAPIKEY}/{file_path}"
                        #print(voice_url)
                        #answer = f"You have just sent a voice: = {voice_url}"

                        #downloads the image frorm telegram
                        import urllib.request 
                        urllib.request.urlretrieve(voice_url, "tutorial4.ogg")
                        
                        ready_text = self.speechToText('tutorial4.ogg')

                        response = requests.get(f'{self.__URL}sendMessage?chat_id={chat_id}&text={ready_text}&parse_mode=HTML')

                        #send a voice message
                        file_name = self.generateVoice(ready_text)
                        files = {'voice': open(file_name, 'rb')}
                        print(requests.post(f'{self.__URL}sendVoice?chat_id={chat_id}', files=files).json())

        return 0

telegramBot = TelegramBot()
telegramBot.runUpdate()



