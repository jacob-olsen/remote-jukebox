import player_manger
import stroge_manger

class Mager:
    def __init__(self):
        pass

#testing
new = player_manger.Player()
new.setSong("/home/jacob/Music/Blacksmith, Blacksmith.opus",0)
new.play()

print(new.status())
input()
new.pause()
print(new.status())
input()
new.play()

while True:
    print(new.status())
    input()