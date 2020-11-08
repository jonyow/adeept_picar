

from pygame import mixer

mixer.init()
file = '../sounds/jackie.mp3'

mixer.music.load(file)
mixer.music.play()
