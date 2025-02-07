import sqlite3
#"CREATE TABLE IF NOT EXISTS Config(Id INTEGER,Name TEXT, Value TEXT, PRIMARY KEY(Id));"
class MetaStroge:
    def __init__(self):
        self.__con = sqlite3.connect("info.sqlite", check_same_thread=False)

        #make tabels if needet
        cur = self.__con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS song(ID INTEGER,name TEXT, path TEXT, PRIMARY KEY(Id));")#song

        cur.execute("CREATE TABLE IF NOT EXISTS album(ID INTEGER,name TEXT, PRIMARY KEY(Id));")#album
        cur.execute("CREATE TABLE IF NOT EXISTS albumEntry(ID INTEGER, albumID INTEGER, songID INTEGER, PRIMARY KEY(Id), FOREIGN KEY(albumID) REFERENCES album(ID), FOREIGN KEY(songID) REFERENCES song(ID));")#albumEntry
        
        cur.execute("CREATE TABLE IF NOT EXISTS playlist(ID INTEGER,name TEXT, PRIMARY KEY(Id));")#playlist
        cur.execute("CREATE TABLE IF NOT EXISTS playlistEntry(ID INTEGER,slot INTEGER,playlistID INTEGER, songID INTEGER, PRIMARY KEY(Id), FOREIGN KEY(playlistID) REFERENCES playlist(ID), FOREIGN KEY(songID) REFERENCES song(ID));")#playlist entry
        
        cur.execute("CREATE TABLE IF NOT EXISTS auther(ID INTEGER,name TEXT, PRIMARY KEY(Id));")#auther
        cur.close()
    
    def addSong(self, name, path):
        cur = self.__con.cursor()
        cur.execute("INSERT INTO song (name, path) VALUES(?, ?);",(name, path))
        Id = cur.lastrowid
        self.__con.commit()
        cur.close()
        return Id
    def setName(self, ID, name):
        cur = self.__con.cursor()
        cur.execute("UPDATE song SET name=? WHERE ID=?;",(name, ID))
        Id = cur.lastrowid
        self.__con.commit()
        cur.close()
    def getSong(self, ID):
        cur = self.__con.cursor()
        cur.execute("SELECT * FROM song WHERE ID = ?;",(ID,))
        data = cur.fetchone()
        cur.close()
        return data
    def getSongPath(self, ID):
        cur = self.__con.cursor()
        cur.execute("SELECT path FROM song WHERE ID = ?;",(ID,))
        data = cur.fetchone()
        cur.close()
        return data[0]
    def getSongs(self,page,size):
        cur = self.__con.cursor()
        cur.execute("SELECT ID, name FROM song LIMIT ? OFFSET ?;",(size,int(page*size)))
        data = cur.fetchall()
        cur.close()
        return data
    def getSongCount(self) -> int:
        cur = self.__con.cursor()
        cur.execute("SELECT COUNT(*) FROM song;")
        data = cur.fetchone()
        cur.close()
        return data[0]