import sqlite3
#"CREATE TABLE IF NOT EXISTS Config(Id INTEGER,Name TEXT, Value TEXT, PRIMARY KEY(Id));"
class MetaStroge:
    def __init__(self):
        self.__con = sqlite3.connect("info.sqlite")

        #make tabels if needet
        cur = self.__con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS song(ID INTEGER,name TEXT, path TEXT, PRIMARY KEY(Id));")#song
        cur.execute("CREATE TABLE IF NOT EXISTS album(ID INTEGER,name TEXT, PRIMARY KEY(Id));")#album
        cur.execute("CREATE TABLE IF NOT EXISTS auther(ID INTEGER,name TEXT, PRIMARY KEY(Id));")#auther
        cur.execute("CREATE TABLE IF NOT EXISTS playlist(ID INTEGER,name TEXT, PRIMARY KEY(Id));")#playlist
        cur.close()
    
    def add_song(self, name, path):
        cur = self.__con.cursor()
        cur.execute("INSERT INTO song (name, path) VALUES(?, ?);",(name, path))
        self.__con.commit()
        cur.close()

temp = MetaStroge()
temp.add_song("test1","test2")