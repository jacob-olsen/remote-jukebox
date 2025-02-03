import player_manger
import stroge_manger
import time

import threading

class Manger:
    def __init__(self):
        self.__songs = stroge_manger.Songs()
        self.__player = player_manger.Player()

        self.__playList = [2,3,1]
        self.__playListPos = 0
        self.__loop = 0 # 0=playList 1=loopList 2=loopSong

        self.__condition = threading.Condition()
        threading.Thread(target=self.__songDone, daemon=True).start()

        self.__player.done_event_add(self.__songDoneEvent)
        self.__player.status_event_add(self.__updateUi)#temp

    def setSong(self, ID):
        self.__player.setSong(self.__songs.findSongPath(ID),ID)

    def play(self):
        data = self.__player.status()
        if data["ID"]:
            self.__player.play()
        else:
            self.setSong(self.__playList[self.__playListPos])

    def __songDoneEvent(self):
        with self.__condition:
            self.__condition.notify_all()

    def __songDone(self):
        while True:
            with self.__condition:
                self.__condition.wait()
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
    
    def __updateUi(self):
        data = self.__player.status()
        print(data)



master = Manger()
while True:
    master.play()
    input()
