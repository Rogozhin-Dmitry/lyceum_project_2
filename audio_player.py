from pygame import mixer
from pygame import time

mixer.init()


def background_music(music_path, volume):
    mixer.music.load(music_path)
    mixer.music.set_volume(volume)
    mixer.music.play()
    # while mixer.music.get_busy():
    #     pass



def sound_effects(effect_path, volume):
    mixer.Channel(1).play(mixer.Sound(effect_path))
    mixer.Channel(1).set_volume(volume)
    while mixer.Channel(1).get_busy():
        pass


background_music('music&effects/music/boss_fight/NGAHHH!! (from Undertale).mp3', 100)
mixer.music.unpause()
print(1)