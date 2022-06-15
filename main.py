import threading
import keyboard
import pygame
import time
import json
from pydub import AudioSegment, playback
from pydub.playback import play

binds = []
stopbind = ""
file = ""
end = False

class music():
    def pyplay(file):
        global play_obj
        global end

        pygame.mixer.init(devicename='Line (Voicemod Virtual Audio Device (WDM))')

        pygame.mixer.music.load(file)

        song = AudioSegment.from_mp3(file)

        song = song - 10

        pygame.mixer.music.play()
        pygame.mixer_music.set_volume(0.7)

        play_obj = playback._play_with_simpleaudio(song)

def cls():
    if os.name == "nt":
        clear = lambda: os.system('cls')
        clear()
    else:
        clear = lambda: os.system('clear')
        clear()

def initbinds():
    global stopbind
    global binds
    global bindstring

    cls()

    print("-" * 90)

    with open("config.json", "r") as f:
        jsonfile = f.read()
        j = json.loads(jsonfile)

    bindstring = j["play"]

    try:
        binds = bindstring.split("|")
    except:
        print("invalid binds")
        quit()

    #print(binds)

    stopbind = "ctrl+n"

    for item in binds:
        try:
            bind, filename = item.split("!")
            print(bind + ": "+filename)
            if filename == "stop":
                stopbind = bind
        except:
            pass

    print("""
CTRL + SHIFT + Z + V: edit volume on a range of 0-1 (decimals work)
CTRL + SHIFT + Z + Y: add a .wav file (MUST BE A .WAV FILE)
CTRL + SHIFT + Z + R: remove a sound
    """)

    print("-" * 90)

initbinds()

while True:
    for item in binds:
        bind, file = item.split("!")
        if keyboard.is_pressed(bind) and bind != stopbind:
            print("playing")

            try:
                pygame.mixer.music.stop()
                play_obj.stop()
            except:
                pass

            t1 = threading.Thread(target=music.pyplay, args=(file,)).start()
            time.sleep(0.15)

        elif keyboard.is_pressed(stopbind):
            print("clearing thread")
            pygame.mixer.music.stop()
            play_obj.stop()
            time.sleep(0.15)

        elif keyboard.is_pressed("ctrl+shift+z+v"):
            volume = input("volume to set? (0-1)\n>")

            try:
                pygame.mixer_music.set_volume(float(volume))
                play_obj.volume

                print("set")
            except:
                print("was unable to set: " + str(e))

        elif keyboard.is_pressed("ctrl+shift+z+y"):
            try:
                directory = input("directory?\n>")
            except:
                print("an issue occured, try again")
                continue

            if ".mp4" in directory:
                try:
                    sound = AudioSegment.from_mp3(directory)
                    sound.export(directory+".wav", format="wav")
                    directory += ".wav"
                except:
                    raise

            directory = directory.replace("\\", "\\\\")

            bindtoadd = input("bind to add as? (ex: ctrl+l)\n>")
            
            bindstring = bindstring.replace("\\", "\\\\")

            bindstring += f"|{bindtoadd}!"+directory

            print(bindstring)

            with open("config.json", "w") as f:
                f.write("""
{
  "play": \""""+bindstring+"""\",
  "volume": "50"
}
                """)
                f.flush()

            initbinds()

        elif keyboard.is_pressed("ctrl+shift+z+r"):
            ebinds = {}
            for x in range(len(binds)):
                x = x
                print(f"[{str(x)}] {binds[x]}")
                ebinds[str(x)] = binds[x]

            bind2remove = input("bind to remove?\n\n>")

            if int(bind2remove) not in range(len(binds)):
                print("invalid")
                continue

            bindstring = bindstring.replace(ebinds[bind2remove]+"|", "")

            bindstring = bindstring.replace("\\", "\\\\")

            print(bindstring)

            with open("config.json", "w") as f:
                f.write("""
{
  "play": \""""+bindstring+"""\",
  "volume": "50"
}
                """)
                f.flush()

            initbinds()
