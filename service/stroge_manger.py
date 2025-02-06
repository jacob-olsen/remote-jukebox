import stroge.database

class Songs:
    def __init__(self):
        self.__sql = stroge.database.MetaStroge()

    def findSongPath(self, id):
        return self.__sql.getSongPath(id)
        
    def addSong(self, name, filePath):
        self.__sql.addSong(name, filePath)
    
    def getSong(self, ID):
        data = self.__sql.getSong(ID)
        return {"ID":data[0], "name":data[1], "path":data[2]}

    def getSongs(self, page, size):
        data = []
        for temp in self.__sql.getSongs(page, size):
            data.append({"ID":temp[0],"name":temp[1]})
        return data