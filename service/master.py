import player_manger
import stroge_manger



#testing
songs = stroge_manger.Songs()
new = player_manger.Player()


while True:
    print(new.status())
    cm = input()
    if cm.isnumeric():
        new.setSong(songs.findSong(int(cm)),int(cm))
    if cm == "s":
        new.pause()
    if cm == "p":
        new.play()