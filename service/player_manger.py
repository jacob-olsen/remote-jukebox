import vlc #https://python-vlc.readthedocs.io/en/latest/api/vlc/MediaPlayer.html#

class Player:
    def __init__(self):
        self.__updateEventList = []
        self.__doneEventList = []
        self.__instance = vlc.Instance()
        self.__player = self.__instance.media_player_new()
        self.__songId = 0
        self.__media = None

        self.__event_manager = self.__player.event_manager()
        self.__event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.__done_event_triger)

        

    def __str__(self):
        return f"{self.__player.get_time()}-{self.__player.get_length()}:ms {int(self.__player.get_position()*100)}%"

    def setSong(self, filepath, songId):
        if self.__songId == songId:
            self.__player.stop()
            self.__player.set_time(0)
            self.__player.play()
            self.__status_event_triger()
        else:
            self.__songId = songId
            self.__player.stop()
            self.__media = self.__instance.media_new(filepath)
            self.__player.set_media(self.__media)
            self.__player.play()
            self.__status_event_triger()

    def play(self):
        self.__player.play()
        self.__status_event_triger()
    
    def pause(self):
        self.__player.pause()
        self.__status_event_triger()

    def skip(self, offset):
        pos = self.__player.get_time() + offset
        self.__player.stop()
        if pos < 0:
            pos = 0
        elif pos >= self.__player.get_length():
            self.__player.stop()
            self.__done_event_triger()
            return
        self.__player.set_time(pos)
        self.__player.play()
        self.__status_event_triger()

    def set(self, pos):
        if pos < 0:
            pos = 0
        elif pos >= self.__player.get_length():
            self.__player.stop()
            self.__done_event_triger()
        self.__player.set_time(pos)

    def status(self):
        return {"ID":self.__songId,
                "playing": self.__player.is_playing(),
                "play_time":self.__player.get_time(),
                "length":self.__player.get_length(),
                "position":int(self.__player.get_position()*100)}
    
    def status_event_add(self, listener):
        self.__updateEventList.append(listener)

    def __status_event_triger(self):
        for func in self.__updateEventList:
            func()
    
    def done_event_add(self, listener):
        self.__doneEventList.append(listener)

    def __done_event_triger(self,event):
        for func in self.__doneEventList:
            func()
