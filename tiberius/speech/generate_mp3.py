#!/usr/bin/python
from gtts import gTTS
from tempfile import NamedTemporaryFile

import pygame
import sys

# init game engine with audio
pygame.init()
pygame.mixer.init()
# mixer.init()
if len(sys.argv) > 1:
    text = sys.argv[1]
else:
    print "Must provide text as first arg."
    sys.exit()

filename = text.lower()
invalid_chars = " .,;:'@#~!'"
for char in invalid_chars:
    filename = filename.replace(char, "")

tts = gTTS(text=text, lang='en')
f = NamedTemporaryFile()
tts.save(filename + ".mp3")
# tts.save("thing.mp3")

# # load a sound
# print "About to play " + f.name
# sound = pygame.mixer.Sound("thing.mp3")
# #
# # # playback
# # sound.play()
#
# # Play f
# #f.close()
#
# # mixer.music.load(sound)
# # mixer.music.play()
# # f.close()
#
# explosion = media.load('thing.mp3', streaming=False)
# explosion.play()
