import speech_recognition as sr
import googletrans
from googletrans import Translator
from gtts import gTTS
import os

#Class combining many libraries into one translator
class speechTranslator:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.translator = Translator()
    #input the text, text language, and language to translate to. 
    #outputs the translated text in that language
    def textToText(self, textToTranslate, fromLanguage, toLanguage):
        translatedText = self.translator.translate(textToTranslate, src=fromLanguage, dest=toLanguage)
        return translatedText.text
    #input the text and the language of the text
    #saves the mp3 and plays the audio
    def textToSpeech(self, textToSpeech, language):
        speech = gTTS(text=textToSpeech, lang=language, slow=False)
        speech.save("captured_voice.mp3")
        os.system("start captured_voice.mp3")
    #speak into the mic and stops when there is no input
    #sends google a request to turn it into text
    #returns the text of the speech
    def speechToText(self, stop_event):
        with self.microphone as source:
            #print("Listening...")
            while not stop_event.is_set():
                audio = self.recognizer.listen(source)
                try:
                    #print("Recognizing...")
                    text = self.recognizer.recognize_google(audio)
                    #print(f"Recognized Text: {text}")
                    return text
                except sr.RequestError:
                    print("Could not connect to Google Speech Recognition service")
                    return None
                except sr.UnknownValueError:
                    print("Unknown error occurred")
                    return None
    #gets the map of all the languages in the format needed
    def getAllLanguages(self):
        languages = {name: code for code, name in googletrans.LANGUAGES.items()}
        return languages
        
        