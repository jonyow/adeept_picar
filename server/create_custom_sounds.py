
from gtts import gTTS
import os

from pygame import mixer
mixer.init()

CACHE_FOLDER = '../sounds/'
language = 'en'

def play_person_spotted(name, volume = 0.3):
    if not os.path.exists(CACHE_FOLDER):
        os.makedirs(CACHE_FOLDER)

    filename = CACHE_FOLDER + name + ".mp3"
    if not os.path.exists(filename):
        text = "%s spotted, %s spotted" % (name, name)
        try:
            speech = gTTS(text=text, lang=language, slow=False)
        except:
            print('Error creating sound')
            return False
        try:
            speech.save(filename)
        except ValueError:
            print('Error saving sound')
            os.remove(filename)
            return False
    mixer.music.set_volume(volume)
    mixer.music.load(filename)
    print("playing sound: " + name)
    mixer.music.play()

    return True

