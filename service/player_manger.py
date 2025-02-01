import vlc

class Player:
    def __init__(self):
        self.__instance = vlc.Instance()
        self.__player = self.__instance.media_player_new()
        self.__media = None

    def __str__(self):
        return f"{self.__player.get_time()}-{self.__player.get_length()}:ms {int(self.__player.get_position()*100)}%"

    def setSong(self, filepath):
        self.__player.stop()
        self.__media = self.__instance.media_new(filepath)
        self.__player.set_media(self.__media)
        self.play()

    def play(self):
        self.__player.play()
    
    def pause(self):
        self.__player.pause()

    




#testing
new = Player()
new.setSong("/home/jacob/Music/Blacksmith, Blacksmith.opus")
new.play()

print(str(new))
input()
new.pause()
print(str(new))
input()
new.play()

while True:
    print(str(new))
    input()

