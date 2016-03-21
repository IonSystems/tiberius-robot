import pyttsx
from predefined import PredefinedSounds
def say_new(text, voice_id="english", volume=None, rate=None):
    engine = pyttsx.init()
    if volume:
        engine.setProperty('volume', volume)
    if rate:
        engine.setProperty('rate', rate)

    engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()


def say_predefined(predefined=PredefinedSounds.ARE_YOU_LOST)

def play(file):


if __name__ == "__main__":
    say("MISSION COMPLETE")
    say("STARTING MISSION: Drive around car park.")
