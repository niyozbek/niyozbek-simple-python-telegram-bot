#https://linuxhint.com/install-tesseract-ocr-linux/
#https://pypi.org/project/pytesseract/

#By default Tesseract will install the English language pack, to install additional languages run
    #sudo apt-get install tesseract-ocr-LANG

#for example, to add Hebrew:
    #sudo apt-get install tesseract-ocr-heb

#You can include all languages by running:
    #sudo apt-get install tesseract-ocr-all

#pip3 install pytesseract


try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

from gtts import gTTS 
import os, pyttsx3

#offline version - low quality, stable
def generateVoice(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)     # setting up new voice rate
    #engine.say("I will speak this text")
    engine.save_to_file(text, 'voice.mp3')
    engine.runAndWait()

def letters(input):
    return "".join([x for x in input if x.isalpha() or x == ' '])
    #return ''.join(filter(str.isalpha, input))

# Simple image to string
text = (pytesseract.image_to_string(Image.open('google_play.png'), lang='eng'))
print(letters(text))
generateVoice(text)


