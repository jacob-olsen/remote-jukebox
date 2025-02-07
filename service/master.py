import service.player_manger
import service.stroge_manger
import hashlib
import os

import threading

class Manger:
    def __init__(self):
        self.__makeFolders()
        self.__clearTemp()

        self.__songs = service.stroge_manger.Songs()
        self.__player = service.player_manger.Player()

        self.__playList = []
        self.__playListPos = 0
        self.__loop = 0 # 0=playList 1=loopList 2=loopSong

        self.__condition = threading.Condition()
        threading.Thread(target=self.__songDone, daemon=True).start()

        self.__player.done_event_add(self.__songDoneEvent)
        self.__player.status_event_add(self.__updateUi)#temp

        self.__uiUpdateList = []

    def addSongToList(self,ID: int):
        if ID not in self.__playList:
            self.__playList.append(ID)
            self.__updateUi()
    def rmSongfromList(self,ID: int):
        if ID in self.__playList:
            self.__playList.remove(ID)
            if self.__playListPos >= len(self.__playList):
                self.__playListPos = 0
            self.setSong(self.__playList[self.__playListPos])
            self.__updateUi()
    def songMoveList(self,ID,move):
        findPos = self.__playList.index(ID)
        newPos = findPos + move
        if newPos < 0:
            return
        if newPos >= len(self.__playList):
            return
        oldID = self.__playList[newPos]
        self.__playList[newPos] = ID
        self.__playList[findPos] = oldID
        if self.__playListPos == findPos:
            self.__playListPos = newPos
        if self.__playListPos == newPos:
            self.__playListPos = findPos
        self.__updateUi()
    def getSongList(self):
        return self.__playList
    def jumpToSong(self, ID):
        self.__playListPos = self.__playList.index(ID)
        self.setSong(self.__playList[self.__playListPos])

    
    def getPlayList(self):
        data = []
        for id in self.__playList:
            info = self.__songs.getSong(id)
            data.append({"ID":id,"name":info["name"]})
        return data

    def setSong(self, ID):
        self.__player.setSong(self.__songs.findSongPath(ID),ID)

    def play(self):
        data = self.__player.status()
        if data["ID"]:
            self.__player.play()
        else:
            if len(self.__playList) > 0:
                if self.__playListPos >= len(self.__playList):
                    self.__playListPos = len(self.__playList) - 1
                self.setSong(self.__playList[self.__playListPos])

    def pause(self):
        self.__player.pause()
    
    def skip(self, offset):
        self.__player.skip(offset)
    
    def setTime(self,time):
        data = self.__player.status()
        self.__player.set(int(data["length"]*(time/100)))
        self.__updateUi()

    def skipBackward(self):
        time = self.playTime()
        if time["play_time"] < 10000:
            self.__playListPos -= 1
            if self.__playListPos < 0:
                self.__playListPos = len(self.__playList) -1
            self.setSong(self.__playList[self.__playListPos])
        else:
            self.setTime(0)

    def skipForward(self):
        self.__playListPos += 1
        if self.__playListPos >= len(self.__playList):
            self.__playListPos = 0
        self.setSong(self.__playList[self.__playListPos])

    def addUiUpdateList(self, func):
        self.__uiUpdateList.append(func)
    
    def playTime(self):
        data = self.__player.status()
        return {"play_time":data["play_time"],"length":data["length"],"position":data["position"]}

    def status(self):
        data = self.__player.status()
        data["playList"] = {}
        data["playList"]["list"] = self.getPlayList()
        data["loop"] = self.__loop
        if len(self.__playList) > self.__playListPos:
            data["playList"]["plaingID"] = self.__playList[self.__playListPos]
        else:
            data["playList"]["plaingID"] = 0
        return data

    def saveSong(self, songName, songPath):
        if not os.path.isfile(songPath):
            return "upload faild"
        hashSum = hashlib.md5(open(songPath,"rb").read()).hexdigest()

        if os.path.isfile(os.path.join("songs", f"{hashSum}.{songName.rsplit('.', 1)[1].lower()}")):
            return "song alrday exist"
        
        os.rename(songPath, os.path.join("songs", f"{hashSum}.{songName.rsplit('.', 1)[1].lower()}"))
        self.__songs.addSong(songName.rsplit('.', 1)[0], os.path.join("songs", f"{hashSum}.{songName.rsplit('.', 1)[1].lower()}"))
        return True

    def getSongs(self, page, size):
        return self.__songs.getSongs(page, size)
    def getSongsCount(self):
        return self.__songs.getSongsCount()

    def __updateUi(self):
        data = self.status()
        for func in self.__uiUpdateList:
            func(data)

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
                    if self.__playListPos < len(self.__playList)-1:
                        self.__playListPos += 1
                        print(f"start playlist-index:{self.__playListPos} song-id:{self.__playList[self.__playListPos]}")
                        self.setSong(self.__playList[self.__playListPos])
                    elif self.__loop == 1:
                        print("reset list pos")
                        self.__playListPos = 0
                        print(f"start playlist-index:{self.__playListPos} song-id:{self.__playList[self.__playListPos]}")
                        self.setSong(self.__playList[self.__playListPos])

    def __clearTemp(self):
        if os.path.isdir("temp/upload"):
            for taget in os.listdir("temp/upload"):
                os.remove(os.path.join("temp/upload",taget))
    def __makeFolders(self):
        self.__mkdir("temp")
        self.__mkdir("temp/upload")
        self.__mkdir("songs")
    def __mkdir(self,folderPath):
        if not os.path.isdir(folderPath):
            os.mkdir(folderPath)