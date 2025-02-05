import stroge.database

class Songs:
    def __init__(self):
        self.__sql = stroge.database.MetaStroge()

    def findSongPath(self, id):
        if id == 1:
            return "/home/jacob/Music/Blacksmith, Blacksmith.opus"
        elif id == 2:
            return "/home/jacob/Music/Overlord - Lord of the End (Ainz's Song) [klsmddJFkm0].opus"
        elif id == 3:
            return "/home/jacob/Music/Woe to the People of Order - Technoblade’s War Ballad (Cami-Cat Full Cover) [yaxRl3He7xg].opus"
        
    def addSong(self, name, filePath):
        self.__sql.addSong(name, filePath)
    
    def getSongs(self, page, size):
        return self.__sql.getSongs(page, size)