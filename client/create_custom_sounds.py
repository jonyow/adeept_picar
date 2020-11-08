

from gtts import gTTS
import os

language = 'en'

text = "Jackie spotted, Jackie spotted"
speech = gTTS(text = text, lang = language, slow = False)
speech.save('../sounds/jackie.mp3')

text = "jonny spotted, jonny spotted"
speech = gTTS(text = text, lang = language, slow = False)
speech.save('../sounds/jonny.mp3')

from pygame import mixer

mixer.init()
file = '../sounds/jackie.mp3'

mixer.music.load(file)
mixer.music.play()

