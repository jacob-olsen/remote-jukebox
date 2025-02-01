import player_manger
import stroge_manger
import time

class Manger:
    def __init__(self):
        self.__songs = stroge_manger.Songs()
        self.__player = player_manger.Player()

        self.__playList = [1,2]
        self.__playListPos = 0
        self.__loop = 0 # 0=playList 1=loopList 2=loopSong

        #the event systme vikker til at loker op når den bruger event fra vlc til at skriver til vlc (NEED FIX)
        #self.__player.done_event_add(self.__songDone)

    def __songDone(self):
        print("song done")
        if self.__loop == 2:
            print("replaing")
            self.__player.set(0)
            self.__player.play()
        else:
            if self.__playListPos < len(self.__playList):
                self.__playListPos += 1
                print(f"start playlist-index:{self.__playListPos} song-id:{self.__playList[self.__playListPos]}")
                self.setSong(self.__playList[self.__playListPos])
            elif self.__loop == 1:
                print("reset list pos")
                self.__playListPos = 0
                print(f"start playlist-index:{self.__playListPos} song-id:{self.__playList[self.__playListPos]}")
                self.setSong(self.__playList[self.__playListPos])

    def setSong(self, ID):
        self.__player.setSong(self.__songs.findSongPath(ID),ID)


master = Manger()

master.setSong(1)
input()
master.setSong(3)
input()