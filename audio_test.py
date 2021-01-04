import audio_player
from pygame import mixer

mixer.init()

# audio_player.background_music('music&effects/music/menu/Florian Christl - Close Your Eyes.mp3', 50)
# audio_player.sound_effects('music&effects/music/boss_fight/NGAHHH!! (from Undertale).mp3', 50)


# mixer.Channel(0).play(mixer.Sound('music&effects/music/menu/Florian Christl - Close Your Eyes.mp3'))
# mixer.Channel(0).set_volume(10)
# mixer.Channel(1).play(mixer.Sound('music&effects/music/boss_fight/NGAHHH!! (from Undertale).mp3'))
# mixer.Channel(1).set_volume(10)


mixer.Channel(0).play(mixer.Sound('music&effects/music/menu/Florian Christl - Close Your Eyes.mp3').play())
mixer.Channel(1).play(mixer.Sound('music&effects/music/boss_fight/NGAHHH!! (from Undertale).mp3'))