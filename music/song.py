import json


class Song:
    url = ""
    likes = 0
    name = ""

    def __init__(self, *kwargs):
        if len(kwargs) == 1:
            j = json.loads(kwargs[0])
            self.url = j["url"]
            self.likes = j["likes"]
            self.name = j["name"]
        elif len(kwargs) == 2:
            self.name = kwargs[0]
            self.url = kwargs[1]

    def toString(self):
        d = dict()
        d["url"] = self.url
        d["likes"] = self.likes
        d["name"] = self.name
        print(json.dumps(d))
        return json.dumps(d)

    def like(self):
        self.likes += 1
