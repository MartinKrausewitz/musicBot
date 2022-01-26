import json
import random

from music import song

class Playlist:
    songs = dict()
    copysongs = songs.keys()
    name = ""
    limit = 10000

    def __init__(self, *kwargs):
        if len(kwargs) == 1:
            zw = json.loads(kwargs[0])
            self.name = zw["name"]
            zw.pop("name")
            for x in zw.keys():
                self.songs[x] = song.Song(zw[x])
        elif len(kwargs) == 2:
            self.name = kwargs[0]
            self.limit = kwargs[1]
        self.getnext()

    def toString(self):
        ret = dict()
        for x in self.songs.keys():
            ret[x] = self.songs[x].toString()
        return json.dumps(ret)

    def getSong(self, name):
        try:
            return self.songs[name]
        except KeyError:
            return None

    def addSong(self, name, url):
        if not self.getSong(name) is None:
            return False
        self.songs[name] = song.Song(name, url)

    def getnext(self):
        if len(self.copysongs) == 0:
            self.copysongs = [*self.songs]
            random.shuffle(self.copysongs)
            print(self.copysongs)
        if len(self.copysongs) == 0:
            return
        return self.songs[self.copysongs.pop()]


