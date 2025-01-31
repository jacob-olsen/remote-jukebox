import vlc #https://python-vlc.readthedocs.io/en/latest/api/vlc/MediaPlayer.html#
import time
player = vlc.MediaPlayer('file:///home/jacob/Music/Blacksmith, Blacksmith.opus')
player.play()

def on_media_end(event):
    print("Media playback has ended.")

event_manager = player.event_manager()
event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, on_media_end)

print("start")
time.sleep(1)
while not player.is_playing():
    time.sleep(0.1)
while player.is_playing():
    print(f"{player.get_time()}-{player.get_length()} {int(player.get_position()*100)}%")
    print(player.is_playing())
    time.sleep(1)
print("end")